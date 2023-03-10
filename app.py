from flask import Flask, render_template, url_for, request, redirect
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

@app.route("/tracker/<id_usuario>", methods=['GET'])
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
    
    saldo_total = ((ingresos_totales) - (gastos_totales))
    
    print(saldo_total)
    

    return render_template('base.html', usuario=usuario, ingresos=ingresos, gastos=gastos, ahorros=ahorros, saldo_total=saldo_total, gastos_totales=gastos_totales)

@app.route("/agregar_ingreso/<id_usuario>")
def agregar_ingreso(id_usuario):

    return 'enviado'

@app.route("/agregar_gasto/<id_usuario>", methods=["POST", "GET"])
def agregar_gastos(id_usuario):
    gasto_reciente = request.form['gasto_reciente']
    razon_gasto = request.form['razon_gasto']
    # fecha_gasto = request.form['fecha_gasto']

    gasto = Gastos(id_usuario=id_usuario, gasto_reciente=gasto_reciente, razon_gasto=razon_gasto)
    db.session.add(gasto)
    db.session.commit()
    return redirect(url_for('tracker', id_usuario=id_usuario))

@app.route("/editar/<id_usuario>")
def editar(id_usuario):
    return 'editar'

@app.route("/eliminar/<id_usuario>")
def borrar(id_usuario):
    return 'borrar'
    

    

    




# BREAKPOINT #
if __name__ == "__main__":
    app.run(debug=True)