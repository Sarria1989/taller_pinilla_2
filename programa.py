from flask import Flask, render_template, redirect,request, session
from flask_mysqldb import MySQL, MySQLdb
import hashlib

programa = Flask(__name__)
bdd = MySQL()

programa.config['MYSQL_DATABASE_HOST']='localhost'
programa.config['MYSQL_DATABASE_PORT']= 3306
programa.config['MYSQL_DATABASE_USER']='root'
programa.config['MYSQL_DATABASE_PASSWORD']=''
programa.config['MYSQL_DATABASE_DB']='turismo'

bdd.init_app(programa)

@programa.route('/') #Ruta Principal
def inicio():
    return render_template("login.html")

@programa.route('/login', methods = ['POST']) 
def login():
    
    documento = request.form['txtDocumento']
    clave = request.form['txtClave']
    cifrada = hashlib.sha512(clave.encode("utf-8")).hexdigest()
    sql = f"SELECT operadores WHERE documento='{documento}' AND clave='{cifrada}' AND estado='ACTIVO'"
    con = bdd.connect()
    cur = con.cursor()
    cur.execute(sql)
    resultado = cur.fetchall()
    con.commit()
    
    if len(resultado)==0:
        return render_template("login.html", msg="Error al Iniciar sesion, Datos Incorrectos")
    else:
        session['loginCorrecto'] = True
        session['nombreUsuario'] = resultado[0][0]
        return redirect("/agregarsitio.html")
    


if __name__ == '__main__':
    programa.run(debug=True)
