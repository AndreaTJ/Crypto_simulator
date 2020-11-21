from the_app import app
from the_app.forms import PurchaseForm
from flask import render_template, request, redirect, url_for
from the_app.resources.funciones.funciones import GestionarMovimientos, CalidadInsercion, ValidarDatosAntesCompra, CalcularCantidadPrecio,  CargarNuevasMonedasFrom, ConsultarEurosInvertidos, CalcularSaldoEuros, GetDatosCryptosPositivas, Calcula_Inversion_atrapada, Gestionarerrores

Euros = app.config['EUROS']
Cryptos = app.config['CRYPTOMONEDAS']

@app.route("/") 
def index():
            
    BuenResultado, Movimientos = GestionarMovimientos () 
    if BuenResultado: 
        if Movimientos != 0: 
            return render_template('movimientos.html', movimientos = Movimientos)
        else: 
            return render_template('movimientos.html') 
    else:
        Error = Movimientos
        print ("Mensaje para el administrador: El error en la consulta en la BBDD se ha dado en la ruta / al ejecutar la función GestionarMovimientos")
        return render_template('movimientos.html', error_BBDD = Error)
          

@app.route("/purchase", methods=['GET', 'POST']) 
def compra():
    form = PurchaseForm()
    CargarNuevasMonedasFrom (form, Euros, Cryptos)    

    if request.method == 'GET':
        return render_template('compras.html', form=form)
        
    else: 
        if request.form.get('calcular'):
            if form.validate():
                BuenaConsulta, Valor = CalcularCantidadPrecio (request.values, form)
                if BuenaConsulta: 
                    Qto_consultada, precio_unitario = Valor 
                    return render_template('compras.html', form=form,  Cantidad_Conseguida=Qto_consultada, PU = precio_unitario)
                else:
                    Error = Valor 
                    return render_template('compras.html', form=form, errorApi = Error)

            else: 
                return render_template('compras.html', form=form)
        else: 
            
            HayError, Error= ValidarDatosAntesCompra (form)
            if HayError: 
                return render_template('compras.html', form=form,  error_Datos  = Error) 
            else: 
                if form.validate(): 
                    BuenaInsercion, Valor = CalidadInsercion (request.values)
                    if BuenaInsercion:
                        return redirect(url_for("index"))
                    else: 
                        Error = Valor 
                        return render_template('compras.html', form=form, error_BBDD = Error )
                else: 
        
                    return render_template('compras.html', form=form)
    
@app.route("/status") 
def estado():
    if request.method == 'GET':
        
        ConsultaBBDDok, Valor = ConsultarEurosInvertidos (Euros)
        ConsultaBBDDok2, Valor2 = CalcularSaldoEuros(Euros)
        Correcto, Valor3 =  GetDatosCryptosPositivas (Cryptos, Euros)
        
        
        if ConsultaBBDDok and ConsultaBBDDok2 and Correcto: 
              
            Total_Euros_Invertidos = Valor
            Saldo_Euros_Invertidos = Valor2
            DatosCryptos = Valor3   
        
        else: 
            Error = Gestionarerrores (Valor, Valor2, Valor3)
            return render_template ('status.html', Errores = Error)
        
        Inversion_atrapada = Calcula_Inversion_atrapada (DatosCryptos)
        Valor_Actual = Total_Euros_Invertidos +  Saldo_Euros_Invertidos+ Inversion_atrapada
        return render_template('status.html', invertido = Total_Euros_Invertidos, valorActual = Valor_Actual,  SaldosCryto = DatosCryptos, Saldo_Euros= Saldo_Euros_Invertidos, Inversion_atrapada = Inversion_atrapada) 
   