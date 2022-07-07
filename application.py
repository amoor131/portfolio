from flask import Flask, render_template
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Sort(db.Model):
    key = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    words = db.Column(db.String(26600))

    def __repr__(self):
        return f"{self.key} - {self.words}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/solutions")
def solutions():
    return render_template("solutions.html")

@app.route("/descrambler")
def descrambler():
    return render_template("descrambler.html")
    
@app.route("/descrambler/<key>")
def descrambler_results(key):
    results = Sort.query.get_or_404(key)
    return {"key":results.key, "words": results.words}
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)
