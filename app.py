from flask import Flask

from flask import render_template #cuando el usuario hace una poeticion devuelve los templates
from flaskext.mysql import MySQL 

app= Flask(__name__)
#asdasdasdasdasfsdf
mysql= MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']='root'
app.config['MYSQL_DATABASE_DB']='empleados'
mysql.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
