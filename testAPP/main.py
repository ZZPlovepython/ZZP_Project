import os
from flask import Flask,request,render_template, session, redirect 
import sys  
import os  
  
app = None  
if getattr(sys, 'frozen', False):  
    template_folder = os.path.join(sys.executable, '..', 'templates')  
    static_folder = os.path.join(sys.executable, '..', 'static')  
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)  
else:  
    app = Flask(__name__) 

@app.route('/404')
def index():
	return render_template('main.html')
	#return redirect('/user/zzp')
	#return '<h1>wocao</h1>'

@app.route('/user/<name>')
def user(name):
	return '<h>Hello %s !</h>'%name


if __name__ == '__main__':
    app.run(debug=True)