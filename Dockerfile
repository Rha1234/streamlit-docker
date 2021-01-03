#PythonのDockerイメージを指定
FROM python:3.8.7-slim

#イメージの/app内をワークディレクトリに設定
WORKDIR /app

# requirements.txtをコピー
COPY requirements.txt .

#ライブラリインストール
RUN pip install --upgrade pip
RUN pip install streamlit
RUN pip install -r requirements.txt

#ローカルのファイルをイメージのappディレクトリにコピー
COPY ./app/ /app

#エントリーポイント（常に実行するコマンドみたいなもの？）
ENTRYPOINT [ "streamlit", "run"]

#エントリーポイントで指定するファイル？
CMD ["/app/main.py"]