import re
from flask import Flask,render_template,request
from flask import render_template #creo que tambien es redirecicon
from flask import request #nos permite llamar
from flask import redirect, url_for # nos permite redireccionar
from flask import flash # permite enviar mensajes

from flaskext.mysql import MySQL


app= Flask(__name__)

#mysql conection
app.config['MYSQL_DATABASE_HOST']='biwmg7uycgr3iaunvbxg-mysql.services.clever-cloud.com'
app.config['MYSQL_DATABASE_USER']='uzkyivgvx6prvvsa'
app.config['MYSQL_DATABASE_PASSWORD']='DNn2ZUgi2oycdRXAtcOa'
app.config['MYSQL_DATABASE_DB']='biwmg7uycgr3iaunvbxg'
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

@app.route('/deleteUsuario')
def deleteUsuario():
   return render_template('/empleados/deleteUsu.html')

@app.route('/salir')
def salir():
   return redirect(url_for('login'))
   



@app.route('/info', methods=['POST'])
def info():
    name = request.form['name']
    password = request.form['password']
    
  
    if name!='' and password!='':
        #si no puede tomar losd atos de la base de datos xq pusiste cualquier cosa te da error
        #con el try te redirige
        try:
            nameBase = 'SELECT * FROM register WHERE name= %s ;'
            con = mysql.connect()
            cur = con.cursor()
            cur.execute(nameBase,name)
            data = cur.fetchall()
            c= data[0]
            
            
        except:
            flash('datos invalidos','error')
            return redirect(url_for('login'))
        else:        
            if name==c[1] and password==c[2]:
                return redirect(url_for('index'))      
    
    else:
        flash('datos invalidos','error')
        return redirect(url_for('login'))



@app.route('/nuevousu', methods=['POST'])
def nuevousu():
    if request.method == 'POST':       
        name = request.form['name']
        password = request.form['password']
        try:
            con = mysql.connect()
            cur = con.cursor()
            a =  'INSERT INTO register(name,password) VALUES (%s, %s);'
            b = (name, password)
            cur.execute(a, b)
            con.commit() 
            
        except:
            flash('Ya hay un usuario con ese nomrbe','error')
            return redirect(url_for('register'))
        else:
            flash('cuenta creada')
            return redirect(url_for('login'))

@app.route('/deleteUsu', methods=['POST'])
def deleteUsu():
    
    name = request.form['name']
    password = request.form['password']
    
  
    if name!='' and password!='':
        #si no puede tomar losd atos de la base de datos xq pusiste cualquier cosa te da error
        #con el try te redirige
        print('atr')
        try:
            print('try')
            con = mysql.connect()
            cur = con.cursor()
            cur.execute('SELECT * FROM register WHERE name = %s',name);
            
            data = cur.fetchall()
            c = data[0]
            
        except:
            
            flash('Invalid Data','error')
            return redirect(url_for('deleteUsuario'))
        
        else:
            if name==c[1] and password==c[2]:
                
                cur.execute('DELETE FROM register WHERE name =%s',name)
                con.commit()
                flash('Acount deleted')
                return redirect(url_for('login'))

    
    else:
        flash('Invalid Data','error')
        
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

        if  len(_fullname)<4 or len(_fullname)>25:
            flash('El nombre debe contener entre 4 y 25 caracteres','error')
            return redirect(url_for('index'))
        
        if any(chr.isdigit() for chr in _phone)!=True:
            flash('solo podes poner numeros','error')
            return redirect(url_for('index'))

        if not '@' in _email or not'.com' in _email:
            flash('email invalido','error')
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
