import sqlite3 

# El \ se conoce como caracter de escape, se usa para construir códigos especiales
# \n, \t, C:\sqlite3\db\c03.db  ==> \s    \d     \c
# \\  ==> C:\sqlite3\db\c03.db
# /sqlite3/db/c03.db
#

def conectar():
    try:
        #sal = sqlite3.connect('C:\\Users\\Usuario\\PycharmProjects\\Reto Semanal 4\\cafeteria.db')
        sal = sqlite3.connect('cafeteria.db')

    except Exception as ex:
        sal = None
        print(ex)
    return sal  

def desconectar(con):
    try:
        con.close()
    finally:
        con = None
    return con

def ejecutar_consulta_sel(con,sql):
    try:
        cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
        sal = cur.execute(sql).fetchall()
    except Exception as ex:
        sal = None
        print(ex)
    return sal

def ejecutar_consulta_acc(con,sql,datos):
    try:
        cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
        sal = cur.execute(sql,datos)
        con.commit()
    except Exception as ex:
        sal = 0
        print(ex)
    return


def actualizar(con,sql,datos):
    try:
        cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
        sal = cur.execute(sql)
        con.commit()
    except Exception as ex:
        sal = 0
        print(ex)
    return sal

def eliminar(con,sql):
    try:
        cur = con.cursor()                  # Crea un cursor (un lugar para almacenar los resultados de la consulta)
        sal = cur.execute(sql,datos)
        con.commit()
    except Exception as ex:
        sal = 0
        print(ex)
    return
