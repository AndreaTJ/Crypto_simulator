# Simulador de Cryptos 

## Instalación 
1.Ejecutar
```
pip install -r requirements.txt
```

2.Crear config.py

* Renombrar `config_template.py` a `config.py` e informar correctamente sus claves.


3.Crear Base de Datos. 

*	Ejecutar `migrations.sql` con `sqlite3` en el 	fichero elegido como Base de Datos. 

4.Renombrar `config_template.ini` a `config.ini` e informar correctamente su APIKEY.

* Para obtener la APIKEY, visite [CoinMarketCap](https://coinmarketcap.com/api/). Existe un plan gratuito. 

5.Informar correctamente .env (solo para desarrollo)

Renombrar `.env_template` a `.env` e informar las claves

    - FLASK_APP=run.py
    - FLASK_ENV=`development` o `production``


6.Ejecutar 

```
python cargaMonedas.py
```

7.Ejecutar 

```
flask run
```


Por favor, recuerde que necesita conexión a Internet..
