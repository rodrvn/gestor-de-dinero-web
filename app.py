from flask import Flask, render_template, url_for, request, redirect, flash
from models import db, Usuario, Ingresos, Gastos, Ahorro
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_123123sdg_SDgsdg-'

# conecta la base de datos y conecta la app
db.init_app(app)

# Instanciamos LoginManager para conectar con la app
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Creamos una funcion para manejar los usuarios logeados
@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))


# Homepage
@app.route("/")
def home():
    return redirect(url_for('tracker'))

# Register
@app.route("/registro", methods=['POST', 'GET'])
def registro():
    # if current_user.is_authenticated:
    #     flash(f'Ya estas logeado {current_user.nombre}! :)')
    #     return redirect(url_for('tracker'))
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        # Hacemos la confirmación de creación de usuario
        if Usuario.query.filter_by(correo=email).first():
            flash('Este correo ya existe uwu', category='error')
        elif len(email) < 4:
            flash('Tu correo debe ser mayor a 4 caracteres', category='error')
        elif len(nombre) < 4:
            flash('Tu nombre debe ser mayor a 4 caracteres', category='error')
        elif len(apellido) < 4:
            flash('Tu apellido debe ser mayor a 4 caracteres', category='error')
        elif len(password1) < 3:
            flash('Tu contraseña debe ser mayor a 3 caracteres', category='error')
        elif password1 != password2:
            flash('Las contraseñas no coinciden', category='error')
        else:
            # Hasheamos la contraseña para mayor seguridad
            password = generate_password_hash(password1, method='sha256')
            user = Usuario(nombre=nombre, apellido=apellido, correo=email, password=password)
            # Agregamos a la db
            db.session.add(user)
            # Y confirmamos
            db.session.commit()
            # Recuerda que el usuario esta logeado
            login_user(user, remember=True)
            if user.is_authenticated:
                ingresos = Ingresos(id_usuario=current_user.id, razon_ingreso='Nombre del ingreso')
                gastos = Gastos(id_usuario=current_user.id, razon_gasto='Nombre del gasto')
                ahorros = Ahorro(id_usuario=current_user.id, razon_ahorro='Nombre del ahorro')
                db.session.add(ingresos)
                db.session.add(gastos)
                db.session.add(ahorros)
                db.session.commit()


            flash('Usuario creado!', category='success')
            return redirect(url_for("tracker"))
    return render_template("registro.html")

#Ruta para logearte
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Ya estas logeado {current_user.nombre}! :)')
        return redirect(url_for('home'))
    if request.method == 'POST':
        correo = request.form.get("correo_user")
        password = request.form.get("password")
        user = Usuario.query.filter_by(correo=correo).first()
        if user and user.confirmar_contraseña(password):
            flash(f'Bienvenidx de vuelta {user.nombre} :)', category='succes')
            # Recuerda que el usuario esta logeado
            login_user(user, remember=True)
            print(current_user)
            return redirect(url_for('tracker'))  
        else:
            flash('Correo o contraseña incorrecta', category='error')
    return render_template('login.html')

# Desconectar sesion
@app.route('/logout', methods = ['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Pagina inicial del tracker
@app.route("/tracker", methods=['GET'])
@login_required
def tracker():

    # Trae los datos del usuario segun id
    usuario = Usuario.query.get(current_user.id)
    
    #Trae los datos segun el id
    ingresos = Ingresos.query.filter_by(id_usuario=current_user.id).all()
    gastos = Gastos.query.filter_by(id_usuario=current_user.id).all()
    ahorros = Ahorro.query.filter_by(id_usuario=current_user.id).all()

    #Para traer solo los ultimos 5 gastos
    ultimos_gastos = Gastos.query.filter_by(id_usuario=current_user.id).order_by(Gastos.fecha.desc()).limit(5).all()
    #Para traer solo los ultimos 5 ingresos
    ultimos_ingresos = Ingresos.query.filter_by(id_usuario=current_user.id).order_by(Ingresos.fecha.desc()).limit(5).all()

    #Trae los datos de la database sumados y filtrados por la id
  
    gastos_totales = db.session.query(db.func.sum(Gastos.gasto_reciente)).filter(Gastos.id_usuario==current_user.id).scalar()
    ahorros = db.session.query(db.func.sum(Ahorro.monto_ahorro)).filter(Ahorro.id_usuario==current_user.id).scalar()
    ingresos_totales = db.session.query(db.func.sum(Ingresos.ingreso_reciente)).filter(Ingresos.id_usuario==current_user.id).scalar()
    
    #Hace el calculo del saldo total
    if ingresos_totales == None:
        ingresos_totales = 0
    if gastos_totales == None:
        gastos_totales = 0
    if ahorros == None:
        ahorros = 0
    saldo_total = ((ingresos_totales) - (gastos_totales))
    

    return render_template('tracker.html', usuario=usuario, ingresos=ingresos, gastos=gastos, ultimos_gastos=ultimos_gastos, ahorros=ahorros, saldo_total=saldo_total, gastos_totales=gastos_totales, ultimos_ingresos=ultimos_ingresos, ingresos_totales=ingresos_totales)




#### Pagina Gastos ####

@app.route("/tracker/gastos/", methods=['GET'])
@login_required
def ver_gastos():

    # Trae los datos del usuario segun id
    usuario = Usuario.query.get(current_user.id)
    
    #Trae los datos de gastos segun el id
    gastos = Gastos.query.filter_by(id_usuario=current_user.id).all()

    #Trae los datos de la database sumados y filtrados por la id
    gastos_totales = db.session.query(db.func.sum(Gastos.gasto_reciente)).filter(Gastos.id_usuario==current_user.id).scalar()
    
    if gastos_totales == None:
        gastos_totales = 0
    

    return render_template('all_gastos.html', usuario=usuario, gastos=gastos,gastos_totales=gastos_totales)

# Agregar gastos
@app.route("/agregar_gasto/", methods=["POST"])
@login_required
def agregar_gastos():
    gasto_reciente = request.form['gasto_reciente']
    razon_gasto = request.form['razon_gasto']
    # fecha_gasto = request.form['fecha_gasto']

    gasto = Gastos(id_usuario=current_user.id, gasto_reciente=gasto_reciente, razon_gasto=razon_gasto)
    db.session.add(gasto)
    db.session.commit()
    return redirect(url_for('tracker'))


# Editar gastos
@app.route("/tracker/editar-gasto/<id_gasto>", methods=['GET', 'POST'])
@login_required
def editar_gasto(id_gasto):

    usuario = Usuario.query.get(current_user.id)

    gasto_editar = Gastos.query.filter_by(id_usuario=current_user.id, id=id_gasto).first()

    #Si el metodo es Post actualiza
    if request.method == 'POST':
        gasto_editar.razon_gasto = request.form["razon_gasto"]
        gasto_editar.gasto_reciente = request.form["gasto_reciente"]
        gasto_editar.fecha = request.form["fecha_gasto"]

        db.session.commit()
        return redirect(url_for("tracker"))
    #Si es GET, nos da los datos que necesitamos
    
    return render_template('edit_gastos.html', gasto_editar=gasto_editar, usuario=usuario)


# Eliminar gasto
@app.route("/eliminar_g/<id_gasto>", methods=['POST','GET'])
@login_required
def eliminar_gasto(id_gasto):

    gasto_eliminar = Gastos.query.filter_by(id_usuario=current_user.id, id=id_gasto).first()

    db.session.delete(gasto_eliminar)
    db.session.commit()

    return redirect(url_for('tracker'))


#### Termina Pagina Gastos ####




#### Pagina Ingresos ####

@app.route("/tracker/ingresos/", methods=['GET'])
@login_required
def ver_ingresos():

    # Trae los datos del usuario segun id
    usuario = Usuario.query.get(current_user.id)
    
    #Trae los datos de gastos segun el id
    ingresos = Ingresos.query.filter_by(id_usuario=current_user.id).all()

    #Trae los datos de la database sumados y filtrados por la id
    ingresos_totales = db.session.query(db.func.sum(Ingresos.ingreso_reciente)).filter(Ingresos.id_usuario==current_user.id).scalar()
    if ingresos_totales == None:
        ingresos_totales = 0
    return render_template('all_ingresos.html', usuario=usuario, ingresos=ingresos,ingresos_totales=ingresos_totales)

# Agregar ingresos
@app.route("/agregar_ingreso/", methods=["POST"])
@login_required
def agregar_ingreso():
    ingreso_reciente = request.form['ingreso_reciente']
    razon_ingreso = request.form['razon_ingreso']
    # ingreso_gasto = request.form['fecha_ingreso']

    ingreso = Ingresos(id_usuario=current_user.id, ingreso_reciente=ingreso_reciente, razon_ingreso=razon_ingreso)
    db.session.add(ingreso)
    db.session.commit()
    return redirect(url_for('tracker'))


# Editar ingresos
@app.route("/tracker/editar-ingreso/<id_ingreso>", methods=['GET', 'POST'])
@login_required
def editar_ingreso(id_ingreso):

    usuario = Usuario.query.get(current_user.id)
    ingreso_editar = Ingresos.query.filter_by(id_usuario=current_user.id, id=id_ingreso).first()
    
    #Si el metodo es Post actualiza los datos
    if request.method == 'POST':
        ingreso_editar.razon_ingreso = request.form["razon_ingreso"]
        ingreso_editar.ingreso_reciente = request.form["ingreso_reciente"]
        ingreso_editar.fecha = request.form["fecha_ingreso"]

        db.session.commit()
        return redirect(url_for("tracker"))
    
    return render_template('edit_ingresos.html', ingreso_editar=ingreso_editar)


# Eliminar ingreso
@app.route("/eliminar_i/<id_ingreso>", methods=['GET','POST'])
@login_required
def eliminar_ingreso(id_ingreso):

    ingreso_eliminar = Ingresos.query.filter_by(id_usuario=current_user.id, id=id_ingreso).first()

    db.session.delete(ingreso_eliminar)
    db.session.commit()

    return redirect(url_for('tracker'))

#### Termina Pagina Ingresos ####





#### Pagina Ahorros ####

@app.route("/tracker/ahorros/", methods=['GET', 'POST'])
@login_required
def ver_ahorros():

    # Trae los datos del usuario segun id
    usuario = Usuario.query.get(current_user.id)
    
    #Trae los datos de gastos segun el id
    ahorros = Ahorro.query.filter_by(id_usuario=current_user.id).all()

    #Trae los datos de la database sumados y filtrados por la id
    ahorros_totales = db.session.query(db.func.sum(Ahorro.monto_ahorro)).filter(Ahorro.id_usuario==current_user.id).scalar()
    if ahorros_totales == None:
        ahorros_totales = 0
    

    return render_template('all_ahorros.html', ahorros=ahorros, ahorros_totales=ahorros_totales)


# Agregar ahorros
@app.route("/agregar_ahorro/", methods=["POST"])
@login_required
def agregar_ahorro():
    monto_ahorro = request.form['monto_ahorro']
    razon_ahorro = request.form['razon_ahorro']
    # ingreso_gasto = request.form['fecha_ingreso']

    ahorro = Ahorro(id_usuario=current_user.id, monto_ahorro=monto_ahorro, razon_ahorro=razon_ahorro)
    db.session.add(ahorro)
    db.session.commit()
    return redirect(url_for('ver_ahorros'))

# Eliminar Ahorro
@app.route("/eliminar_a/<id_ahorro>", methods=['GET','POST'])
@login_required
def eliminar_ahorro(id_ahorro):

    ahorro_eliminar = Ahorro.query.filter_by(id_usuario=current_user.id, id=id_ahorro).first()

    db.session.delete(ahorro_eliminar)
    db.session.commit()

    return redirect(url_for('ver_ahorros'))

# Editar ahorro
@app.route("/tracker/editar-ahorro/<id_ahorro>", methods=['GET', 'POST'])
@login_required
def editar_ahorro(id_ahorro):

    usuario = Usuario.query.get(current_user.id)

    ahorro_editar = Ahorro.query.filter_by(id_usuario=current_user.id, id=id_ahorro).first()

    #Si el metodo es Post actualiza
    if request.method == 'POST':
        ahorro_editar.razon_ahorro = request.form["razon_ahorro"]
        ahorro_editar.monto_ahorro = request.form["monto_ahorro"]
        ahorro_editar.fecha = request.form["fecha_ahorro"]

        db.session.commit()
        return redirect(url_for("ver_ahorros"))
    #Si es GET, nos da los datos que necesitamos
    
    return render_template('edit_ahorro.html', ahorro_editar=ahorro_editar)

#### Termina Pagina Ahorros ####




# BREAKPOINT #
if __name__ == "__main__":
    app.run(debug=True, port='9000')