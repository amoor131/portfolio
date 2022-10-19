from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
#from curses.ascii import isalpha #for addKey
from addKeyDeps import isKey, fitsIn
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///descrambler.db'

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

#called in descrambler function
#adds new key
def addKey(testKey):
    print(f"testing key: {testKey}")
    #used to add new lines to f statements
    new_line = '\n'
    #check that the entry is only letters
    if testKey.isalpha() == False:
        return -1
    #user input in reverse alphabetical order, 
    sortedKey = ''.join(sorted(testKey.strip('\n')))
    foundWords = ''
    with open('sorted_length.txt','r') as engWords:
        for word in engWords:
            if fitsIn(word, testKey):
                foundWords += ' ' + ''.join(word.strip('\n')) # not sure if I need to strip new line
        if len(foundWords) > 0:
            entry = Sort(key=testKey, words=foundWords)
            db.session.add(entry)
            db.session.commit()
            return 1

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
        #sorts user input alphabetically and sets to uppercase
        letterSet = ''.join(sorted(letterSet.upper()))
        #find if this key exists
        keyExists = Sort.query.filter_by(key=letterSet).first() is not None
        if keyExists == True:
            result = Sort.query.filter_by(key=letterSet).first()
            print(f"results: {result}")
            result = str(result).split( )
            result.pop(0)
            result.pop(0)
            result = ' '.join(result)
            print(f"search with key {letterSet} found: {result}") #DEBUG
            return render_template("descrambler.html", possibleWords=result)
        else:
            tryAddKey = addKey(letterSet)
            match tryAddKey:
                case 1:
                    print(f"successfully added key {letterSet}")
                    result = Sort.query.filter_by(key=letterSet).first()
                    print(f"results: {result}")
                    result = str(result).split( )
                    result.pop(0)
                    result.pop(0)
                    result = ' '.join(result)
                    return render_template("descrambler.html", possibleWords=result)
                case 0:
                    print(f"tried adding key {letterSet} but it already existed")#DEBUG
                    return render_template("descrambler.html", possibleWords="No words found")
                case -1:
                    print(f"tried adding key {letterSet} but it contains non alphabet characters")
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


@app.route("/grid")
def grid():
    return render_template("grid.html")

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