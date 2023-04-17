from time import time
from flask import Flask
from flask import request
from flask import g
from werkzeug.exceptions import BadRequest


app = Flask(__name__)
@app.route("/")
def index():
    return "Hello web!"

@app.route("/greet/<name>/")
def greet_name(name: str):
    return f"Hello {name}!"

@app.route("/<int:city>")
def greet_city(city: int):
    return f"Hello {city}, {isinstance(city, int)}!"


#Обрабатываем параметры запроса (query string)
@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"



#Обрабатываем тело запроса и возвращаем кастомные
#статус-коды
#примеры
#http --form POST http://127.0.0.1:5000/status/ code=202
#http -v --json POST http://127.0.0.1:5000/status/ code=205

@app.route("/status/", methods=["GET", "POST"])
def custom_status_code():
    if request.method == "GET":
        return """\
        To get response with custom status code
        send request using POST method
        and pass `code` in JSON body / FormData
        """


    print("raw bytes data:", request.data)

    if request.form and "code" in request.form:
        return "code from form", request.form["code"]

    if request.json and "code" in request.json:
        return "code from json", request.json["code"]

    if request.method == 'POST':
        data = request.json
        return f'{request.method}, {data["data"]}, {request.data}'

    return "", 204

@app.route("/state/", methods=["GET", "POST"])
def test():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}, {request.method}"


#Обработчики before_request, after_request; объект g
@app.before_request
def process_before_request():
    """
    Sets start_time to `g` object
    """
    g.start_time = time()

@app.after_request
def process_after_request(response):
    """
    adds process time in headers
    """
    if hasattr(g, "start_time"):
        response.headers["process-time"] = time() - g.start_time
    return response


#Логгер, обработка исключений
@app.route("/power/")
def power_value():
    x = request.args.get("x") or ""
    y = request.args.get("y") or ""
    if not (x.isdigit() and y.isdigit()):
        app.logger.info("invalid values for power: x=%r and y=%r", x, y)
        raise BadRequest("please pass integers in `x` and `y` query params")
    x = int(x)
    y = int(y)
    result = x ** y
    app.logger.debug("%s ** %s = %s", x, y, result)
    return str(result)

#Обработка непредвиденных исключений
@app.route("/divide-by-zero/")
def do_zero_division():
    return 1 / 0

@app.errorhandler(ZeroDivisionError)
def handle_zero_division_error(error):
    print(error) # prints str version of error: 'division by zero'
    app.logger.exception("Here's traceback for zero division error")
    return "Never divide by zero!", 400