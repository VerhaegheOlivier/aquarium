from flask import Flask, render_template, request
class DbClass:
    __bestand = '/sys/bus/w1/devices/28-800000038fd7/w1_slave'
    def __init__(self):
        import mysql.connector as connector

        self.__dsn= {"host": "localhost", "user":"root", "passwd":"olivier", "db":"vissendb"}

        self.__connection=connector.connect(**self.__dsn)
        self.__cursor=self.__connection.cursor()
        self.__id=""
    def inlog(self,gn,ww):
        q = "select wachtwoord from tblgebruiker where gebruikersnaam='"+gn+"';"
        self.__cursor.execute(q)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        if len(result)==1:
            for ww2 in result:
                if(ww2[0]==ww):
                    global wachtwoord
                    wachtwoord=ww2[0]
                    return "home.html"
                else:
                    return "index.html"
        else:
            return  "index.html"

    def getGegevens(self,gn,ww):
        qGebruiker="select * from tblgebruiker where gebruikersnaam='"+gn+"' and wachtwoord='"+ww+"';"
        self.__cursor.execute(qGebruiker)
        resultGebruiker = self.__cursor.fetchall()

        for id in resultGebruiker:
            self.__id=id[0]
            qAquarium = "SELECT lengte,breedte,hoogte, aquariumID FROM vissendb.tblaquarium where gebruikerID=" + str(id[0]) + ";"
            self.__cursor.execute(qAquarium)
        resultAquarium = self.__cursor.fetchall()
        self.__cursor.close()
        return resultGebruiker,resultAquarium

    def updateGegevens(self,id,naam,voornaam,email, gebruikersnaam, wachtwoord, lengte,breedte,hoogte):
        qGebruiker = "UPDATE tblgebruiker SET naam ='"+naam+"', voornaam = '"+voornaam+"', email = '"+email+"', gebruikersnaam = '"+gebruikersnaam+"', wachtwoord = '"+wachtwoord+"' WHERE gebruikerID = "+id+";"
        self.__cursor.execute(qGebruiker)
        self.__connection.commit()

        qAquarium = "UPDATE tblaquarium SET lengte =" + lengte + ", breedte = " +breedte+ ", hoogte = " +hoogte+ " WHERE gebruikerID = " + id + ";"
        self.__cursor.execute(qAquarium)
        self.__connection.commit()
        self.__cursor.close()
        return "*Gegevens zijn aangepast."

    def getVis(self):
        q="SELECT naam, temperatuur FROM vissendb.tblvis;"
        self.__cursor.execute(q)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getAqariumId(self):
        print(self.__id)
        q="SELECT aquariumID FROM tblaquarium WHERE gebruikerID="+self.__id+";"
        print(q)
        self.__cursor.execute(q)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getLog(self,aquariumID):
        q = "SELECT time, temperatuur, gemiddeldeTemperatuur FROM vissendb.tbllogfile where aquariumID="+aquariumID+";"
        self.__cursor.execute(q)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def insertLog(self,tijd, temp, gemTemp, id):
        q="INSERT INTO `vissendb`.`tbllogfile` VALUES ('"+str(tijd)+"',"+str(temp)+","+str(gemTemp)+","+str(id)+");"
        print(q)
        self.__cursor.execute(q)
        self.__connection.commit()
        self.__cursor.close()

    def temp(self):
        fp = open(DbClass.__bestand, 'r')
        regels = fp.readlines()
        graden = regels[1].find('t=')
        if graden > -1:
            tekst = regels[1]
            cel = int(tekst[graden + 2:-1]) / 1000.0

            return cel
        else:
            return ""
