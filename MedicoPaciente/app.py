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

@app.route('/')
def index():
    return render_template('Index.html')

@app.route('/ingresarpaciente', methods=['POST'])
def guardar():
    if request.method=='POST':
        VnombreP= request.form['nombreP']
        VapellidoPP= request.form['apellidoPP']
        VapellidoPM= request.form['apellidoPM']
        VfechaNP= request.form['fechaNP']
        VEnfermedadesP= request.form['EnfermedadesP']
        ValergiasP= request.form['alergiasP']
        VantecedentesP= request.form['antecedentesP']

        CS= mysql.connection.cursor()
        CS.execute('insert into Pacientes (Nombres, ApellidoP, ApellidoM, Fecha_nac, Enfermedades_cronicas, Alergias,Antecedentes_familiares ) values (%s,%s,%s,%s,%s,%s,%s)', (VnombreP, VapellidoPP, VapellidoPM, VfechaNP, VEnfermedadesP, ValergiasP, VantecedentesP))        
        mysql.connection.commit()


    flash('Album Agregado Correctamente')    
    return redirect(url_for('RegPas'))

@app.route('/IAdmIMedica')
def IAdmIMedica():
    return render_template('IAdmIMedica.html')

@app.route('/RegPas')
def RegPas():
    return render_template('RegPas.html')


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
            return redirect(url_for('IAdmIMedica'))
        else: 
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('index'))
    elif Vrfc == 'RFCM1234':
        if Vrfc in usu and usu[Vrfc] == Vpassword:
            session['rfc'] = Vrfc
            return redirect(url_for('RegPas'))
        else: 
            flash('Usuario o contraseña incorrectos')
            return redirect(url_for('index'))
    else:
        flash('Usuario o contraseña incorrectos')
        return redirect(url_for('index'))

# -----------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=4000, debug=True)

