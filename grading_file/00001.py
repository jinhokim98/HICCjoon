# app.py
from flask import Flask # 1

app=Flask(__name__) # 2

@app.route("/", methods=['GET']) # 3
def hello_world():
	return "Hello World!"

if __name__ == '__main__': # 4
    app.run()
