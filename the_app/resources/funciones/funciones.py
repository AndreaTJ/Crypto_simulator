from the_app.resources.consultas.consulta_BBDD import consulta_a_BBDD
from the_app.resources.consultas.consulta_API import busca_API_monedas, busca_API_cambio
from the_app import app 
import sqlite3
from datetime import datetime

def CargarMonedas (): 
    data = busca_API_monedas()
    if type(data) != list:
        print(" Mensaje para el administrador: No es posible, cargar las Crytomonedas en la base de datos por que hay un problema con la consulta a la API")
    else: 
        query = 'INSERT OR IGNORE into CRYPTOS (symbol, name) values (?, ?);'
        for indice in range (0, len(data)): 
            name = data[indice].get("name")
            symbol= data[indice].get("symbol")  
            datos = symbol, name
            consulta_BBdd = consulta_a_BBDD (query, datos)
        if type (consulta_BBdd) != sqlite3.Cursor: 
            print ( "Mensaje para el administrador: El error al realizar la consulta en la BBDD se ha producido al cargar las crytomonedas en la Tabla CRYPTOS") 
        else: 
            print (" Mensaje para el administrador: Las cryptomonedas se han cargados correctamente en la Tabla CRYPTOS de la BBDD")

def VerificarConsultaBBDD (Consulta):
    if type(Consulta)==str: 
        return False, Consulta
    else: 
        return True, Consulta

def GestionarMovimientos ():
    consultaOK, Valor = ContarMovimientosBBDD()
    if consultaOK: 
        Num_movimientos = Valor 
        if Num_movimientos == 0: 
            return True, Num_movimientos
        else: 
            consultaOK, Valor = ConsultarMovimientosBBDD()
            if consultaOK: 
                Movimientos_a_Mostrar = Valor 
                return True, Movimientos_a_Mostrar
            else:
                Error = Valor 
                return False, Error 
    else:
        Error = Valor 
        return False, Error

def ConsultarMovimientosBBDD (): 
    query = "SELECT date, time, from_currency, from_quantity, to_currency, to_quantity, from_quantity/to_quantity from MOVEMENTS;"
    Consulta= consulta_a_BBDD (query)
    consultaOK, Valor = VerificarConsultaBBDD (Consulta)
    if consultaOK:
        movimientos= Valor.fetchall()
        return consultaOK, movimientos
    else: 
        return consultaOK, Valor 
    
def ContarMovimientosBBDD (): 
    query = "SELECT COUNT(*) FROM MOVEMENTS;"
    Consulta = consulta_a_BBDD (query)
    consultaOK, Valor = VerificarConsultaBBDD (Consulta)
    if consultaOK: 
        cuenta = Valor.fetchone()
        Num_movimientos = cuenta[0]
        return consultaOK, Num_movimientos
    else: 
        return consultaOK, Valor


def CargarNuevasMonedasFrom (form, Euros, Cryptos):
    form.Moneda_from.choices= ListaMonedasSaldoPositivo([Euros], Cryptos) 
    return form.Moneda_from.choices

def CalcularCantidadPrecio (parametro, form): 
    datos = getDatosCalculadora (parametro)
    consulta = busca_API_cambio (datos[0], datos[1], datos[2])

    consultaOK, valor = VerificarConsultaAPI (consulta)
    if consultaOK:  
        Qto_consultada = valor
        precio_unitario = PrecioUnitario (parametro, Qto_consultada)
        GuardarValoresCamposOcultos (form, parametro,Qto_consultada)
        return True, [Qto_consultada, precio_unitario]
    else: 
        Error = valor 
        return False, Error  
def PrecioUnitario (parametro, Qto_consultada):
    precio_unitario= float((parametro.get('Cantidad_from')))/Qto_consultada
    return precio_unitario

def getDatosCalculadora (parametro):
    Cantidad_from = parametro.get('Cantidad_from')
    Moneda_from = parametro.get('Moneda_from')
    Moneda_to = parametro.get('Moneda_to')
    return Cantidad_from, Moneda_from, Moneda_to

def GuardarValoresCamposOcultos (form, parametro,Qto_consultada): 
    form.Cantidad_to.data = Qto_consultada
    form.ComprobacionMonedaFrom.data = parametro.get('Moneda_from')
    form.ComprobacionMonedaTo.data = parametro.get('Moneda_to')
    form.ComprobacionCantidadFrom.data  = float(parametro.get('Cantidad_from'))

def ValidarDatosAntesCompra (form): 
    if form.Cantidad_to.data == "": 
        Noconsulta = "BLIND transactions are not allowed. Please, check first the amount you will get (Q To) and the price (P.U.) at which the transaction will be made, by pressing the Calculator button."
        return True, Noconsulta
    elif form.Cantidad_from.data != float(form.ComprobacionCantidadFrom.data): 
        Error = "A change has been detected in the quantity queried, From {} to {}. To carry out the transaction with the new quantity: {}, first check the quantity that you will obtain (Q To) and the unit price, pressing the Calculator button".format (form.ComprobacionCantidadFrom.data, form.Cantidad_from.data,form.Cantidad_from.data)
        return True, Error 
    elif form.Moneda_from.data != form.ComprobacionMonedaFrom.data: 
        Error = "A change has been detected in the From Currency. From {} to {}. To carry out the transaction with the new currency: {}, please first check the amount you will get (Q To) and the unit price (P.U.) for this currency, by pressing the Calculator button".format(form.ComprobacionMonedaFrom.data,form.Moneda_from.data, form.Moneda_from.data )
        return True, Error 
    elif form.Moneda_to.data != form.ComprobacionMonedaTo.data: 
        Error= "A change has been detected in the To Currency. From {} to {}. To carry out the transaction with the new currency: {}, please first check the amount you will get (Q To) and the unit price (P.U.) for this currency, by pressing the Calculator button".format(form.ComprobacionMonedaTo.data,form.Moneda_to.data, form.Moneda_to.data )
        return True, Error 
    else:
        NohayError = "No hay Error"
        return False, NohayError
        
def DatosCompra (parametro): 
    ahora = datetime.now()
    fecha_hoy = ahora.strftime ("%d-%m-%Y")
    hora_hoy = ahora.strftime("%H:%M:%S.%f")[:-3]

    Moneda_from = parametro.get('Moneda_from')
    Cantidad_from = parametro.get('Cantidad_from')
    Moneda_to = parametro.get('Moneda_to')
    Cantidad_to = parametro.get('Cantidad_to')

    return (fecha_hoy, hora_hoy, Moneda_from, Cantidad_from, Moneda_to , Cantidad_to)


def InsertarCompraBBDD (parametro):
    query = "INSERT INTO MOVEMENTS(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES (?, ?, ?, ?, ?, ?);"
    datos = DatosCompra(parametro)
    Consulta= consulta_a_BBDD (query, datos)
    consultaOK, Valor = VerificarConsultaBBDD (Consulta)
    return consultaOK, Valor       

def CalidadInsercion (parametro): 
    consultaOK, valor = InsertarCompraBBDD(parametro)
    if consultaOK:
        return True, valor 
    else: 
        Error = valor 
        return False, valor  


def VerificarConsultaAPI (Consulta):
    if type(Consulta)==str: 
        return False, Consulta
    else: 
        return True, Consulta


def SaldosColumna (query,Moneda):   
    consultaBBDD = consulta_a_BBDD (query, (Moneda,))
    if type (consultaBBDD) ==str: 
        return consultaBBDD
    else: 
        SUM_Cantidad = consultaBBDD.fetchall() 

        if SUM_Cantidad[0][0] == None: 
            Suma_Cantidad = 0
            return Suma_Cantidad

        else: 
            Suma_Cantidad = SUM_Cantidad[0][0] 
            return Suma_Cantidad

def ConsultarEurosInvertidos (Euros): 
    query_Euros_Invertidos= "SELECT SUM(from_quantity) FROM MOVEMENTS where from_currency = ?;"
    Total_Euros_Invertidos = SaldosColumna (query_Euros_Invertidos, Euros)
    ConsultaOK, Resultado  = VerificarConsultaBBDD (Total_Euros_Invertidos)
    return ConsultaOK, Resultado

def Saldo_moneda (Moneda): 
    query_to = "SELECT SUM(to_quantity) FROM MOVEMENTS where to_currency = ?;"
    query_from= "SELECT SUM(from_quantity) FROM MOVEMENTS where from_currency = ?;"
    SaldoTotalTo =  SaldosColumna (query_to, Moneda)
    if type (SaldoTotalTo)== str: 
        return SaldoTotalTo 
    
    SaldoTotalFrom = SaldosColumna(query_from, Moneda)
    if type (SaldoTotalFrom)==str: 
        return SaldoTotalFrom
    
    if type (SaldoTotalTo) != str and type (SaldoTotalFrom) !=str:
        saldo_total = SaldoTotalTo - SaldoTotalFrom 
        return saldo_total 

def CalcularSaldoEuros (Euros):
    SaldoEuros = Saldo_moneda (Euros)
    ConsultaOK, Resultado = VerificarConsultaBBDD (SaldoEuros)
    return ConsultaOK, Resultado


def ConfirmarErrores (ListaValores):
    Errores = []
    for error, Mensaje in ListaValores: 
        if type(error) ==str:  
            print (Mensaje)
            Errores.append(error)
    return Errores 

def MostrarErrorUnaVez (Errores): 
    ErrorUnico = set(Errores)
    return ErrorUnico

def CambioMonedasSaldoPositivo (saldo,crypto, Euros): 
                    
    if saldo < 1e-8:   
        ConsultaAPIBien, Valor = GetCambio (1,crypto, Euros)
        if ConsultaAPIBien: 
            Cambio = Valor*saldo 
            return True, Cambio
        else: 
            Error = Valor
            return False, Error 
    else: 

        ConsultaAPIBien2, Valor2 = GetCambio (saldo, crypto, Euros)
        if ConsultaAPIBien2:
            Cambio = Valor2 
            return True, Cambio
        else: 
            Error = Valor2 
            return False, Error 


def GetCambio (saldo, crypto, Euros): 
    consulta = busca_API_cambio (saldo, crypto, Euros)
    ConsultaOK, Valor = VerificarConsultaAPI (consulta) 
    if ConsultaOK: 
        return True, Valor 
    else:
        Error = Valor 
        return False,Error


def GetDatosCryptosPositivas (Cryptos, Euros): 
    DatosCryptos = list()
    for crypto in Cryptos: 
        consulta = Saldo_moneda (crypto)
        ConsultaBien, Valor = VerificarConsultaBBDD(consulta)
        if ConsultaBien: 
            saldo = Valor 
            if saldo != 0:
                ConsultaOK, Valor = CambioMonedasSaldoPositivo (saldo,crypto, Euros)
                if ConsultaOK:
                    Cambio = Valor 
                    DatosCryptos.append ((crypto, saldo, Cambio))
                else: 
                    Error = Valor
                    return False, Error 
        else: 
            Error = Valor
            return False, Error 
    return True, DatosCryptos

def Gestionarerrores (Valor, Valor2, Valor3):
    MensajeV1 = "Mensaje para el administrador: El error al hacer una consulta a la Base de Datos se ha dado en Ruta /status al ejecutar la funcion ConsultarEurosInvertidos"
    MensajeV2 = "Mensaje para el administrador: El error al hacer una consulta a la Base de Datos se ha dado en Ruta /status al ejecutar la funcion CalcularSaldoEuros"
    MensajeV3 = "Mensaje para el administrador: El error al se ha dado en Ruta /status al ejecutar la funcion GetCryptosPositivas"
    PosiblesErrores = [(Valor, MensajeV1), (Valor2,MensajeV2), (Valor3, MensajeV3)]
    ListaErrores = ConfirmarErrores(PosiblesErrores)
    Error = MostrarErrorUnaVez (ListaErrores)        
    return Error  

    
def Calcula_Inversion_atrapada (DatosCryptos): 
    Suma = 0 
    for crypto, saldo, cambio in DatosCryptos: 
        Suma+=cambio 
    return Suma 



def saldo_positivo (Monedas): 
    MonedasSaldoPositivo = []
    for moneda in Monedas: 
        Saldo = Saldo_moneda (moneda)
        if type (Saldo) == str: 
            return Saldo
        else: 
            if Saldo > 0: 
                MonedasSaldoPositivo.append (moneda)
    return MonedasSaldoPositivo
    

def ListaMonedasSaldoPositivo (Moneda, Cryptomonedas):
    lista = list() 
    consulta = saldo_positivo (Cryptomonedas)
    if type (consulta) == str: 
        return consulta
    else: 
        ListaMonedas = Moneda + consulta
        for moneda in ListaMonedas:
            lista.append((moneda,moneda))
        return lista









if __name__ == "__main__":

    BaseDatos = "./the_app/data/BaseDatos.db"

    def consulta_a_BBDD (query, *tupla_datos):

        conn = sqlite3.connect(BaseDatos)
        cur = conn.cursor()
        try:
            consulta = cur.execute(query, *tupla_datos)
            conn.commit()
            return consulta

        except Exception as e:  
            Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
            print (" Mensaje para el administrador : Error al hacer una consulta a la Base de Datos, el error es: >>{}<< ".format(e))
            return Error 
        conn.close()

   