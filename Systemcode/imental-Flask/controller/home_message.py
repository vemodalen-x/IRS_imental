# from model.User import  User
import os
from flask import render_template

@app.route('/')
def layout():
    return render_template('Home.html')
