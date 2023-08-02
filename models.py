from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime

db = SQLAlchemy()

#Fecha actual en string
fecha_string = datetime.strftime(datetime.now(), '%b %d, %Y')


# MODELS #

#Para el usuario
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70))
    apellido = db.Column(db.String(70))
    correo = db.Column(db.String(70))
    password = db.Column(db.String(400))
    rol = db.Column(db.String(15), default='user')

    ingresos = db.relationship('Ingresos', backref = 'usuario')
    gastos = db.relationship('Gastos', backref = 'usuario')
    ahorro = db.relationship('Ahorro', backref = 'usuario')


    # Funcion que te permite confirmar contraseñá hasheada
    def confirmar_contraseña(self, password):
        return check_password_hash(self.password, password)

#Para los ingresos
class Ingresos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # Creador de la receta
    ingreso_reciente = db.Column(db.Integer, default=0)
    razon_ingreso = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)



#Para los gastos
class Gastos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # Creador de la receta
    gasto_reciente = db.Column(db.Integer, default=0)
    razon_gasto = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)


#Para ahorro
class Ahorro(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False) # Creador de la receta
    monto_ahorro = db.Column(db.Integer, default=0)
    razon_ahorro = db.Column(db.String(50))
    fecha = db.Column(db.String, default=fecha_string)
