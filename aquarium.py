from flask import Flask, render_template, request
from DBClass import DbClass

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home',methods=['POST'])
def home():
    gn = request.form["gn"]
    ww = request.form["ww"]
    db=DbClass()
    page=db.inlog(gn,ww)
    return render_template(page)

@app.route('/home')
def home2():
    return render_template("home.html")

@app.route('/temperatuurAanpassen')
def aanpassen():
    return render_template("temperatuurAanpassen.html")

@app.route('/temperatuurAanpassen/zelfAangepast',methods=['POST'])
def aangepastZelf():
    tempZelf=request.form['zelfGraden']
    if tempZelf>str(0):
        commentZelf="*De temperatuur is  handmatig gewijzigd."
    else:
        commentZelf="*Gelieve een positief temperatuur in te geven."
    return render_template("temperatuurAanpassen.html", commentZelf=commentZelf)

@app.route('/temperatuurAanpassen/automatischAangepast',methods=['POST'])
def aangepastAuto():
    tempAuto=request.form['autoGraden']
    print(tempAuto)
    if len(tempAuto)>0:
        commentAuto="*De temperatuur is automatisch gewijzigd."
    else:
        commentAuto="*Gelieve een waarde te selcteren."
    return  render_template("temperatuurAanpassen.html", commentAuto=commentAuto)

@app.route('/instellingen')
def instellingen():
    return render_template("instellingen.html")

if __name__ == '__main__':
    app.run()