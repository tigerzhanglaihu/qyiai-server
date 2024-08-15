## QyiAi致力于使用AI实现可落地的适用方案
QyiAi是基于Langchain的本地知识库解决方案
## QyiAi的能力
我们的解决方案，可满足从个人到公司不同客户的需求。
### 知识库
pdf，excel，csv ，url ，txt 产生自我的知识库。
### 机器人
自定义与QyiAi自有知识库体系，前所未有的提高效率。
### 共享知识库与机器人
您创建的知识库与机器人可以共享给需要的朋友，当然您也可以通过共享自己的知识库，获得收益。
### Saas解决方案
我们将提供专业的Saas解决方案，让您的企业无缝接入到QyiAi，与时代同步。
### 本地化解决方案
提供本地化部署方案，让您的隐私和您的数据安全得到完善的保护。
### 咨询
客制化的解决方案，期待与您一起同行。
可以访问我们的网站www.qyiai.cn 试用。

## 安装前端 -- Front

### 1. 获取前端代码 `last.zip`
下载前端代码包 `last.zip`。

### 2. 解压到 Apache 或 Nginx 对应目录
将 `last.zip` 文件解压到你的 Web 服务器目录中：

```sh
# 示例：解压到 Apache 服务器目录
unzip last.zip -d /var/www/html/

# 示例：解压到 Nginx 服务器目录
unzip last.zip -d /usr/share/nginx/html/
```

### 3. 获取 MySQL 备份代码 `mysqlscript.zip`
下载 MySQL 备份代码包 `mysqlscript.zip`。

### 4. 创建数据库 `qyiai`
登录到你的 MySQL 数据库并创建一个新的数据库 `qyiai`：

```sql
CREATE DATABASE qyiai;
```

### 5. 导入备份到 `qyiai`
将 `mysqlscript.zip` 解压并导入到数据库 `qyiai` 中：

```sh
unzip mysqlscript.zip
mysql -u your_username -p qyiai < path/to/your/mysqlscript.sql
```

### 6. 修改 `wp-config.php` 中对应的 `DB_NAME`，`DB_USER`，`DB_PASSWORD`
打开并编辑 `wp-config.php` 文件，更新数据库名称、用户名和密码：

```php
define('DB_NAME', 'qyiai');
define('DB_USER', 'your_username');
define('DB_PASSWORD', 'your_password');
```

### 7. 查看结果
启动你的 Apache 或 Nginx 服务器，打开浏览器并访问你的前端页面，检查是否正确显示。

```sh
# 示例：启动 Apache 服务器
sudo systemctl start apache2

# 示例：启动 Nginx 服务器
sudo systemctl start nginx
```

## 安装后端 -- Server

### 1. 安装 Ollama
根据你的操作系统安装 Ollama：

```sh
# 示例：安装 Ollama（Linux 或 macOS）
curl -sSL https://ollama.dev/install.sh | sh

# 示例：安装 Ollama（Windows，使用 PowerShell）
iwr -useb https://ollama.dev/install.ps1 | iex
```

### 2. 推送相关模型，比如 `qwen2`
将相关模型推送到 Ollama：

```sh
ollama push qwen2
```

### 3. 配置模型关系在 `config.ini` 中
打开 `config.ini` 文件，并配置模型关系：

```ini
[models]
#ollma 模型名称 20242424 llama2-chinese llama3
LLM_OLLAMA_MODEL = qwen2
```

### 4. 申请阿里云通义千问 Key
在阿里云控制台申请通义千问 API 的 Key。

### 5. 配置 URL 和 Key 对应关系在 `config.ini` 中
更新 `config.ini` 文件，添加 API URL 和 Key：

```ini
#阿里云key
LLM_NETWORK_KEY = sk-72741c6XXXXXXXXXX
#api的地址，根据阿里云的说法，openAI与阿里云通用
LLM_NETWORK_URL = https://dashscope.aliyuncs.com/compatible-mode/v1
#ollma 模型名称 20242424 llama2-chinese llama3
LLM_NETWORK_MODEL = qwen-turbo
```

### 6. 安装依赖项
安装 `requirements.txt` 文件中的所有依赖项：

```sh
pip install -r requirements.txt
```

### 7. 下载 Embedding 模型
下载 Embedding 模型并解压到指定目录：

```sh
git clone https://www.modelscope.cn/Jerry0/text2vec-large-chinese.git
```

### 8. 运行 main 测试
一切准备就绪后，运行 `main.py` 文件进行测试：

```sh
python main.py
```

通过以上步骤，你应该可以成功安装并配置前端和后端系统。如有任何问题，请参考相关文档或联系我们的技术支持。
