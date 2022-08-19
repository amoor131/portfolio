from flask import Flask, render_template, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy
import json

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

#class for 
class Sort(db.Model):
    key = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    words = db.Column(db.String(26600))

    def __repr__(self):
        return f"{self.key} - {self.words}"

db.create_all()

def populate():
    new_line = '\n'
    with open("dictionary.json",'r') as dict:
        keys = json.load(dict)
        for word in keys:
            values = keys[word]
            #print(f"word: {word} {new_line} keys[{word}] : {values}")
            entry = Sort(key=word, words=keys[word])
            #print(f"adding {entry}")
            db.session.add(entry)
        print(f"commiting all")
        db.session.commit()

checkEmpty = Sort.query.count()
print(f"checking if db empty: {checkEmpty}")
if (checkEmpty == 0):
    print("adding to database")
    populate()

@app.route("/")
def home():
    return render_template("index.html")

'''
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/solutions")
def solutions():
    return render_template("solutions.html")
'''

@app.route("/descrambler")
#Function gets url parameter SORTED and returns result of query for value where key = SORTED
def descrambler():
    letterSet = request.args.get('sorted', default = '*')
    #page with no search made
    if letterSet == '*':
        f"letter set is {letterSet}"
        return render_template("descrambler.html")
    #page with results from user input
    else:
        letterSet = ''.join(sorted(letterSet.upper()))
        isKey = Sort.query.filter_by(key=letterSet).first() is not None
        if isKey == True:
            result = Sort.query.filter_by(key=letterSet).first()
            print(f"results: {result}")
            result = str(result).split( )
            result.pop(0)
            result.pop(0)
            result = ' '.join(result)
            print(f"search with key {letterSet} found: {result}")
            return render_template("descrambler.html", possibleWords=result)
        else:
            return render_template("descrambler.html", possibleWords="No words found")

#this function lets me populate the /descrambler page with the contents of a file
@app.route("/resources/aboutDescrambler.txt")    
def test():
    about = ""
    with open("aboutDescrambler.txt","r") as file:
        for lines in file:
            #print(f"about = {about}")
            about += lines 
            #print(f"updated about = {about}")
    return about


'''
#render page for choice tracker
@app.route("/choicetracker")
def choicetracker():
    return render_template("choicetracker.html")

#temporary page while I figure out how to test if user is signed in
#render page for choice tracker sign-in
@app.route("/choicetrackersignin")
def choicetrackersignin():
    return render_template("choicetrackerSignin.html")
'''
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)