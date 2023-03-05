from flask import Flask , render_template,request ,flash , session,redirect,url_for
from functions import *





app = Flask(__name__)
app.config['SECRET_KEY'] = 'wallpaperwide'


@app.route('/', methods=['POST','GET'])
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
                session["iname"]=str(result[0][1]).replace(" ","_")

                return redirect(url_for('dash'))
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
            db.execute(f"CREATE DATABASE {iname.replace(' ','_')}")
            db.close()
            connection.close()
            flash('Successfully Registered. Try to SIGN IN now ..', category='success')
            return render_template(r"register.html")


@app.route('/dash',methods=['POST','GET'])
def dash():
    if request.method == 'GET':
        db,connection=connect_database_server()
        db.execute(f"SHOW TABLES FROM {session['iname']}")
        result = db.fetchall()
        result_f=[]
        for each in result:
            result_f.append(each[0])
        db.close()
        return render_template(r'dashboard.html',result_f=result_f)


@app.route('/getData/<table_name>',methods=['POST','GET'])
def getSem(table_name):
    if request.method == 'GET':
        db, connection = connect_database(session['iname'])
        tableN=table_name
        session['tableN'] = tableN
        semList = get_sem_list(db,session['tableN'])
        return render_template(r'semInfo.html', semList=semList)


@app.route('/getData/<table_name>/<sem>',methods=['POST','GET'])
def getSemAnalysis(table_name,sem):
    if request.method == 'GET':
        db, connection = connect_database(session["iname"])
        sl,mi,a,mx,fa,ba=get_subject_analysis(db,sem,table_name)
        sl=convert_listItems_int(sl)
        mi=convert_listItems_int(mi)
        a=convert_listItems_int(a)
        mx=convert_listItems_int(mx)
        fa=convert_listItems_int(fa)
        ba=convert_listItems_int(ba)
        arr=[sl,mi,a,mx,fa,ba]
        pie = pieChart(db,sem)
        return render_template(r'graphs.html',pie=pie,sl=arr)


if __name__ == '__main__':
    app.run(debug=True)