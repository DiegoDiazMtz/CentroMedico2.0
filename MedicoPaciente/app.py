from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL

# Inicialización del servidor Flask
app = Flask(__name__, static_folder='public', template_folder='templates')
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "consultorio"

app.secret_key = 'mysecretkey'

mysql = MySQL(app)

# -----------------------------------------------------------------------------

@app.route('/ListaDr')
def ListaDr():
    return render_template('ListaDr.html')

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/ingresar', methods=['POST'])
def ingresar():
    if request.method == 'POST':
        Vrfc = request.form['rfc']
        Vpassword = request.form['password']

    usu = {
    'RFCA1234': 'Admin1',
    'RFCM1234': 'Medico1'
    }

    if Vrfc == 'RFCA1234':
        if Vrfc in usu and usu[Vrfc] == Vpassword:
            session['rfc'] = Vrfc
            return redirect(url_for('ListaDr'))
        else: 
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('index'))
    elif Vrfc == 'RFCM1234':
        if Vrfc in usu and usu[Vrfc] == Vpassword:
            session['rfc'] = Vrfc
            return redirect(url_for('ListaDr'))
        else: 
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('index'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('index'))

@app.route('/submenu', methods=['POST'])
def submenu():
    if request.method == 'POST':
        menu_value = request.form['menu']
        # Aquí puedes realizar las acciones correspondientes según el valor del menú seleccionado
        if menu_value == 'AdministracionMedicos':
            # Lógica para la opción "Administración Médica"
            return  render_template('Adminmed.html')
        elif menu_value == 'RegPas':
            # Lógica para la opción "Registro Paciente"
            return render_template("RegPas.html")
        elif menu_value == 'Diagnostico':
            # Lógica para la opción "Diagnóstico"
            return render_template('ExpyDiag.html')
        elif menu_value == 'ConsultarPaciente':
            # Lógica para la opción "Consultar Paciente"
            return render_template("ConsultaPacientes.html")
        elif menu_value == 'AdministracionConsultas':
            # Lógica para la opción "Administración Consultas"
            return render_template("ConPas.html")
        else:
            return "Opción inválida"
    else:
        return "Método no permitido"

@app.route('/agregarMed', methods=['POST'])
def agregarMed():
    if request.method == 'POST':
        Vrfc = request.form['RFC']
        Vnomb = request.form['nombre']
        Vapp = request.form['apellidoP']
        Vapm = request.form['apellidoM']
        Vrol = request.form['rol']
        
        # Establecer conexión con la base de datos
        conn = mysql.connector.connect('consultorio')
        cursor = conn.cursor()

        # Consulta SQL para insertar los datos en la tabla médico
        query = "INSERT INTO medico (RFC, nombre, apellidoP, apellidoM, rol) VALUES (%s, %s, %s, %s, %s)"
        values = (Vrfc, Vnomb, Vapp, Vapm, Vrol)

        try:
            # Ejecutar la consulta SQL
            cursor.execute(query, values)

            # Confirmar los cambios en la base de datos
            conn.commit()

            # Cerrar la conexión con la base de datos
            cursor.close()
            conn.close()

            # Redirigir o retornar una respuesta según lo necesites
            
            flash('Medico agregado correctamente')
            return render_template('index')
        except mysql.connector.Error as error:
            # Manejo de errores en caso de falla en la inserción
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('Adminmed.html'))
        
        

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=4000, debug=True)

