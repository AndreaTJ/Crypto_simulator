import requests
from configparser import *

config = ConfigParser()
config.read('config.ini')
APIKEY = config["DEFAULT"]["APIKEY"]

def busca_API_cambio (CantidadInvertida, From, To):
  URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

  url = URL.format(CantidadInvertida, From, To, APIKEY)
  
  try:
      results = requests.get(url)
      try:
        results.status_code == 200
        consulta = results.json()
        data= consulta.get("data")
        cantidad_to = data.get("quote").get(To).get("price")
        return cantidad_to
      except Exception as e : 
        if type (e) == AttributeError: 
          Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
          print ("""Mensaje para el administrador: Error en la consulta a la API. Asegúrese que la información que contiene el endpoint es correcta.
          Su endpoint debería tener este aspecto: "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}".
          Donde los {} serán sustituidos por los valores a consultar 
          amount = <Cantidad que quiero invertir>,
          symbol = <Moneda que tengo>, 
          convert = <Moneda que quiero conseguir> y 
          CMC_PRO_API_KEY  = <Su Clave de Acceso a la Api>""" ) 
          return Error
        else: 
          Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
          print ("Mensaje para el administrador: Error al hacer una consulta a la API, el error es: >>{}<< ".format(e)) 
          return Error 
  except Exception as e : 
    Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
    print ("Mensaje para el administrador: Error al hacer una consulta a la API, el error es: >>{}<< ".format(e)) 
    return Error 
          
   

def busca_API_monedas ():
  URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY={}&symbol=BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX"

  url = URL.format(APIKEY)

  try:
      results = requests.get(url)
      try:
        results.status_code == 200
        consulta = results.json()
        data= consulta.get("data")
        return data 
      except Exception as e : 
        Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
        if type (e) == AttributeError: 
          print("""Mensaje para el administrador: Asegúrese que la información que contiene el endpoint es correcta.
            Su endpoint debería tener este aspecto: 
           'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY={}&symbol=BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX"'. 
           Donde el {}  tras CMC_PRO_API_KEY, será sustituido por  <Su Clave de Acceso a la Api> """)
          return Error 
        else: 
          Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
          print ("Mensaje para el administrador: Error al hacer una consulta a la API, el error es: >>{}<< ".format(e), type(e)) 
          return Error 
  except Exception as e : 
    Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
    print ("Mensaje para el administrador: Error al hacer una consulta a la API, el error es: >>{}<< ".format(e)) 
    return Error 