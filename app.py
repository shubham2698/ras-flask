from flask import Flask , render_template,request ,flash,redirect,url_for,jsonify
import pymysql

def connect_database_server():
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()

def connect_database(dbName):
    try:
        connection = pymysql.connect(host="localhost", user="root", passwd="", database=f"{dbName}")
        db = connection.cursor()
        return db,connection
    except:
        print("\033[91mFAILED TO CONNECT WITH YOUR DATABASE\033[0m")
        exit()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'wallpaperwide'


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template(r"login.html")
    elif request.method == 'POST':
        email=request.form['email']
        password = request.form['password']
        db,connection=connect_database("ras")
        db.execute(f"SELECT pass_word,institute_name FROM user_info WHERE email_id = '{email}' ")
        result = db.fetchall()
        db.close()
        connection.close()
        try:
            if result[0][0] == password:
                return render_template('dashboard.html',institute=result[0][1])
            else:
                flash('invalid password. Try Again..', category='error')
                return render_template(r"login.html")
        except:
            flash('invalid email/password. Try Again..', category='error')
            return render_template(r"login.html")



@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template(r"register.html")
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_c = request.form['password_c']
        iname = request.form['iname']
        if password != password_c:
            flash('Password not matched. Try Again..', category='error')
            return render_template(r"register.html")
        else:
            db,connection = connect_database("ras")
            db.execute(f"INSERT INTO user_info (email_id,pass_word,institute_name) VALUES ('{email}','{password}','{iname}')")
            connection.commit()
            db.close()
            connection.close()
            flash('Successfully Registered. Try to SIGN IN now ..', category='success')
            return render_template(r"register.html")



@app.route('/',methods=['POST','GET'])
def dash():
    if request.method == 'GET':
        db,connection=connect_database_server()
        db.execute(f"show databases")
        result = db.fetchall()
        result_f=[]
        remove_d = ['information_schema', 'mysql', 'performance_schema', 'phpmyadmin']
        for each in result:
            if each[0] in remove_d:
                pass
            else:
                result_f.append(each[0])
        return render_template(r'dashboard.html',result_f=result_f)


@app.route('/getData/<db_name>',methods=['POST','GET'])
def getData(db_name):
    if request.method == 'GET':
        db, connection = connect_database(db_name)
        db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM mca2020_all WHERE SEM=2 AND `SUBJECT CODE`=121 OR `SUBJECT CODE`=111")
        result = db.fetchall()
        total_student=result[0][0]
        db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM mca2020_all WHERE SEM=2 AND `SEM 2`!='F' AND `GENDER`=' M'")
        result = db.fetchall()
        passedBoys = int(result[0][0])
        db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM mca2020_all WHERE SEM=2 AND `SEM 2`!='F' AND `GENDER`=' F'")
        result = db.fetchall()
        passedGirls = int(result[0][0])
        db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM mca2020_all WHERE SEM=2 AND `SEM 2`='F' AND `GENDER`=' M'")
        result = db.fetchall()
        failedBoys = int(result[0][0])
        db.execute(f"SELECT COUNT(DISTINCT(`NAME OF STUDENT`)) FROM mca2020_all WHERE SEM=2 AND `SEM 2`='F' AND `GENDER`=' F'")
        result = db.fetchall()
        failedGirls = int(result[0][0])
        res=[passedBoys,passedGirls,failedBoys,failedGirls]
        return render_template(r'graphs.html',result=res)



if __name__ == '__main__':
    app.run(debug=True)