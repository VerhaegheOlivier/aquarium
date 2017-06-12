from flask import Flask, render_template, request
class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn= {"host": "localhost", "user":"root", "passwd":"olivier", "db":"vissendb"}

        self.__connection=connector.connect(**self.__dsn)
        self.__cursor=self.__connection.cursor()
    def inlog(self,gn,ww):
        q = "select wachtwoord from tblgebruiker where gebruikersnaam='"+gn+"';"
        self.__cursor.execute(q)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        if len(result)==1:
            for ww2 in result:
                if(ww2[0]==ww):
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
            qAquarium = "SELECT lengte,breedte,hoogte FROM vissendb.tblaquarium where gebruikerID=" + str(id[0]) + ";"
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
