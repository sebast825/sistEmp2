from flask import Flask,render_template,request


from flaskext.mysql import MySQL


app= Flask(__name__)


app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='flaskcontacts'

mysql= MySQL(app) #conecta pytohn con la base de datos

@app.route('/')
def index():
    return render_template('empleados/index.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        _fullname = request.form['fullname']
        _phone = request.form['phone']
        _email = request.form['email']
        

        conn = mysql.connect()
        cursor = conn.cursor()
        A = 'INSERT INTO contacts (fullname,phone,email) VALUES (%s, %s, %s);'
        B = (_fullname, _phone, _email)
        cursor.execute(A, B)
        conn.commit()
        return "recived"



if __name__ == "__main__":
    app.run(debug=True)
