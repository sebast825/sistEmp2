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


@app.route('/')
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
    return id

if __name__ == "__main__":
    app.run(debug=True)
