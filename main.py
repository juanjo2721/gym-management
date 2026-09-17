from database import verificar_usuario

usuario = input("Usuario: ")
contrasena = input("Contraseña: ")

resultado = verificar_usuario(usuario, contrasena)

if resultado:
    print("Login correcto")
else:
    print("Usuario o contraseña incorrectos")