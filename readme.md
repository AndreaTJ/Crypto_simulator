# Cryptocurrency Exchange Simulator

## Installation 
1.Run
```
pip install -r requirements.txt
```

2.Create config.py

* Rename `config_template.py` to `config.py` and fill in the information required. 


3.Create Database

*	Run  `migrations.sql` with `sqlite3` in the file chosen as the Database. 

4.Rename `config_template.ini` to `config.ini` and fill in the APIKEY.

* To obtain the APIKEY, visit: [CoinMarketCap](https://coinmarketcap.com/api/). There is a free plan available.  

5.Fill in the information required in .env (development only)

Rename `.env_template` to `.env` and copy the information below. 

    - FLASK_APP=run.py
    - FLASK_ENV=`development` or `production``


6.Run

```
python cargaMonedas.py
```

7.Run

```
flask run
```


An Internet connection is required. 
