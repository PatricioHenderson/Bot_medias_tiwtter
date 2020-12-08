#!/usr/bin/env python
'''

Bot de Medias Moviles
---------------------------
Autor: Patricio Henderson Vigil
Version: 1.9

Descripcion:
Programa que analiza si hubo cruce de medias moviles
'''

__author__ = "Patricio Henderson"
__email__ = "patriciohenderson@hotmail.com"
__version__ = "1.4"


import csv
import pandas_datareader as pdr
import statistics
import tweepy
import pandas as pd
from datetime import date

consumer_key = "qtzSGjqwNjzd0KXlxMuJ0HYLy"
consumer_secret = "cIS2KZ4qicfAn499hPwl0vIkenKrwRdNIqEmoxfbi2h6ZojHfp"
acces_token = "1330939267628085252-T64fEg9TAvrSB2jfbJ87Qxw0NP1bW0"
acces_token_secret = "RAbTEPiTV6FdSaqovFT3upfv4UkzT8WI3VZb2oBizweyS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(acces_token, acces_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)





def analisis_semanal (empresa):
    precio_dieciocho = []
    precio_nueve = []
    nombre = empresa + "BA.csv"
    with open (nombre) as fo:
    #Abrimos archivo .csv    

        file = list(csv.DictReader(fo))
        #leemos en forma de lista
        len_reader = len(file)
    
        ultimas_dieciocho = len_reader - 18
        #Restaos para obtener las últimas 18 y poder sacar la media
        try:
            for i in range(ultimas_dieciocho,len_reader):

                row = file[i]
                #arrancamos desde las últimas 20 filas
                precio_cierre = float(row.get("Close"))
                #obtenemos el precio de cierre
                precio_dieciocho.append(precio_cierre)
                #Vamos sumando el precio de cierre
            promedio_dieciocho = statistics.mean(precio_dieciocho)
            #obtenemos el promedio del cierre de las últimas 18 rondas.
            

            #Procedemos a sacar la media de los últimos 09 períodos
            ultimas_nueve = len_reader - 9
            #Restaos para obtener las últimas 09 y poder sacar la media

            for i in range(ultimas_nueve,len_reader):

                row = file[i]
                #arrancamos desde las últimas 09 filas
                precio_cierre = float(row.get("Close"))
                #obtenemos el precio de cierre
                precio_nueve.append(precio_cierre)
                #Vamos sumando el precio de cierre
            promedio_nueve = statistics.mean(precio_nueve)
            #obtenemos el promedio del cierre de las últimas 20 rondas.
            
            
            #Realizamos conclusiones :

            if 0 < (promedio_nueve - promedio_dieciocho) < 1 :


                api.update_status("En timeframe semanal (9 y 18), en la empresa {}, estamos cerca de un cruce de medias " .format(empresa))
                print("Cruce de  medias semanal en ",empresa)
            
            #print ("Media de 18: {}, media de 9 {} en {}" .format(promedio_dieciocho, promedio_nueve, empresa))
        except:
            print("Hay un problema en " , empresa)
            fo = open("reporte_errores.txt","a")
            lines = ("Hay un problema en " , empresa, date.today(), "En semanal")
            fo.write(str(lines))
            fo.write("\n")
            fo.flush()
            fo.close()


def analisis_diario (empresa):
    precio_dieciocho = []
    precio_nueve = []
    nombre = empresa + "BA.csv"
    with open (nombre) as fo:
    #Abrimos archivo .csv    

        file = list(csv.DictReader(fo))
        #leemos en forma de lista
        len_reader = len(file)
    
        ultimas_dieciocho = len_reader - 18
        #Restaos para obtener las últimas 18 y poder sacar la media
        try:
            for i in range(ultimas_dieciocho,len_reader):

                row = file[i]
                #arrancamos desde las últimas 20 filas
                precio_cierre = float(row.get("Close"))
                #obtenemos el precio de cierre
                precio_dieciocho.append(precio_cierre)
                #Vamos sumando el precio de cierre
            promedio_dieciocho = statistics.mean(precio_dieciocho)
            #obtenemos el promedio del cierre de las últimas  rondas.
            

            #Procedemos a sacar la media de los últimos 09 períodos
            ultimas_nueve = len_reader - 9
            #Restaos para obtener las últimas 09 y poder sacar la media

            for i in range(ultimas_nueve,len_reader):

                row = file[i]
                #arrancamos desde las últimas 09 filas
                precio_cierre = float(row.get("Close"))
                #obtenemos el precio de cierre
                precio_nueve.append(precio_cierre)
                #Vamos sumando el precio de cierre
            promedio_nueve = statistics.mean(precio_nueve)
            #obtenemos el promedio del cierre de las últimas 20 rondas.
            
            
            #Realizamos conclusiones :

            if 0 < (promedio_nueve - promedio_dieciocho) < 1 :


                api.update_status("En timeframe diario (9 y 18), en la empresa {}, estamos cerca de un cruce de medias " .format(empresa))
                print("Cruce de  medias diario en ",empresa)
            
        except:
            print("Hay un problema en " , empresa)
            fo = open("reporte_errores.txt","a")
            lines = ("Hay un problema en " , empresa, date.today(), "en diario")
            fo.write(str(lines))
            fo.write("\n")
            fo.flush()
            fo.close()

#Descarga del archivo .csv con la cotización

panel_lider = ["ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
               "GGAL","MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2", "TRAN", 
               "TXAR", "VALO", "YPFD"]
#Seleccionamos las acciones que queremos descargar por su ticker, en este caso "Galicia"
def descarga_semanal():
    for i in panel_lider:
        df = pdr.get_data_yahoo(str(i)+".BA","01/01/20",interval = "w") 
        #Seleccionamos la bolsa donde cotizan ".BA" la fecha desde y el intervalo
        df = df[df["Volume"]>0]
        #Eliminamos los dias con volumen de operación 0
        df = df.drop(["Adj Close"], axis = 1)
        #elimnar información sobre los cierres ajustados
        df.to_csv(str(i)+ "BA.csv")
        #Damos nombre y escrbimos el archivo.csv
    
        print(i, "Descargado Semanal")

def descarga_diaria():
    for i in panel_lider:
        df = pdr.get_data_yahoo(str(i)+".BA","01/10/20",interval = "d") 
        #Seleccionamos la bolsa donde cotizan ".BA" la fecha desde y el intervalo
        df = df[df["Volume"]>0]
        #Eliminamos los dias con volumen de operación 0
        df = df.drop(["Adj Close"], axis = 1)
        #elimnar información sobre los cierres ajustados
        df.to_csv(str(i)+ "BA.csv")
        #Damos nombre y escrbimos el archivo.csv
    
        print(i, "Descargado diario")

if __name__ == "__main__":

    descarga_diaria()
    for empresa in panel_lider:
        analisis_diario(empresa)
    descarga_semanal()
    for empresa in panel_lider:
        analisis_semanal(empresa)


