from flask import Flask, jsonify, request, make_response
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Alonso.99",
    database='spotify'
)


app = Flask(__name__)


@app.route('/usuarios')
def getusers():
    mycursor = db.cursor(dictionary=True)
    mycursor.execute('select u.id , u.nombre, tu.nombre as tipo from usuarios as u inner join tipos_de_usuarios as tu on u.tipo = tu.id')
    result = mycursor.fetchall()
    mycursor.close()
    return jsonify({'users': result})


@app.route('/usuarios/<int:user_id>')
def getuser(user_id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select u.id , u.nombre, tu.nombre as tipo from usuarios as u inner join tipos_de_usuarios as tu on u.tipo = tu.id where u.id ={user_id}")
    userfound = mycursor.fetchall()
    mycursor.close()
    if len(userfound) > 0:
        return jsonify(userfound[0])
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/usuarios', methods=['POST'])
def adduser():
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"INSERT INTO usuarios (nombre, tipo) VALUES ('{request.json['nombre']}',{request.json['tipo']})")
    db.commit()
    response = mycursor.rowcount
    mycursor.close()
    if response > 0:
        return make_response(jsonify({'message': 'Usuario agreagado correctamente'}), 201)
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/usuarios/<int:user_id>', methods=['DELETE'])
def deleteuser(user_id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"DELETE FROM usuarios where id = {user_id}")
    db.commit()
    response = mycursor.rowcount
    mycursor.close()
    if response > 0:
        return jsonify({'message': 'usuario eliminado'})
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/usuarios/<int:user_id>', methods=['PUT'])
def edituser(user_id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"UPDATE usuarios set nombre = '{request.json['nombre']}',tipo = {request.json['tipo']} where id ={user_id}")
    db.commit()
    response = mycursor.rowcount
    mycursor.close()
    if response > 0:
        return jsonify({'message': 'Usuario agreagado correctamente'})
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/pagos', methods=['POST'])
def addpayment():
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select count(*) as c from pagos where usuario = {request.json['usuario']}  group by usuario")
    counter = mycursor.fetchall()
    if len(counter) == 0:
        counter = 0
    else:
        counter = counter[0]['c']
    mycursor.execute(f"INSERT INTO pagos (usuario,id,cantidad, fecha) VALUES ({request.json['usuario']},{counter + 1},{request.json['cantidad']},'{request.json['fecha']}')")
    db.commit()
    response = mycursor.rowcount
    mycursor.close()
    if response > 0:
        return make_response(jsonify({'message': 'pago agreagado correctamente'}), 201)
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/pagos')
def getpayments():
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select p.id , u.nombre, p.cantidad, p.fecha from usuarios as u inner join pagos as p on u.id = p.usuario")
    userfound = mycursor.fetchall()
    mycursor.close()
    if len(userfound) > 0:
        return jsonify(userfound)
    return jsonify({'message': 'pagos no encontrados'})


@app.route('/pagos/<int:user_id>')
def getpayment(user_id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select p.id , u.nombre, p.cantidad, p.fecha from usuarios as u inner join pagos as p on u.id = p.usuario where u.id ={user_id}")
    userfound = mycursor.fetchall()
    mycursor.close()
    if len(userfound) > 0:
        return jsonify(userfound)
    return jsonify({'message': 'usuario no encontrado'})


@app.route('/pagos/<int:user_id>/<int:id>', methods=['DELETE'])
def deletepayment(user_id, id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"DELETE FROM pagos where usuario = {user_id} and id = {id}")
    db.commit()
    response = mycursor.rowcount
    mycursor.close()
    if response > 0:
        return jsonify({'message': 'pago eliminado'})
    return jsonify({'message': 'pago no encontrado'})


@app.route('/estados')
def getestados():
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select u.id , u.nombre, ea.meses_pagados from usuarios as u inner join estado_actual as ea on u.id = ea.usuario")
    userfound = mycursor.fetchall()
    mycursor.close()
    if len(userfound) > 0:
        return jsonify(userfound)
    return jsonify({'message': 'usuarios no encontrados'})


@app.route('/estados/<int:user_id>')
def getestado(user_id):
    mycursor = db.cursor(dictionary=True)
    mycursor.execute(f"select u.id , u.nombre, ea.meses_pagados from usuarios as u inner join estado_actual as ea on u.id = ea.usuario where u.id ={user_id}")
    userfound = mycursor.fetchall()
    mycursor.close()
    if len(userfound) > 0:
        return jsonify(userfound)
    return jsonify({'message': 'no se pudo encontrar los pagos de este usiario'})


if __name__ == '__main__':
    app.run(debug=True)


