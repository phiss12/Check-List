from flask import Flask, request, Response, jsonify, send_from_directory
from tinyDB import tinyDB
from flask_swagger_ui import get_swaggerui_blueprint
from days_between import days_between

db = tinyDB("Todo.json")

app = Flask(__name__)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={ 'app_name': "TODO" })
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

@app.route("/todo/list")
def getGetAllTodo():
    listWithDiffofDays = []
    listofSortedTodo = []
    for dict in db.all():
        if dict["Timestamp"] == '' or dict["Deadline"] == '' or dict["Timestamp"] == dict["Deadline"]:
            listofSortedTodo.append(dict)
        else:
            listWithDiffofDays.append((days_between(dict["Timestamp"],dict["Deadline"]), dict))
    
    listWithDiffofDays.sort()

    for i in listWithDiffofDays:
        listofSortedTodo.append(i[1])

    return jsonify(listofSortedTodo)

@app.route("/todo", methods = ["POST"])
def createNewTodo():
    newTodo = request.get_json()
    db.insert(newTodo["Todo"], newTodo["Timestamp"], newTodo["Deadline"])
    return Response('{"message":"success"}', status=201, mimetype='application/json')

@app.route("/todo/<id>", methods = ["PUT"])
def updateTodo(id):
    try:
        newTodo = request.get_json()
        db.update({'Todo': newTodo["Todo"]}, id)
        db.update({'Timestamp': newTodo["Timestamp"]}, id)
        db.update({'Deadline': newTodo["Deadline"]}, id)
        response = jsonify('{"message::"item updated"}')
        response.status_code = 201
        return response
    except KeyError as keyerror:
        response = jsonify('{"message::"item does not exist"}')
        response.status_code = 404
        return response     
    
@app.route("/todo/<id>", methods = ["DELETE"])
def deleteTodo(id):
    try:
        db.remove(id)
        response = jsonify('{"message::"item deleted"}')
        response.status_code = 200
        return response
    except KeyError as keyerror:
        response = jsonify('{"message::"item does not exist"}')
        response.status_code = 404
        return response     

if __name__ == "__main__":
    app.run(host= "localhost",port=8181,debug=True)

