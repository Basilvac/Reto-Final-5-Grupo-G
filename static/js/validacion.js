function validar_formulario_Inicio(){
    var usuario = document.formRegistro.txtNombre;
    var clave = document.formRegistro.txtCla;

    var usuario_len = usuario.value.length;
    if (usuario_len == 0 || userLen < 5) {
        alert("Debe ingresar un usuario con mínimo 5 caracteres incluyendo 1 Mayúscula, 1 Minúscula, 1 Caracter especial y 1 Número");
    } else {

        console.log("Paso prueba de usuario");
    }

    var passwdLen = clave.value.length;
    if (passwdLen ==0 || passwdLen<5) {
        alert("Debe ingresar un usuario con mínimo 5 caracteres incluyendo 1 Mayúscula, 1 Minúscula, 1 Caracter especial y 1 Número");
    } else {
        console.log("Paso prueba de la contraseña");
    }

}



