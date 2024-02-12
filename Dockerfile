# 指定基底映像檔
FROM python:3.10

# 將工作目錄設定為 /app
WORKDIR /app

# 向映像檔複製內容
# 將 requirements-flask.txt 複製到 /app 內
COPY requirements-flask.txt .

# 安裝 Python 套件
# 使用 pip install 命令
RUN pip3 install -r requirements-flask.txt

# 將本地的 run.py 檔案複製到容器的 /app 資料夾內
COPY . .

# 指定 Docker 啟動容器時要運行的命令
CMD ["python", "run.py"]
