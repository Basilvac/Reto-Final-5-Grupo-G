import sqlite3, db
import yagmail as yagmail# Servidor de correo
import os #Libreria para llave secreta para enviar correo
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from markupsafe import escape  # Seguridad, evitar inyeccion
from werkzeug.security import generate_password_hash, check_password_hash #libreria del hash de seguridadd


app = Flask(__name__)

app.secret_key = os.urandom(24)


# FUNCION PARA MANEJO DE SESIONES
def verificaion_login(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect('/')
        return view(**kwargs)
    return wrapped_view

# RUTAS DEL ADMINISTRADOR

@app.route('/', methods=["GET","POST"])
def inicio():
    if request.method == "POST":
        con = db.conectar()               #Variable para conectar la base de datos
        usuario = request.form['txtNombre']
        clave = request.form['txtCla']
        seleccion = request.form['radio']
        boton = request.form['sb']
        if boton=="Entrar al Sistema" and seleccion=="Si":
            if con!=None:
                res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE id_usuario = '" + usuario + "'")
                db.desconectar(con)           
                if res!=None:        
                    for fila in res:
                        if fila[2] == usuario:
                            return redirect('/administrador')
                        else:
                            return redirect('/')    
                else:
                    return redirect('/')
            else:
                print('Error de conexion')
#            return redirect('/administrador')
            return redirect('/')
        elif boton=="Entrar al Sistema" and seleccion=="No":
            return redirect('/usuarioExterno')
        elif boton=="Recuperar Clave":
            return redirect('/recuperarClave')

    else:
        return render_template("Inicio.html")

@app.route('/administrador', methods=["GET","POST"])
def menuAdmin():
    if request.method == "POST":
        seleccion = request.form['radio']
        boton = request.form['sb']
        if boton=="Ingresar" and seleccion=="adminUsr":
            return redirect('/opcionesUsuario/')
        elif boton=="Ingresar" and seleccion=="adminPrd":
           return redirect('administrarProductos')
    else:
        return render_template("Funciones Administrador.html")

@app.route('/opcionesUsuario/', methods=["GET","POST"])
def opcionesUsr():
    if request.method == "POST":
        valor = request.form['radio']
        boton = request.form['sb']
        if valor=="registrar" and boton=="Ingresar":
            return redirect('registrarUsuario')
        elif valor=="buscar" and boton=="Ingresar":
            return redirect('buscarUsuario')
    else:
        return render_template("Opciones Usuario.html")

@app.route('/opcionesUsuario/registrarUsuario', methods=["GET","POST"])
def registrarUsr(): #código con base de datos para registro
    if request.method == 'POST':
        con = db.conectar()
        nombre = request.form['txtNombre']
        id_usuario = request.form['txtID']
        usuario = request.form['txtLog']
        correo = request.form['txtCorreo']
        esAdmin = request.form['check']
        admin = "FALSE"
        if esAdmin == "si":
            admin = "TRUE"
        if esAdmin == "no":
            admin = "FALSE"    
        pwd1 = request.form['txtCla']
        pwd2 = request.form['txtVerCla']
        if pwd1 == pwd2:
            sql = "INSERT INTO usuarios (identificacion,nombre,id_usuario,correo,clave,administrador) VALUES (?,?,?,?,?,?)"
            db.ejecutar_consulta_acc(con,sql,(id_usuario,nombre,usuario,correo,pwd1,admin,))
            db.desconectar(con)
            return redirect('/administrador')
        else:
            return render_template('Registrar Usuario.html')

    else:
        return render_template('Registrar Usuario.html')

@app.route('/opcionesUsuario/buscarUsuario/', methods=["GET","POST"])
def buscarUsr():
    if request.method == "POST":
        boton = request.form['sb']
        if boton == "Buscar":
            return redirect('/Buscar Usuario.html/')
        elif boton == "Modificar":
            return redirect('/modificarUsuario/')
        elif boton == "Eliminar":
            return redirect('/modificarUsuario/')
    else:

        return render_template('Buscar Usuario.html')



#####Mostrar lista dinámica de la busqueda
@app.route('/mostrarUsuario', methods=["POST"])
def mostrarUsuario():
    if request.method == 'POST':
        texto = request.form['texto']
        radio = request.form['radio']
        con = db.conectar()               #Variable para conectar la base de datos
        print(texto)
        print(radio)
        if radio == "nombre":
#            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE nombre = '"+ texto +"'")
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE nombre LIKE '%"+ texto +"%'")
            db.desconectar(con)  
        elif radio == "usuario":
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE id_usuario = '"+ texto +"'")
            db.desconectar(con)
        elif radio == "id":
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE identificacion = '"+ texto +"'")
            db.desconectar(con)
        elif radio == "correo":
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE correo = '"+ texto +"'")
            db.desconectar(con)
    print(res)
    return render_template('Buscar Usuario.html', usuarios = res)

####CARGAR DATOS EN LOS TEXTOS DEL HTML
@app.route('/editar/<string:id>')
def editar_contact(id):
    con = db.conectar()               #Variable para conectar la base de datos
    res = db.ejecutar_consulta_sel(con, 'SELECT * FROM usuarios WHERE identificacion = {0}'.format(id))
 #   sql = 'UPDATE usuarios SET identificacion =, nombre =, id_usuario = , correo = , clave = , administrador =, WHERE id = {0}'.format(id)
 #   db.editar(con,sql)
    print(res[0])
    db.desconectar(con)           
 #   return redirect('/modificarUsuario/', usuario = res[0])
    return render_template('Modificar Usuario.html', usuario = res[0])

#Actualizar información, corregir la sentencia SQL
@app.route('/modificarUsuario/<id>', methods=["GET","POST"])
def modificarUsr(id):
    if request.method == "POST":
        nombre = request.form['txtNombre']
        id_usuario = request.form['txtID']
        usuario = request.form['txtLog']
        correo = request.form['txtCorreo']
        esAdmin = request.form['check']
        admin = "FALSE"
        if esAdmin == "si":
            admin = "TRUE"
        if esAdmin == "no":
            admin = "FALSE"    
        pwd1 = request.form['txtCla']
        pwd2 = request.form['txtVerCla']
        actualiza = request.form['sb']
        con = db.conectar()               #Variable para conectar la base de datos
 #       sql = 'UPDATE usuarios SET identificacion = ?, nombre = ?, id_usuario = ?, correo = ?, clave = ?, administrador = ? WHERE idetificacion = {0}'.format(id)
 #       db.actualizar(con,sql,(id_usuario,nombre,usuario,correo,pwd1,admin,))
 #       db.desconectar(con)  
        if pwd1 == pwd2:
            if actualiza == "Actualizar":
                sql =  "UPDATE usuarios SET identificacion = ?, nombre = ?, id_usuario = ?, correo = ?, clave = ?, administrador = ? WHERE identificacion = '"+ id +"'"##info de la base de datos
                db.ejecutar_consulta_acc(con,sql,(id_usuario,nombre,usuario,correo,pwd1,admin,))
                db.desconectar(con)
        return redirect('/opcionesUsuario/buscarUsuario/')
#    return render_template('Modificar Usuario.html')

#Eliminar usuario
@app.route('/eliminarUsuario/<id>')
####CARGAR DATOS EN LOS TEXTOS DEL HTML
def eliminar_contact(id):
    con = db.conectar()               #Variable para conectar la base de datos
 #   res = db.eliminar(con, 'DELETE * FROM usuarios WHERE identificacion = {0}'.format(id))
    res = db.ejecutar_consulta_acc(con, 'DELETE FROM usuarios WHERE identificacion = ?',(id,))
    print(id)
 #   sql = 'UPDATE usuarios SET identificacion =, nombre =, id_usuario = , correo = , clave = , administrador =, WHERE id = {0}'.format(id)
 #   db.editar(con,sql)
    db.desconectar(con)           
 #   return redirect('/modificarUsuario/', usuario = res[0])
    return redirect('/opcionesUsuario/buscarUsuario/')

### OPCIONES DE USUARIO

@app.route('/usuario', methods=["GET","POST"])
def menuUsr():
    if request.method == "POST":
        seleccion = request.form['radio']
        boton = request.form['sb']
        if boton=="Ingresar" and seleccion=="registrar":
            return redirect('/registrar/')
        elif boton=="Ingresar" and seleccion=="buscar":
           return render_template('administrarProductos')
    else:
        return render_template("Opciones Producto.html")

@app.route('/administrarProductos/', methods=["GET","POST"])
def administrarProductos():
    if request.method == "POST":
        valor = request.form['radio']
        boton = request.form['sb']
        if valor=="registrar" and boton=="Ingresar":
            return redirect('/registrarProducto/')
        elif valor=="buscar" and boton=="Ingresar":
            return redirect('/buscarProductoAdministrador/')
    else:
        return render_template("administrarProductos.html")

###################
@app.route('/administrarProductosUsuario/', methods=["GET","POST"])
def administrarProductosUsr():
    if request.method == "POST":
        valor = request.form['radio']
        boton = request.form['sb']
        if valor=="registrar" and boton=="Ingresar":
            return redirect('/registrarProducto/')
        elif valor=="buscar" and boton=="Ingresar":
            return redirect('/buscarProductoUsuarioExterno/')
    else:
        return render_template("administrarProductosUsuario.html")


@app.route('/registrarProducto/', methods=["GET","POST"])
def registrarProductoAdministrador():

    if request.method == 'POST':
        con = db.conectar()
        id_producto = request.form['idProducto']
        nombre_producto = request.form['nombreProducto']
        cantidad_producto = request.form['cantidadProducto']
        verificar_cantidad = request.form['VerificarCantidad']
        descripcion_producto = request.form['descripcionProducto']
        imagen_producto = request.form['ImagenProducto']

        if cantidad_producto == verificar_cantidad:
            sql = "INSERT INTO productos (id_producto,nombre,cantidad,Descripcion,imagen) VALUES (?,?,?,?,?)"
            db.ejecutar_consulta_acc(con,sql,(id_producto,nombre_producto,cantidad_producto,descripcion_producto,imagen_producto))
            db.desconectar(con)
            return redirect('/administrador')
        else:
            return render_template('registrarProducto.html')

    else:
        return render_template('registrarProducto.html')

@app.route('/buscarProductoAdministrador/', methods=["GET","POST"])
def buscarProductoAdministrador():
    if request.method == "POST":
        boton = request.form['sb']
        if boton == "Buscar":
            return redirect('/buscarProductoAdministrador.html/')
        elif boton == "Modificar":
            return redirect('/modificarUsuario/')
        elif boton == "Eliminar":
            return redirect('/modificarUsuario/')
    else:

        return render_template('buscarProductoAdministrador.html')

#####Mostrar lista dinámica de la busqueda
@app.route('/mostrarProducto', methods=["POST"])
def mostrarProducto():
    if request.method == 'POST':
        texto = request.form['texto']
        radio = request.form['radio']
        con = db.conectar()  # Variable para conectar la base de datos
        print(texto)
        print(radio)
        if radio == "nombre":
            #            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE nombre = '"+ texto +"'")
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM productos WHERE nombre LIKE '%" + texto + "%'")
            db.desconectar(con)
        elif radio == "id":
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM productos WHERE id_producto = '" + texto + "'")
            db.desconectar(con)

    print(res)
    return render_template('buscarProductoAdministrador.html', productos = res)
#    return render_template('Usuario Buscar Producto.html', productos = res)


####CARGAR DATOS EN LOS TEXTOS DEL HTML
@app.route('/editarProducto/<string:id>')
def editar_contact_producto(id):
    con = db.conectar()               #Variable para conectar la base de datos
    res = db.ejecutar_consulta_sel(con, 'SELECT * FROM productos WHERE id_producto = {0}'.format(id))
 #   sql = 'UPDATE usuarios SET identificacion =, nombre =, id_usuario = , correo = , clave = , administrador =, WHERE id = {0}'.format(id)
 #   db.editar(con,sql)
    print(res[0])
    db.desconectar(con)
 #   return redirect('/modificarUsuario/', usuario = res[0])
    return render_template('Modificar Producto.html', producto = res[0])

@app.route('/editarProductoUsuario/<string:id>')
def editar_producto_usr(id):
    con = db.conectar()               #Variable para conectar la base de datos
    res = db.ejecutar_consulta_sel(con, 'SELECT * FROM productos WHERE id_producto = {0}'.format(id))
 #   sql = 'UPDATE usuarios SET identificacion =, nombre =, id_usuario = , correo = , clave = , administrador =, WHERE id = {0}'.format(id)
 #   db.editar(con,sql)
    print(res[0])
    db.desconectar(con)
 #   return redirect('/modificarUsuario/', usuario = res[0])
    return render_template('Modificar Producto Usuario.html', producto = res[0])


#Actualizar información, corregir la sentencia SQL
@app.route('/modificarProducto/<id>', methods=["GET","POST"])
def modificarProducto(id):
    if request.method == 'POST':
        con = db.conectar()
        id_producto = request.form['txtID']
        nombre_producto = request.form['txtNombre']
        cantidad_producto = request.form['cantidadProducto']
        verificar_cantidad = request.form['VerificarCantidad']
        descripcion_producto = request.form['descripcionProducto']
        imagen_producto = request.form['ImagenProducto']

        actualiza = request.form['sb']
        con = db.conectar()  # Variable para conectar la base de datos
        print(imagen_producto)    
        if cantidad_producto == verificar_cantidad:
            if actualiza == "Actualizar":
                #               sql = "UPDATE usuarios SET identificacion = '" + id_usuario + "', nombre = '"+ nombre +"', id_usuario = '"+ id_usuario +"', correo = '"+ correo +"', clave = '"+ pwd1 +"', administrador = "+ admin +" WHERE identificacion = {0}".format(id) ##info de la base de datos
                if imagen_producto.strip() != None :
                    sql = "UPDATE productos SET id_producto = ?, nombre = ?, cantidad = ?, Descripcion = ?, imagen = ? WHERE id_producto = '"+ id +"'"  ##info de la base de datos
                    db.ejecutar_consulta_acc(con, sql, (id_producto, nombre_producto, cantidad_producto, descripcion_producto, imagen_producto,))
                elif imagen_producto == " ":
                    sql = "UPDATE productos SET id_producto = ?, nombre = ?, cantidad = ?, Descripcion = ? WHERE id_producto = '"+ id +"'"  ##info de la base de datos
                    db.ejecutar_consulta_acc(con, sql, (id_producto, nombre_producto, cantidad_producto, descripcion_producto,))
                db.desconectar(con)
        return redirect('/administrarProductos/')
#    return render_template('Modificar Producto.html')

@app.route('/modificarProductoUsuario/<id>', methods=["GET","POST"])
def modificarProductoUsr(id):
    if request.method == 'POST':
        con = db.conectar()
        id_producto = request.form['txtID']
        nombre_producto = request.form['txtNombre']
        cantidad_producto = request.form['cantidadProducto']
        verificar_cantidad = request.form['VerificarCantidad']
        descripcion_producto = request.form['descripcionProducto']
        imagen_producto = request.form['ImagenProducto']

        actualiza = request.form['sb']
        con = db.conectar()  # Variable para conectar la base de datos
        print(imagen_producto)    
        if cantidad_producto == verificar_cantidad:
            if actualiza == "Actualizar":
                #               sql = "UPDATE usuarios SET identificacion = '" + id_usuario + "', nombre = '"+ nombre +"', id_usuario = '"+ id_usuario +"', correo = '"+ correo +"', clave = '"+ pwd1 +"', administrador = "+ admin +" WHERE identificacion = {0}".format(id) ##info de la base de datos
                if imagen_producto.strip() != None :
                    sql = "UPDATE productos SET id_producto = ?, nombre = ?, cantidad = ?, Descripcion = ?, imagen = ? WHERE id_producto = '"+ id +"'"  ##info de la base de datos
                    db.ejecutar_consulta_acc(con, sql, (id_producto, nombre_producto, cantidad_producto, descripcion_producto, imagen_producto,))
                elif imagen_producto == " ":
                    sql = "UPDATE productos SET id_producto = ?, nombre = ?, cantidad = ?, Descripcion = ? WHERE id_producto = '"+ id +"'"  ##info de la base de datos
                    db.ejecutar_consulta_acc(con, sql, (id_producto, nombre_producto, cantidad_producto, descripcion_producto,))
                db.desconectar(con)
        return redirect('/administrarProductosUsuario/')


# RUTAS DEL USUARIO EXTERNO

@app.route('/usuarioExterno/', methods=["GET","POST"])
def menuUsuarioExterno():
    if request.method == "POST":
        seleccion = request.form['radio']
        boton = request.form['sb']
        if boton=="Ingresar" and seleccion=="Buscar Productos":
            return redirect('/buscarProductoUsuarioExterno/')
        elif boton=="Ingresar" and seleccion=="Cambiar clave":
           return redirect('/cambiarClave')

    else:
        return render_template("menuUsuarioExterno.html")

@app.route('/buscarProductoUsuarioExterno/', methods=["GET", "POST"])
def buscarProductoUsuarioExterno():
    if request.method == "POST":
        boton = request.form['sb']
        if boton == "Buscar":
            return redirect('/Usuario Buscando Productos.html/')

    else:

        return render_template('Usuario Buscando Productos.html')


@app.route('/mostrarProductoUsuario', methods=["POST"])
def mostrarProductoUsuario():
    if request.method == 'POST':
        texto = request.form['texto']
        radio = request.form['radio']
        con = db.conectar()  # Variable para conectar la base de datos
        print(texto)
        print(radio)
        if radio == "nombre":
            #            res = db.ejecutar_consulta_sel(con, "SELECT * FROM usuarios WHERE nombre = '"+ texto +"'")
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM productos WHERE nombre LIKE '%" + texto + "%'")
            db.desconectar(con)
        elif radio == "id":
            res = db.ejecutar_consulta_sel(con, "SELECT * FROM productos WHERE id_producto = '" + texto + "'")
            db.desconectar(con)

    print(res)
    return render_template('Usuario Buscando Productos.html', productos = res)

@app.route('/recuperarClave/', methods=["GET","POST"])   
def recuperarClave():
    try:
        if request.method == "POST":
            email = request.form['email']
            serverEmail = yagmail.SMTP('sub2grupog@gmail.com','GrupoG1234')
            serverEmail.send(to=email, subject='Reestablecer contraseña', contents='Haz clic en el siguiente link para reestablecer contraseña http://127.0.0.1:5000/cambiarClave/')
            print('Se envió el correo')
            flash('Revisa tu correo para reestablecer tu contraseña')
        return render_template('recuperarClave.html')
    except Exception as e:
        print("Error es:", e)
        flash('No se envió el correo')
        return render_template('recuperarClave.html')


@app.route('/cambiarClave/', methods=["GET", "POST"])
def cambiarClave():
    try:
        if request.method == 'POST':
            clave_nueva = request.form['clavenueva']
            verificacion = request.form['verificacion']
            usuario = request.form['usuario']
            error = None
            if clave_nueva != verificacion:
                error = "Su clave nueva no concuerda"
                flash(error)
                print(error)
                return render_template('Nuevocambioclave.html')
            con = db.conectar()
            sql = "UPDATE usuarios SET clave = '" + clave_nueva + "' WHERE id_usuario = '" + usuario + "';"
            cursorObj = con.cursor()
            cursorObj.execute(sql)
            con.commit()
            db.desconectar(con)
            flash("Ha cambiado su contraseña con éxito")
            print("Ha cambiado su contraseña con éxito")
        return render_template('Nuevocambioclave.html')
    except Exception as e:
        print("Error es:", e)
        flash('No se cambió la clave')
        return render_template('Nuevocambioclave.html')

#Eliminar producto
@app.route('/eliminarProducto/<id>')
####CARGAR DATOS EN LOS TEXTOS DEL HTML
def eliminar_product(id):
    con = db.conectar()               #Variable para conectar la base de datos
 #   res = db.eliminar(con, 'DELETE * FROM usuarios WHERE identificacion = {0}'.format(id))
    res = db.ejecutar_consulta_acc(con, 'DELETE FROM productos WHERE id_producto = ?',(id,))
 #   sql = 'UPDATE usuarios SET identificacion =, nombre =, id_usuario = , correo = , clave = , administrador =, WHERE id = {0}'.format(id)
 #   db.editar(con,sql)
    db.desconectar(con)           
 #   return redirect('/modificarUsuario/', usuario = res[0])
    return render_template('buscarProductoAdministrador.html')

if __name__ == "__main__":
#    app.run(port='80',host='0.0.0.0')
    app.run(port='443',host='0.0.0.0',ssl_context=('certificate01.pem','llave01.pem'))
#    app.run(ssl_context=('certificate01.pem','llave01.pem'))