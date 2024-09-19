from flask import Flask, request, render_template
from flask_frozen import Freezer
from threading import Thread

app = Flask(__name__)
freezer = Freezer(app)

@app.route('/')
def home():
  return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']
  # 로그인 로직
  return '내용을 입력하세요'


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


if __name__ == '__main__':
  freezer.freeze()
