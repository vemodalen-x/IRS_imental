from flask import Flask, render_template, redirect, url_for, request, session, flash
from model.questions import Questions
from model.user import User
from model.result import Result
from model.user_result import User_Result
from model.material import Article
from init import app, db


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/home')
def home_page():
    return redirect(url_for('home'))

@app.route('/home_log')
def home_log():
    return render_template('Home_log.html')

@app.route('/ques')
def ques():
    return render_template('Ques.html')

@app.route('/question', methods=['GET','POST'])
def question():
    ques_id = 1
    current_id = 'None'
    result = 'None'
    type = 'None'

    if request.method == 'POST':
        if request.form['ques_id'] != 'None':
            ques_id = request.form['ques_id']
        if request.form['current_id'] != 'None':
            current_id = request.form['current_id']
        if request.form['result'] != 'None':
            result = request.form['result']
        if request.form['type'] != 'None':
            type = request.form['type']

    if result != 'None' and len(result) != 0:
        note = Result.query.get(int(current_id))
        if note is not None:
            db.session.delete(note)
            db.session.commit()
        xx = Result(id=current_id, type=type, option1=result)
        db.session.add(xx)
        db.session.commit()

    i = ques_id
    # result_list[int(i)] = result
    question = Questions.query.filter(Questions.id == i)
    if int(i) == 1:
        return render_template('Ques_pages/question1.html',entries=question)
    elif int(i) == 90:
        return render_template('Ques_pages/question3.html',entries=question)
    else:
        return render_template('Ques_pages/question2.html', entries=question)

@app.route('/result', methods=['GET','POST'])
def result():
    ques_id = 1
    current_id = 'None'
    result = 'None'
    type = 'None'

    if request.method == 'POST':
        if request.form['ques_id'] != 'None':
            ques_id = request.form['ques_id']
        if request.form['current_id'] != 'None':
            current_id = request.form['current_id']
        if request.form['result'] != 'None':
            result = request.form['result']
        if request.form['type'] != 'None':
            type = request.form['type']

    if result != 'None' and len(result) != 0:
        note = Result.query.get(int(current_id))
        if note is not None:
            db.session.delete(note)
            db.session.commit()
        xx = Result(id=current_id, type=type, option1=result)
        db.session.add(xx)
        db.session.commit()

    anxi = Result.query.filter_by(type='Anxiety').all()
    depr = Result.query.filter_by(type='Depression').all()
    host = Result.query.filter_by(type='Hostility').all()
    sens = Result.query.filter_by(type='Interpersonal').all()
    obse = Result.query.filter_by(type='Obsession').all()
    para = Result.query.filter_by(type='Paranoid').all()
    psyc = Result.query.filter_by(type='Psychosis').all()
    soma = Result.query.filter_by(type='Somatization').all()
    terr = Result.query.filter_by(type='Terror').all()


    val = 0
    i = 0
    for item in anxi:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    anxi_value = val / i

    val = 0
    i = 0
    for item in depr:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    depr_value = val / i

    val = 0
    i = 0
    for item in host:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    host_value = val / i

    val = 0
    i = 0
    for item in sens:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    sens_value = val / i

    val = 0
    i = 0
    for item in obse:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    obse_value = val / i

    val = 0
    i = 0
    for item in para:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    para_value = val / i

    val = 0
    i = 0
    for item in psyc:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    psyc_value = val / i

    val = 0
    i = 0
    for item in soma:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    soma_value = val / i

    val = 0
    i = 0
    for item in terr:
        i = i + 1
        opt = item.option1
        val = val + int(opt)
    terr_value = val / i

    value_list = [anxi_value, depr_value, host_value, sens_value, obse_value, para_value, psyc_value, soma_value, terr_value]

    global user_global

    user_rst = User_Result.query.filter_by(username=user_global).first()
    if user_rst is not None:
        db.session.delete(user_rst)
        db.session.commit()
    yy = User_Result(username=user_global, anxi=anxi_value, depr=depr_value, host=host_value, sens=sens_value, obse=obse_value, para=para_value, psyc=psyc_value, soma=soma_value, terr=terr_value)
    db.session.add(yy)
    db.session.commit()

    result_delete = Result.query.all()
    for rst in result_delete:
        db.session.delete(rst)
        db.session.commit()

    value_dic = {'Anxiety' : anxi_value,
                 'Depression' : depr_value,
                 'Hostility' : host_value,
                 'Interpersonal sensitivity' : sens_value,
                 'Obsession' : obse_value,
                 'Paranoid': para_value,
                 'Psychosis' : psyc_value,
                 'Somatization' : soma_value,
                 'Terror' : terr_value
                 }
    max_value = max(value_dic, key=value_dic.get)

    return render_template('Ques_result.html', tag=value_list, tag2=max_value)

@app.route('/chat')
def chat():
    return render_template('Chat.html')

@app.route('/mate')
def mate():
    article1 = Article.query.filter_by(Article_id=2110010007).first()
    title1 = article1.Title
    label1 = article1.Label

    article2 = Article.query.filter_by(Article_id=2110010008).first()
    title2 = article2.Title
    label2 = article2.Label

    article3 = Article.query.filter_by(Article_id=2110010009).first()
    title3 = article3.Title
    label3 = article3.Label

    return render_template('Mate.html', title1=title1, label1=label1, title2=title2, label2=label2, title3=title3, label3=label3)

@app.route('/article1')
def article1():
    article = Article.query.filter_by(Article_id=2110010007).first()
    title = article.Title
    date = article.Upload_date
    label = article.Label
    content = article.Content
    return render_template('/Mate_pages/material1.html',title=title, date=date, label=label, content=content)

@app.route('/article2')
def article2():
    article = Article.query.filter_by(Article_id=2110010008).first()
    title = article.Title
    date = article.Upload_date
    label = article.Label
    content = article.Content
    return render_template('/Mate_pages/material2.html', title=title, date=date, label=label, content=content)

@app.route('/article3')
def article3():
    article = Article.query.filter_by(Article_id=2110010009).first()
    title = article.Title
    date = article.Upload_date
    label = article.Label
    content = article.Content
    return render_template('/Mate_pages/material3.html', title=title, date=date, label=label, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=request.form['username']).first()
        passwd = User.query.filter_by(password=request.form['password']).first()

        global user_global
        user_global = user.username

        if user is None:
            error = 'Invalid username'
        elif passwd is None:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home_log'))
    return render_template('Login.html', error=error)

@app.route('/reg',methods=['GET','POST'])
def reg():
    error = None
    username = request.form.get('username')
    password = request.form.get('password')
    if (username is not None) & (password is not None):
        if (username != '') & (password != ''):
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('Login_register.html')

@app.route('/personal')
def personal():
    global user_global

    Curr_User = User_Result.query.filter_by(username=user_global).first()
    anxi_value = Curr_User.anxi
    depr_value = Curr_User.depr
    host_value = Curr_User.host
    sens_value = Curr_User.sens
    obse_value = Curr_User.obse
    para_value = Curr_User.para
    psyc_value = Curr_User.psyc
    soma_value = Curr_User.soma
    terr_value = Curr_User.terr

    value_list = [anxi_value, depr_value, host_value, sens_value, obse_value, para_value, psyc_value, soma_value, terr_value]
    value_dic = {'Anxiety': anxi_value,
                 'Depression': depr_value,
                 'Hostility': host_value,
                 'Interpersonal sensitivity': sens_value,
                 'Obsession': obse_value,
                 'Paranoid': para_value,
                 'Psychosis': psyc_value,
                 'Somatization': soma_value,
                 'Terror': terr_value
                 }
    max_value = max(value_dic, key=value_dic.get)

    return render_template('Personal.html',tag=user_global, tag2=value_list, tag3=max_value)

if __name__ == '__main__':
    app.run()
