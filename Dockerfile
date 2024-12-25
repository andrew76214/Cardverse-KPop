# 使用官方 Python 映像檔
FROM python:3.9-slim

# 為了避免某些編譯需求或系統工具需求，也可以在這裡做 apt-get install (看需求)
# RUN apt-get update && apt-get install -y <some-deps>

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 進入容器
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案原始碼到容器中
COPY . /app

# Expose 5000 port（Flask預設port），可依需求修改
EXPOSE 5000

# 設定容器啟動時要執行的指令，假設您的 Flask app 入口是 app.py
CMD ["python", "app.py"]