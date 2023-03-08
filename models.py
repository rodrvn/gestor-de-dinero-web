from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#Fecha actual en string
fecha_string = datetime.strftime(datetime.now(), '%b %d, %Y')


# MODELS #

#Para el usuario
class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70))
    apellido = db.Column(db.String(70))
    correo = db.Column(db.String(70))
    password = db.Column(db.String(30))

#Para los ingresos
class Ingresos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.ForeignKey('usuario.id_usuario'))
    ingreso_reciente = db.Column(db.Integer)
    razon_ingreso = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)


#Para los gastos
class Gastos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    gasto_reciente = db.Column(db.Integer)
    razon_gasto = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)

#Para ahorro
class Ahorro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))
    monto_ahorro = db.Column(db.Integer)
    razon_ahorro = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)