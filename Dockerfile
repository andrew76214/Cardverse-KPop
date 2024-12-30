# 使用 Python 官方映像
FROM python:3.9-slim

# 安裝必要的系統工具和庫
RUN apt-get update && apt-get install -y \
    gcc libmariadb-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製需求文件並安裝依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . /app

# 曝露 Flask 預設端口
EXPOSE 5000

# 等待 MySQL 準備完成的腳本
COPY wait_for_sql.sh /usr/local/bin/wait_for_sql.sh
RUN chmod +x /usr/local/bin/wait_for_sql.sh

# 啟動 Flask 應用
CMD ["sh", "wait_for_sql.sh", "python", "run.py"]