from flask import render_template
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