from flask import Flask, render_template, request, redirect
import pandas as pd
app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def main():
	message='Hello World'
	return render_template('index.html', message=message)


#Конфиг запуска	
if __name__=='__main__':
	app.run(port=8000,debug=True)