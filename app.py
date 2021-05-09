from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from json import dumps
import json
import psycopg2

app = Flask(__name__)

engine = create_engine("postgresql://postgres:123@localhost/newNewNewTest")
db = scoped_session(sessionmaker(bind=engine))
Session = sessionmaker(bind=engine)
session = Session()

app.secret_key = 'test_key'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route('/addclient', methods=['POST'])
def addClient():
    request_json = request.get_json()
    type = request_json.get('type')
    name = request_json.get('name')
    adress = request_json.get('adress')
    commentaru = request_json.get('commentaru')

    db.execute("INSERT INTO clients (type, name, adress, commentaru) VALUES (:type, :name, :adress, :commentaru)",
            {"type":type, "name":name, "adress":adress, "commentaru":commentaru})
    db.commit()
    return "ok" 

@app.route('/addorder', methods=['POST']) 
def addOrder():
    request_json = request.get_json()
    clientId = request_json.get('clientId')
    description = request_json.get('description')
    adress = request_json.get('adress')
    cost = request_json.get('cost')
    db.execute("INSERT INTO orders (clientId, description ,adress ,cost ) VALUES (:clientId ,:description ,:adress ,:cost )", 
            {"clientId":clientId, "description":description, "adress":adress, "cost":cost})
    db.commit()
    return "ok"

@app.route('/getclient/<int:id>', methods=['GET'])
def getClient(id):
    result = db.execute("SELECT * FROM clients WHERE id = " + str(id))
    return json.dumps([dict(r) for r in result], default=str)

@app.route('/getclients', methods=['GET'])
def getClients():
    result = db.execute("SELECT * FROM clients")
    return json.dumps([dict(r) for r in result], default=str)

@app.route('/getorder/<int:id>', methods=['GET'])
def getOrder(id):
    result = db.execute("SELECT * FROM orders WHERE id = " + str(id))
    return json.dumps([dict(r) for r in result], default=str)

@app.route('/getorders', methods=['GET'])
def getOrders():
    result = db.execute("SELECT * FROM orders")
    return json.dumps([dict(r) for r in result], default=str)

@app.route('/editclient', methods=['PUT'])
def editClient():
    request_json = request.get_json()
    id = request_json.get('id')
    type = request_json.get('type')
    name = request_json.get('name')
    adress = request_json.get('adress')
    commentaru = request_json.get('commentaru')
    db.execute("UPDATE clients SET type = :type, name = :name, adress = :adress, commentaru = :commentaru WHERE id = :id",
            {"id":id,"clientId":clientId, "description":description, "adress":adress, "cost":cost})
    db.commit()
    return "ok"

@app.route('/editorder', methods=['PUT']) 
def editOrder():
    request_json = request.get_json()
    id = request_json.get('id')
    clientId = request_json.get('clientId')
    description = request_json.get('description')
    adress = request_json.get('adress')
    cost = request_json.get('cost')
    db.execute("UPDATE orders SET clientId = :clientId, description = :description, adress = :adress, cost = :cost WHERE id = :id", 
            {"id":id, "clientId":clientId, "description":description, "adress":adress, "cost":cost})
    db.commit()
    return "ok"

@app.route('/deleteclient/<int:id>', methods=['DELETE']) 
def deleteClient(id):
    db.execute("DELETE FROM clients WHERE id = (:id)", {"id":id})
    db.commit()
    return "ok"

@app.route('/deleteorder/<int:id>', methods=['DELETE']) 
def deleteOrder(id):
    db.execute("DELETE FROM orders WHERE id = (:id)", 
            {"id":id})
    db.commit() 
    return "ok"

@app.route('/getclientorders/<int:clientid>', methods=['GET'])
def getClientOrders(clientid):
    result = db.execute("SELECT c.*, o.* FROM clients c RIGHT JOIN order o ON c.id = o.clientId WHERE c.id = :clientid",
            {"clientid":clientid})
    return json.dumps([dict(r) for r in result], default=str)

@app.route('/getordersclient/<int:clientid>', methods=['GET'])
def getOrdersClient(clientid):
    result = db.execute("SELECT o.clientId, o.description, o.adress, o.cost, json_agg(json_build_object('id', c.id, 'type', c.type, 'name', c.name, 'adress', c.adress, 'commentaru', c.commentaru)) AS orders FROM clients o RIGHT JOIN orders c ON c.teamName = o.teamName WHERE o.id = :clientid GROUP BY o.teamName, o.homecity, o.sponsors",
            {"clientid":clientid})
    res = json.dumps([dict(r) for r in result], default=str)
    return res

if __name__ == "__main__":
    app.run(debug=True)