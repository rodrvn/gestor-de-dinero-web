from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from models import db, Usuario, Ingresos, Gastos, Ahorro

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# conecta la base de datos y conecta la app
db.init_app(app)

@app.route("/")
def index():
    return 'poner /id_usuario :)'

@app.route("/<id_usuario>")
def tracker(id_usuario):

    # Trae los datos del usuario segun id
    usuario = Usuario.query.get(id_usuario)
    
    #Trae los datos segun el id
    ingresos = Ingresos.query.filter_by(id_usuario=id_usuario).all()
    gastos = Gastos.query.filter_by(id_usuario=id_usuario).all()
    ahorros = Ahorro.query.filter_by(id_usuario=id_usuario).all()

    #Trae los datos de la database sumados y filtrados por la id
  
    ingresos_totales = db.session.query(db.func.sum(Ingresos.ingreso_reciente)).filter(Ingresos.id_usuario==id_usuario).scalar()
    gastos_totales = db.session.query(db.func.sum(Gastos.gasto_reciente)).filter(Gastos.id_usuario==id_usuario).scalar()
    ahorros = db.session.query(db.func.sum(Ahorro.monto_ahorro)).filter(Ahorro.id_usuario==id_usuario).scalar()

    #Hace el calculo del saldo total
    saldo_total = (ingresos_totales - gastos_totales)
    

    return render_template('base.html', usuario=usuario, ingresos=ingresos, gastos=gastos, ahorros=ahorros, saldo_total=saldo_total, gastos_totales=gastos_totales)





# BREAKPOINT #
if __name__ == "__main__":
    app.run(debug=True)