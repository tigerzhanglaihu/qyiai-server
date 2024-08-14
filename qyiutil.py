from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import configparser
import logging
import os
import time
import random
import string
from langchain_openai import ChatOpenAI

# Configure logging module
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class localbot():
    def __init__(self, **params):
        config_file_path = 'config.ini'
        # 创建配置解析器对象
        config = configparser.ConfigParser()
        # 读取配置文件
        config.read(config_file_path, encoding="utf8")
        # 参数字典
        config_params = {
            'MODEL_ROOT_PATH': 'MODEL_ROOT_PATH',
            'LLM_MODEL_DOWNLOAD_URL': 'LLM_MODEL_DOWNLOAD_URL',
            'EMBEDDING_MODEL_DOWNLOAD_URL': 'EMBEDDING_MODEL_DOWNLOAD_URL',
            'EMBEDDING_MODEL_PATH': 'EMBEDDING_MODEL_PATH',
            'LLM_MODEL_PATH': 'LLM_MODEL_PATH',
            'EMBEDDING_MODEL': 'EMBEDDING_MODEL',
            'LLM_LOCAL_MODEL': 'LLM_LOCAL_MODEL',
            'LLM_ONLINE_MODEL': 'LLM_ONLINE_MODEL',
            'VECTOR_DB_PATH': 'VECTOR_DB_PATH',
            'FILE_UPLOAD_PATH': 'FILE_UPLOAD_PATH',
            'LLM_OLLAMA_MODEL': 'LLM_OLLAMA_MODEL',
            'LLM_NETWORK_KEY': 'LLM_NETWORK_KEY',
            'LLM_NETWORK_URL': 'LLM_NETWORK_URL',
            'LLM_NETWORK_MODEL': 'LLM_NETWORK_MODEL',
        }

        for attr, key in config_params.items():
            try:
                setattr(self, attr, config.get('local', key))
            except configparser.NoOptionError:
                print(f"配置文件中缺少选项: {key}")
            except configparser.NoSectionError:
                print(f"配置文件中缺少部分: 'local'")
            except Exception as e:
                print(f"读取配置文件错误 {key}: {e}")

def get_csv_txt(file_path):
    # Load documents from CSV file
    loader = CSVLoader(file_path=file_path, encoding='utf8')
    docs = loader.load()
    return docs

def get_txtfile_txt(file_path):
    # Load documents from CSV file
    loader = TextLoader(file_path=file_path, encoding='utf8')
    docs = loader.load()
    return docs

def get_pdf_txt(file_path):
    # Load documents from CSV file
    loader = PyPDFLoader(file_path=file_path)
    docs = loader.load()
    return docs

def get_filename_without_extension(file_path):
    filename = os.path.basename(file_path)  # 获取文件名
    filename_without_extension = os.path.splitext(filename)[0]  # 去掉后缀
    return filename_without_extension


def faiss_db(directory):
    # 检查指定目录是否存在
    if not os.path.isdir(directory):
        print(f"The specified directory {directory} does not exist.")
        return False
    # 定义要检查的文件名
    file_names = ['index.faiss', 'index.pkl']
    # 检查所有文件是否都存在
    all_files_exist = all(os.path.isfile(os.path.join(directory, file_name)) for file_name in file_names)
    return all_files_exist


def import_file_to_vectorsdb(file_path, vector_db):
    # 初始化 localbot 对象
    envInit = localbot()
    try:
        model_name = envInit.EMBEDDING_MODEL_PATH + '/' + envInit.EMBEDDING_MODEL
        # 日志记录函数
        def log_info(message):
            logging.info(message)

        # 获取文件类型
        file_type = os.path.splitext(file_path)[1].lstrip('.')

        # 根据文件类型加载文档
        if file_type == 'csv':
            docs = get_csv_txt(file_path)
        elif file_type == 'pdf':
            docs = get_pdf_txt(file_path)
        elif file_type == 'txt':
            docs = get_txtfile_txt(file_path)
        else:
            log_info("不支持的文件类型")
            return "E", "不支持的文件类型"

        # 将文档分割成更小的部分
        text_splitter = RecursiveCharacterTextSplitter()
        documents = text_splitter.split_documents(docs)
        log_info(f"将文档分割成 {len(documents)} 部分。")

        # 初始化嵌入模型
        embedding = HuggingFaceEmbeddings(model_name=model_name)
        log_info(f"初始化 Hugging Face 嵌入模型：{model_name}")

        # 生成唯一文件名
        timestamp = time.strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        unique_filename = f"{timestamp}_{random_str}"

        if vector_db == '':
            vector_store_path = envInit.VECTOR_DB_PATH + '/' + unique_filename
        else:
            vector_store_path = envInit.VECTOR_DB_PATH + '/' + vector_db

        # 为文档生成嵌入向量，如果向量数据库已存在则追加，否则创建新的向量数据库
        if not faiss_db(vector_store_path):
            vector_store = FAISS.from_documents(documents, embedding)
            log_info("创建新的向量存储。")
        else:
            vector_store = FAISS.load_local(vector_store_path, embedding, allow_dangerous_deserialization=True)
            vector_store.add_documents(documents)
            log_info("向现有的向量存储添加嵌入。")

        # 保存向量存储
        vector_store.save_local(vector_store_path)
        log_info(f"将向量存储保存到 {vector_store_path}")
        return "S", vector_store_path

    except Exception as e:
        # 记录错误信息并返回
        error_message = str(e)
        logging.error(f"导入文件到向量数据库时发生错误：{error_message}")
        return "E", error_message


def prompt_chat(prompt, user_question):
    instenv = localbot()
    try:
        # 创建 Langchain
        llm = Ollama(model=instenv.LLM_OLLAMA_MODEL)
        template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI bot. Your name is QyiAi."),
            ("human", prompt + "{user_question}"),
        ])
        logging.info(f"template：{template} ")
        prompt_value = template.invoke(user_question)
        logging.info(f"prompt_value：{prompt_value} ")
        # 运行链条以获得答案
        response = llm.invoke(prompt_value)
        logging.info(f"用户问题：{user_question}，模型回答：{response}")

        return "S", response

    except Exception as e:
        error_message = str(e)
        logging.error(f"聊天提示时发生错误：{error_message}")
        return "E",error_message

# 语言模型聊天
def robot_chat(question):
    instenv = localbot()
    try:
        # 创建Langchain
        llm = Ollama(model=instenv.LLM_OLLAMA_MODEL)
        response = llm.invoke(question)
        return "S", response
    except Exception as e:
        error_message = str(e)
        logging.error(error_message)
        return "E", error_message

# 获取检索器
def get_retriever(embeddingsmodel_name, faiss_path):
    logging.info(f"embeddingsmodel_name: {str(embeddingsmodel_name)} faiss_path: {str(faiss_path)}")
    try:
        embedding = HuggingFaceEmbeddings(model_name=embeddingsmodel_name)
        vectordb = FAISS.load_local(faiss_path, embedding, allow_dangerous_deserialization=True)
        return vectordb.as_retriever()
    except Exception as e:
        logging.error(f"An error occurred while loading the retriever: {str(e)}")
        return None

# 获取检索问题的 QA 对象
def _get_retrieval_qa(vertor_db):
    instenv = localbot()
    faiss_path = os.path.join(instenv.VECTOR_DB_PATH, str(vertor_db))
    # 创建Langchain
    llm = Ollama(model=instenv.LLM_OLLAMA_MODEL)
    # 增加网络版本的llm  20240804
    cust_llm = ChatOpenAI(
        api_key=instenv.LLM_NETWORK_KEY,  # 如果您没有配置环境变量，请在此处用您的API Key进行替换
        base_url=instenv.LLM_NETWORK_URL,  # 填写DashScope base_url
        model=instenv.LLM_NETWORK_MODEL
    )

    retriever = get_retriever(instenv.EMBEDDING_MODEL_PATH + '/' + instenv.EMBEDDING_MODEL, faiss_path)
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        verbose=True,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True,
        condense_question_llm=cust_llm #增加网络版本的gpt 20240804
    )
    return qa

# 向量数据库聊天
def vertor_chat(vertor_db, question, chat_history):
    try:
        qa = _get_retrieval_qa(vertor_db)
        response = qa.invoke({"question": question, "chat_history": chat_history})
        return "S", response["answer"]
    except Exception as e:
        error_message = str(e)
        logging.error(error_message)
        return "E", error_message