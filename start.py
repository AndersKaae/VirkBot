from flask import Flask, render_template, flash, request, redirect, url_for, session
import time
from browser import *
from webfunctions import *
from data import *
#from database import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST": 
        session['registrationstype'] = request.form['dropdownitem']
        if request.form.get('dropdownitem') == 'ApS':
            if JsonLoader(request.form['textfield']) != "" and request.form['emailfield'] != "":
                session['jsondata'] = request.form['textfield']
                session['email'] = request.form['emailfield']
                return redirect('/processor')
            else:
                flash('Invalid JSON and/or e-mail')
        if request.form.get('dropdownitem') == 'Efterregistrering':
            if JsonLoader(request.form['textfield']) != "":
                session['jsondata'] = request.form['textfield']
                return redirect('/processor')
            else:
                flash('Invalid JSON')
    return render_template('home.html')

@app.route('/processor')
def processor():
    browser = LaunchSelenium()
    legalOwnerList, managementList, company, jsondata = JsonParser(session['jsondata'])
    if session['registrationstype'] == 'ApS':
        time, ID = MainCapitalCompany(browser, legalOwnerList, managementList, company, jsondata, session['email'])
    if session['registrationstype'] == 'Efterregistrering':
        time, ID = MainSubsequentReg(browser, company)
    # Closing selenium
    try:
        browser.close()
        browser.quit()
    except:
        pass
    return render_template('processor.html', time = time, ID = ID)

@app.route('/waiting')
def waiting():
    return render_template('waiting.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.run(debug=True)