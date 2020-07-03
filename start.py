from flask import Flask, render_template, flash, request, redirect
import time
from browser import *
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        flash('You were successfully logged in')
        time.sleep(1)
        flash('You were successfully logged in')
        #browser()

    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)