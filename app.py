from flask import Flask, jsonify, Response, json, render_template, request, redirect, url_for
from datetime import datetime

# jsonify json모듈을 변환 시키는 파일
# Respons response형식으로 변환시켜주는 라이브러리
# json json형식으로 변환시켜주는 라이브러리
# render_template html파일을 return 하고 싶을때 쓰는 라이브러리 
# request 요청받기 위한 라이브러리

app = Flask(__name__) # 파일이름을 등록

# 2000 Byte짜리 파일이 10개가 만들어지면 다시 처음으로 돌아감
if not app.debug:
  import logging
  from logging.handlers import RotatingFileHandler
  file_handler = RotatingFileHandler(
    'server.log', maxBytes=2000, backupCount=10,
  )
  file_handler.setLevel(logging.WARNING)
  app.logger.addHandler(file_handler)


@app.errorhandler(404) # 존재하지 않는 주소로 요청을 하면 작동하는 에러코드
def page_not_found(error):
  app.logger.error(error)
  return "<h1>404 Error 해당 페이지는 존재하지 않습니다.</h1>", 404

@app.before_request # 요청이 올때마다 실행함
def before_request_fn():
  print("Http요청이 올때마다 실행")

@app.after_request 
def after_request_fn(response):
  print('Http요청 처리가 끝난 후 브라우저에 응답하기전 실행')
  return response

@app.route("/") # 자바로치면 GetMapping("/")임
def test():
  return "<h1>Hello Flask World!!!</h1>"

@app.route("/hello")
def hello():
  a = 10 + 20
  return f"<a href='https://nvaer.com'>{a}이동</a>"

@app.route("/hi")
def hi():
  html = """
    <div>
      <h1>안녕하세요</h1>
      <p>ㅋㅋㅋㅋㅋㅋ</p>
    </div>
  """
  return html

@app.route("/id/<username>")
def get_id(username):
  print(username)
  return f"<h1>요청한 아이디 : {username}</h1>"

@app.route("/add/<int:num>")
def get_num(num):
  num = num * 100
  return f"<h1>계산결과 : {num}</h1>"

# ====== json 리턴시키기 =======
@app.route("/json")
def json_test():
  data={
    'name' : '고길동',
    'age' : 20,
    'gender' : 'M'
  }
  return jsonify(data)

@app.route("/json2")
def json_test2():
  data={
    'name' : '고길동',
    'age' : 20,
    'gender' : 'M'
  }

  response = Response(response=json.dumps( data ), status=200,
                      mimetype='application/json'
                      )
  return response

# 로그인 페이지로 이동하는 route 함수
@app.route('/login')
def login_page():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
  username = request.form.get('username')
  password = request.form.get('password')
  print(username, password)

  return jsonify({'name' : username, 'pw' : password})

# 쿼리스트링 받기
@app.route('/qs')
def qs():
  kw = request.args.get('kw')
  page = request.args.get('page')
  print(request.args)

  return f"<h1>kw : {kw}, page : {page} </h1>"

@app.route('/api')
def api():
  data = request.get_json()
  print(data)
  name = data.get('username')
  age = data.get('age')

  return f"name : {name} age : {age}"

# jinja2 템플릿을 활용 
@app.route('/index')
def index():
  title = "타이틀!!"
  name = "고길동"
  item_list = ['apple', 'banana', 'melon', 'mango']

  user = {
    "name" : None,
    "items" : ['사과', '딸기', '배']
  }
  msg = "<b>Hello Flask</b>"
  today = datetime.now()
  
  return render_template(
    'index.html', title = title, name = name, items=item_list,
    user = user, msg=msg, today=today
    )

@app.route("/home")
def home():
  return render_template("home.html")

# === url_for ===
# url을 통해서 접근 가능한 라우터들을 함수명으로 접근하도록 해줌
@app.route('/user/<username>')
def show_user(username):
  return f"이름 : {username}"

@app.route('/redirect/<name>')
def redirect_aa(name):
  print(f"redirect에서 받은 이름 : {name}")
  return redirect(url_for('show_user', username=name))



if __name__ == '__main__':
  app.run(host="localhost", port="8888", debug=True)