from flask import Flask, jsonify, Response, json, render_template, request

# jsonify json모듈을 변환 시키는 파일
# Respons response형식으로 변환시켜주는 라이브러리
# json json형식으로 변환시켜주는 라이브러리
# render_template html파일을 return 하고 싶을때 쓰는 라이브러리 
# request 요청받기 위한 라이브러리

app = Flask(__name__) # 파일이름을 등록

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
  
  return render_template(
    'index.html', title = title, name = name, items=item_list
    )
  



if __name__ == '__main__':
  app.run(host="localhost", port="8888", debug=True)