from models import db, Usuario, Ingresos, Gastos, Ahorro
from flask import Flask

app = Flask('app')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Inicializa

db.init_app(app)


# Crea la base de datos

with app.app_context():
    db.create_all()


########################

with app.app_context():
    usuario = Usuario(nombre='Rodrigo', apellido='Vallejos', correo='rorro@gmai.com', password='123123')
    ingreso = Ingresos(id_usuario=1, ingreso_reciente=60000, razon_ingreso='brownies')
    gasto = Gastos(id_usuario=1, gasto_reciente=2000, razon_gasto='empanada')
    ahorro = Ahorro(id_usuario=1, monto_ahorro=200000, razon_ahorro='viaje') 

    db.session.add(usuario)
    db.session.add(ingreso)
    db.session.add(gasto)
    db.session.add(ahorro)

    db.session.commit()
    