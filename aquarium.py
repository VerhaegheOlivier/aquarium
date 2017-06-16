from flask import Flask, render_template, request
from DBClass import DbClass

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home',methods=['POST'])
def home():
    global gn,ww
    gn = request.form["gn"]
    ww = request.form["ww"]
    db=DbClass()
    page=db.inlog(gn,ww)
    temp=db.temp()
    return render_template(page,temp=temp)

@app.route('/home')
def home2():
    db = DbClass()
    temp = db.temp()
    return render_template("home.html",temp=temp)

@app.route('/temperatuurAanpassen')
def aanpassen():
    db=DbClass()
    vissen=db.getVis()
    return render_template("temperatuurAanpassen.html",vissen=vissen)

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

    if len(tempAuto)>0:
        commentAuto="*De temperatuur is automatisch gewijzigd."
    else:
        commentAuto="*Gelieve een waarde te selcteren."
    return  render_template("temperatuurAanpassen.html", commentAuto=commentAuto)

@app.route('/instellingen')
def instellingen(comment=""):
    db = DbClass()
    gegevens = db.getGegevens(gn, ww)
    for gegeven in gegevens:
        for i in gegeven:
            if len(i)>4:
                global id,naam,voornaam,email,gebruikersnaam,wachtwoord
                id=i[0]
                naam=i[1]
                voornaam=i[2]
                email=i[3]
                gebruikersnaam=i[6]
                wachtwoord=i[7]
            else:
                global lengte,breedte,hoogte, aquariumID
                lengte=i[0]
                breedte=i[1]
                hoogte=i[2]
                aquariumID=i[3]

    return render_template("instellingen.html",naam=naam,voornaam=voornaam,email=email,gebruikersnaam=gebruikersnaam,wachtwoord=wachtwoord,lengte=lengte,breedte=breedte,hoogte=hoogte, commentUpdate=comment)

@app.route('/instellingen/aangepast',methods=['POST'])
def aanpassenInstelingen():
    db = DbClass()
    naam=request.form.get("naam")
    voornaam=request.form.get("voornaam")
    email = request.form.get("email")
    gebruikersnaam = request.form.get("gebruikersnaam")
    wachtwoord = request.form.get("wachtwoord")
    lengte=request.form.get("lengte")
    breedte = request.form.get("breedte")
    hoogte = request.form.get("hoogte")
    if naam == "" or voornaam == "" or email == "" or gebruikersnaam == "" or wachtwoord == "" or lengte=="" or breedte=="" or hoogte=="":
        return instellingen(comment="*Gelieve alle gegevens integeven.")

    commentUpdate = db.updateGegevens(str(id),str(naam),str(voornaam),str(email),str(gebruikersnaam),str(wachtwoord),str(lengte),str(breedte),str(hoogte))
    return render_template("instellingen.html",commentUpdate=commentUpdate)




if __name__ == '__main__':
    app.run(host='169.254.10.11')