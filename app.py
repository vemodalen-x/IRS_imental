from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/home')
def home_page():
    return redirect(url_for('home'))

@app.route('/ques')
def ques():
    return render_template('Ques.html')

@app.route('/question')
def question():
    return render_template('Ques_question.html')

@app.route('/result')
def result():
    return render_template('Ques_result.html')

@app.route('/chat')
def chat():
    return render_template('Chat.html')

@app.route('/mate')
def mate():
    return render_template('Mate.html')

@app.route('/article1')
def article():
    return render_template('Mate_article.html')

@app.route('/login')
def login():
    return render_template('Login.html')

@app.route('/reg')
def reg():
    return render_template('Login_register.html')

@app.route('/personal')
def personal():
    return render_template('Personal.html')

if __name__ == '__main__':
    app.run()
