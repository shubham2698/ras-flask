from flask import Flask , render_template,request ,flash , session
from functions import *





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
        db.close()
        return render_template(r'dashboard.html',result_f=result_f)


@app.route('/getData/<db_name>/<sem>',methods=['POST','GET'])
def getSemAnalysis(db_name,sem):
    if request.method == 'GET':
        db, connection = connect_database(db_name)
        sl,mi,a,mx,fa,ba=get_subject_analysis(db,sem)
        sl=convert_listItems_int(sl)
        mi=convert_listItems_int(mi)
        a=convert_listItems_int(a)
        mx=convert_listItems_int(mx)
        fa=convert_listItems_int(fa)
        ba=convert_listItems_int(ba)
        arr=[sl,mi,a,mx,fa,ba]
        pie = pieChart(db,sem)
        return render_template(r'graphs.html',pie=pie,sl=arr)


@app.route('/getData/<db_name>',methods=['POST','GET'])
def getSem(db_name):
    if request.method == 'GET':
        db, connection = connect_database(db_name)
        tableN=get_table_name(db,db_name)
        session['tableN'] = tableN
        semList = get_sem_list(db,tableN)
        return render_template(r'semInfo.html', semList=semList,d=db_name)


if __name__ == '__main__':
    app.run(debug=True)