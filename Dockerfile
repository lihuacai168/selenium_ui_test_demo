# 使用官方的Python镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 将依赖项复制到容器中并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 将您的代码复制到容器中
COPY . .

# 执行脚本
CMD ["python", "blog.py"]
