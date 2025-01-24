import MySQLdb
from flask import Flask, render_template, request, session
from flask_mysqldb import Mysql, MySQL
import mysql.connector
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='12345'
app.config['MYSQL_DB']='job_portal2'

mysql=MySQL(app)


@app.route('/submit',methods=['GET','POST'])
def register():
   if request.method=='POST':
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      email = request.form['email']
      password = request.form['password']
      role = request.form['role']
      cur = mysql.connection.cursor()
      cur.execute('INSERT into user(first_name,last_name,email_id,passwords,role)VALUES(%s,%s,%s,%s,%s)',
                  (first_name, last_name, email, password, role))
      mysql.connection.commit()
      data=cur.fetchone()

      cur.close()
      data='register successful'

      return render_template('register.html',data=data)
   return render_template('/register.html')

@app.route('/login',methods=['GET','POST'])
def login():
   if request.method=='POST':
      email_id=request.form['email_id']
      passwords=request.form['passwords']

      cur=mysql.connection.cursor()
      query= 'select * from user where email_id=%s and passwords =%s'
      cur.execute(query,(email_id,passwords,))
      user=cur.fetchone()


      if user:
            if user[6]=='admin':
               return render_template('job_post.html',data=(user[3],user[6],user[0]))
            elif user[6]=='user':
               return render_template("jobs_show.html",data=(user[3],user[6]))

      cur.close()
   return render_template('login.html')

@app.route('/post_job',methods=['POST'])
def job_post():
   title=request.form['title']
   description=request.form['description']
   location=request.form['location']
   posted_by=request.form['posted_by']
   cur=mysql.connection.cursor()
   cur.execute ('INSERT into job(title,description,location,posted_by)VALUES(%s,%s,%s,%s)',(title,description,location,posted_by))
   mysql.connection.commit()
   cur.close()

   return redirect('/list_job')

@app.route('/list_job')
def list_job():
   cur=mysql.connection.cursor()
   cur.execute('select * from job')
   jobs=cur.fetchall()
   cur.close()
   admin='From Admin'
   return render_template('list_of_job.html',job=jobs,admin=admin)

@app.route('/delete_job/<int:id>',methods=['POST'])
def delete(id):
   cur=mysql.connection.cursor()
   cur.execute('Delete from job where id =%s',(id,))
   mysql.connection.commit()
   cur.close
   return redirect('/list_job')

@app.route('/jobs_show')
def job_show():
   cur=mysql.connection.cursor()
   cur.execute('select * from job')
   jobs=cur.fetchall()
   print(jobs)
   cur.close()
   return render_template('jobs_show.html',job=jobs)









@app.route('/list_job')
def jobs_show():

   return render_template('list_of_job.html')















@app.route('/login')
def log():
   return render_template('login.html')
@app.route('/post_job')
def job():
   return render_template('job_post.html')
@app.route('/jobs_show')
def show():
   return render_template('jobs_show.html')





if __name__ == '__main__':
   app.run(debug=True,port=5000)
