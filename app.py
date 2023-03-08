from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    
    fullname = 'Pingunecia Del Rio'

    saldo_total = 50000

    gastos_total = 20000

    ahorro = 400500

    razon_gasto = 'cena choripan'

    gastos_recientes = 12000

    ingresos_recientes = 60000

    razon_ingreso = 'venta chat.gpt'

    banco_efectivo= 'efectivo' #Variable para saber si el ingreso/egreso se hizo a traves de un banco o a traves de efectivo

    fecha = '7/marzo/2023'


    
    

    return render_template('base.html', fullname=fullname, saldo_total=saldo_total, gastos_total=gastos_total, ahorro=ahorro, gastos_recientes=gastos_recientes, ingresos_recientes=ingresos_recientes, fecha=fecha, razon_ingreso=razon_ingreso, razon_gasto=razon_gasto, banco_efectivo=banco_efectivo)





# BREAKPOINT #
if __name__ == "__main__":
    app.run(debug=True)