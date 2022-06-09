from flask import Flask,redirect, render_template,url_for

portfolio = Flask(__name__)

#home page
@portfolio.route('/')
def render_home():
    return render_template("index.html")

if __name__ == "__main__":
    portfolio.run(debug=True)