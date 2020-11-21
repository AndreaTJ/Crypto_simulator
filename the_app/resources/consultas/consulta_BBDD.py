from the_app import app
import sqlite3

BaseDatos = app.config['BASE_DATOS']

def consulta_a_BBDD (query, *tupla_datos):

    conn = sqlite3.connect(BaseDatos)
    cur = conn.cursor()
    try:
        consulta = cur.execute(query, *tupla_datos)
        conn.commit()
        return consulta

    except Exception as e:  
        print (" Mensaje para el administrador : Error al hacer una consulta a la Base de Datos, el error es: >>{}<< ".format(e))
        Error = "Se ha producido un error inesperado. Por favor, inténtelo de nuevo. Si el error persiste, por favor, contacte con el administrador."
        return Error 
    conn.close()


