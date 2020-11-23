#!/usr/bin/env python
'''

Bot de Medias Moviles
---------------------------
Autor: Patricio Henderson Vigil
Version: 1.0

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

consumer_key = "qtzSGjqwNjzd0KXlxMuJ0HYLy"
consumer_secret = "cIS2KZ4qicfAn499hPwl0vIkenKrwRdNIqEmoxfbi2h6ZojHfp"
acces_token = "1330939267628085252-T64fEg9TAvrSB2jfbJ87Qxw0NP1bW0"
acces_token_secret = "RAbTEPiTV6FdSaqovFT3upfv4UkzT8WI3VZb2oBizweyS"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

auth.set_access_token(acces_token, acces_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)





def analisis (empresa):
    precio_dieciocho = 0
    precio_nueve = 0
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
                precio_dieciocho += precio_cierre
                #Vamos sumando el precio de cierre
            promedio_dieciocho = precio_dieciocho / 18
            #obtenemos el promedio del cierre de las últimas 20 rondas.
    

            #Procedemos a sacar la media de los últimos 09 períodos
            ultimas_nueve = len_reader - 9
            #Restaos para obtener las últimas 09 y poder sacar la media

            for i in range(ultimas_nueve,len_reader):

                row = file[i]
                #arrancamos desde las últimas 09 filas
                precio_cierre = float(row.get("Close"))
                #obtenemos el precio de cierre
                precio_nueve += precio_cierre
                #Vamos sumando el precio de cierre
            promedio_nueve = precio_nueve / 9
            #obtenemos el promedio del cierre de las últimas 20 rondas.

            #print (promedio_nueve, promedio_dieciocho)
            #Realizamos conclusiones :

            if 0 < (promedio_nueve - promedio_dieciocho) < 1 :


                api.update_status("En el timeframe semanal (9 y 18), en la empresa {}, estamos cerca de un cruce de medias " .format(empresa))
                print("Cruce de  medias en ",empresa)

            #print ("Media de 18: {}, media de 9 {} en {}" .format(promedio_dieciocho, promedio_nueve, empresa))
        except:
            print("Hay un problema en " , empresa)


#Descarga del archivo .csv con la cotización

panel_lider = ["ALUA", "BBAR", "BMA", "BYMA", "CEPU", "COME", "CRES", "CVH", "EDN",
               "GGAL","MIRG", "PAMP", "SUPV", "TECO2", "TGNO4", "TGSU2", "TRAN", 
               "TXAR", "VALO", "YPFD"]
#Seleccionamos las acciones que queremos descargar por su ticker, en este caso "Galicia"
for i in panel_lider:
    df = pdr.get_data_yahoo(str(i)+".BA","01/01/20",interval = "w") 
    #Seleccionamos la bolsa donde cotizan ".BA" la fecha desde y el intervalo
    df = df[df["Volume"]>0]
    #Eliminamos los dias con volumen de operación 0
    df = df.drop(["Adj Close"], axis = 1)
    #elimnar información sobre los cierres ajustados
    df.to_csv(str(i)+ "BA.csv")
    #Damos nombre y escrbimos el archivo.csv
    
    print(i, "Descargado")


#Procedemos a sacar la media de los últimos 18 períodos

for empresa in panel_lider:
    analisis(empresa)


