import re
from flask import Flask,render_template,request
from flask import render_template #creo que tambien es redirecicon
from flask import request #nos permite llamar
from flask import redirect, url_for # nos permite redireccionar
from flask import flash # permite enviar mensajes

from flaskext.mysql import MySQL


app= Flask(__name__)

#mysql conection
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='flaskcontacts'
mysql= MySQL(app) #conecta pytohn con la base de datos


#settings, donde guardar datos para el servidor
app.secret_key = "mysecretkey" #se esta usando para el mensaje flash x ahora

# PRIMERA PARTE PARA LAS CUENTAS
@app.route('/')
def login():
   return render_template('empleados/login.html')

@app.route('/register')
def register():
   return render_template('/empleados/register.html')

@app.route('/sincuenta')
def sincuenta():
   return render_template('a.html')

@app.route('/salir')
def salir():
   return redirect(url_for('login'))
   



@app.route('/info', methods=['POST'])
def info():
    name = request.form['name']
    password = request.form['password']
    
  
    if name!='' and password!='':

        nameBase = 'SELECT * FROM register WHERE name= %s ;'
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(nameBase,name)
        data = cur.fetchall()
        c= data[0]
      # if password == resultado:
        
        if name==c[1] and password==c[2]:
            return redirect(url_for('index'))
      
    
    else:
        flash('datos invalidos','error')
        return redirect(url_for('login'))

#mirar el sincuenta

  



@app.route('/nuevousu', methods=['POST'])
def nuevousu():
    if request.method == 'POST':       
      name = request.form['name']
      password = request.form['password']

      con = mysql.connect()
      cur = con.cursor()
      a =  'INSERT INTO register(name,password) VALUES (%s, %s);'
      b = (name, password)
      cur.execute(a, b)
      con.commit() 
      return redirect(url_for('login'))

@app.route('/deleteusu/<string:id>')
def deleteusu(id):

   con = mysql.connect()
   cur = con.cursor() 
   cur.execute('DELETE FROM register WHERE id = {} '.format(id))
   con.commit()
   flash('Cuenta eliminada correctamente')           
   return redirect(url_for('login'))



##
##
##
##
##




@app.route('/index')
def index():
    cur = mysql.connect()
    cursor = cur.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall() #devuelve los datos
    
    #redirige y la parte de contacts = data devuelve la info de la base de datos
    #como devuelve una tupla en el index hay que llamar valor por valor
    #para ver la tupla pone print(data), actualizas la pagina y te aparece en terminal
    return render_template('empleados/index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        _fullname = request.form['fullname'] #le pones el name del index
        _phone = request.form['phone']
        _email = request.form['email']
        
        if _fullname=='' or _phone=='' or _email=='':
            flash('Falta llenar algun dato','error')
            return redirect(url_for('index'))

        conn = mysql.connect()
        cursor = conn.cursor()
        A = 'INSERT INTO contacts (fullname,phone,email) VALUES (%s, %s, %s);'
        B = (_fullname, _phone, _email)
        cursor.execute(A, B)
        conn.commit()
        flash ("contaco agregado correctamente") # envia un mensaje
        return redirect(url_for('index')) #redirige, le marcas la url, y index es el nombre de la ruta(arriba)

#siempre que reciba la ruta delete con lo del string le decis que si o si tiene que tener un numero
@app.route('/delete/<string:id>') 
def delete_contact(id):
    cur = mysql.connect()
    cursor = cur.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {} '.format(id))
    cur.commit()
    flash('contacto removido correctamente')
    return redirect(url_for('index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    cur = mysql.connect()
    cursor = cur.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = {} '.format(id))
    data = cursor.fetchall()
    print(data[0]) #sin el indice 0 devuelve una lista dentro de una lista
    return render_template('empleados/edit.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method=='POST':
        fullname = request.form['fullname'] 
        phone = request.form['phone']
        email = request.form['email']

        # if email.value().indexOf()=='@':
        #     flash('falta el @')
        #     return redirect(url_for('index'))

        cur = mysql.connect()
        cursor = cur.cursor()
        cursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        cur.commit()

        flash ('contacto actualizado correctamente')
        return redirect(url_for('index'))
    
   
if __name__ == "__main__":
    app.run(debug=True)
