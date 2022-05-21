from crypt import methods
from email.message import Message
import os
import logging
from json import dumps
from urllib import response

from flask import Flask, g, Response, request
from neo4j import GraphDatabase, basic_auth

app = Flask(__name__, static_url_path = "/static/")

# Try to load database connection info from environment
url = os.getenv("NEO4J_URI", "bolt://localhost:7687")
username = os.getenv("NEO4J_USER", "neo4j")
password = os.getenv("NEO4J_PASSWORD", "1234")
neo4jVersion = os.getenv("NEO4J_VERSION", "4")
database = os.getenv("NEO4J_DATABASE", "taller5")
port = os.getenv("PORT", 8080)

# Create a database driver instance
driver = GraphDatabase.driver(url, auth = basic_auth(username, password))

# Connect to database only once and store session in current context
def get_db():
    if not hasattr(g, "neo4j_db"):
        if neo4jVersion.startswith("4"):
            g.neo4j_db = driver.session(database = database)
        else:
            g.neo4j_db = driver.session()
    return g.neo4j_db

# Close database connection when application context ends
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "neo4j_db"):
        g.neo4j_db.close()

@app.route('/')
def home():
    return "hey"

#crea un comprador
@app.route("/comprador", methods=["POST"])
def create():
    nombre=request.json['name']
    message="Nodo"
    db = get_db()
    summary = db.run("create (c: comprador {nombre:$nombre}) return a",nombre=nombre)
    db.close()

    return  "exito"

#crea un producto
@app.route("/producto", methods=["POST"])
def create():
    nombre=request.json['name']
    message="Nodo"
    db = get_db()
    summary = db.run("create (p: producto {nombre:$nombre}) return a",nombre=nombre)
    db.close()

    return  "exito"

#crea un vendedor
@app.route("/vendedor", methods=["POST"])
def create():
    nombre=request.json['name']
    message="Nodo"
    db = get_db()
    summary = db.run("create (V: vemdedor {nombre:$nombre}) return a",nombre=nombre)
    db.close()

    return  "exito"

#Relacion de vender un producto 
@app.route("/vende", methods[POST])
def vende():
    db = get_db()
    producto = request.json['producto']
    Vendedor = request.json['vendedor']
    Categoria = request.json['categoria']
    db.run("MATCH (V: vendedor {nombre = vendedor},{p: producto {nombre: producto, categoria: $categoria} CREATE (V)-[VENDE]->(p)",     producto=producto, vendedor=vendedor, Categoria=Categoria )
    return  "exito"

#relacion de comprar un producto
@app.route("/compra", methods[POST])
def compra():
    db = get_db()
    comprador = request.json['comprador']
    producto = request.json['producto']
    db.run("MATCH (c: comprador {nombre: $comprador}),(p: producto {nombre: $producto}) CREATE (c)-[COMPRA]->(p) ", producto=producto,comprador=comprador)
    return  "exito"

#Recomendar producto
@app.route("/compra", methods[POST])
def recomienda():
    db = get_db()
    comprador = request.json['comprador']
    producto = request.json['producto']
    puntuacion = request.json['puntuacio']
    db.run("MATCH (c: comprador {nombre: $comprador}),(p: producto {nombre: $producto}) CREATE (c)-[RECOMIENDA {puntuacion: $puntuacion}]->(p) ", producto=producto,comprador=comprador,puntuacion=puntuacion)
    return  "exito"

#Top 5
@app.route("/Top5", methods=['GET'])
def Top5():
    db = get_db()
    result = db.run("MATCH (c:Comprador)-[a:COMPRA]->(p:Producto)-[r:RECOMIENDA]->(p) RETURN b.nombre AS nombre, AVG(r.calificacion) AS promedio, count(c) as compras ORDER BY compras DESC, promedio DESC LIMIT 5")
    return Response(dumps(result.data()),  mimetype='application/json')

#Sugerencia Top 3


@app.route("/lanzar", methods=["POST"])
def create2():
    return "ok"

if __name__ == '__main__':
    logging.info('Running on port %d, database is at %s', port, url)
    app.run(port=port)