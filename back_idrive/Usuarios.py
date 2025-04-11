# Importamos las librerías necesarias de FastAPI, HTTPException y status
from fastapi import APIRouter, HTTPException, status, requests
# Importamos la clase BaseModel de pydantic
from pydantic import BaseModel
# Importamos las conexiones a MySQL desde Clever_MySQL_conn
from Clever_MySQL_conn import cleverCursor, mysqlConn
# Importar bcrypt para el manejo de contraseñas
import bcrypt  


usuariosRtr = APIRouter()

# Definimos una clase usuarioDB utilizando Pydantic para la validación de datos
class usuarioDB(BaseModel):
    nombre: str
    correo_electronico: str
    telefono: int
    cedula: str
    password: str
    id_rol: int
    

# Definimos una ruta GET para obtener la lista de usuarios

@usuariosRtr.get("/Usuarios/", status_code=status.HTTP_302_FOUND, tags=['Gestion de usuarios'])
async def get_users():
    # Consulta SQL para seleccionar el nombre y correo electrónico de los usuarios
    selectAll_query = 'SELECT nombre, correo_electronico, telefono, cedula, id_rol FROM Usuarios'
    # Ejecutamos la consulta utilizando cleverCursor
    cleverCursor.execute(selectAll_query)
    # Obtenemos todos los resultados de la consulta
    result = cleverCursor.fetchall()
    # Devolvemos los resultados obtenidos
    return result


# Definir un endpoint para obtener un rol por su 'id rol'

@usuariosRtr.get("/Usuarios/{id_rol}", status_code=status.HTTP_200_OK, tags=['Gestion de usuarios'])
def get_users_by_role(id_rol: int):
    select_query = """
    SELECT id_usuario, nombre, correo_electronico, telefono, cedula, id_rol 
    FROM Usuarios 
    WHERE id_rol = %s
    """
    
    cleverCursor.execute(select_query, (id_rol,))
    result = cleverCursor.fetchall()
    if result:
        return result
    
    raise HTTPException(status_code=404, detail="No se encontraron usuarios con ese rol")


# Endpoint para insertar un nuevo usuario en la base de datos con contraseña encriptada.

@usuariosRtr.post("/Crear_usuario/", status_code=status.HTTP_201_CREATED, tags=['Gestion de usuarios'])
def insert_user(usuarioPost: usuarioDB):
    # Verificar si el correo ya existe en la BD antes de insertar
    check_query = "SELECT id_usuario FROM Usuarios WHERE correo_electronico = %s"
    cleverCursor.execute(check_query, (usuarioPost.correo_electronico,))
    if cleverCursor.fetchone():
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

    # Hash de la contraseña antes de almacenarla
    hashed_password = bcrypt.hashpw(usuarioPost.password.encode("utf-8"), bcrypt.gensalt())

    insert_query = """
    INSERT INTO Usuarios (nombre, correo_electronico, telefono, cedula, password_hash, id_rol)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (usuarioPost.nombre, usuarioPost.correo_electronico, usuarioPost.telefono, usuarioPost.cedula, hashed_password.decode("utf-8"),  # Convertir hash a string
        usuarioPost.id_rol
    )

    try:
        cleverCursor.execute(insert_query, values)  # Ejecutar consulta
        mysqlConn.commit()  # Guardar cambios en la BD
        
        # Obtener el ID del usuario creado
        user_id = cleverCursor.lastrowid

        return {"message": "Usuario creado correctamente"}

    except mysqlConn.connector.Error as err:
        mysqlConn.rollback()  #

 
#Endpoint para editar usuario

@usuariosRtr.put("/Editar_usuario/{usuario_id}", status_code=status.HTTP_200_OK, tags=['Gestion de usuarios'])
def update_user(usuario_id: int, usuarioPut: usuarioDB):

    # Obtener el usuario actual para verificar si existe
    cleverCursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (usuario_id,))
    usuario_existente = cleverCursor.fetchone()

    if not usuario_existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Si el usuario envió una nueva contraseña, la encriptamos
    hashed_password = bcrypt.hashpw(usuarioPut.password.encode("utf-8"), bcrypt.gensalt()) if usuarioPut.password else usuario_existente[5]

    update_query = """
    UPDATE Usuarios 
    SET nombre = %s, correo_electronico = %s, telefono = %s, cedula = %s, password_hash = %s, id_rol = %s
    WHERE id_usuario = %s
    """

    values = (usuarioPut.nombre, usuarioPut.correo_electronico, usuarioPut.telefono, usuarioPut.cedula, hashed_password, usuarioPut.id_rol, usuario_id)

    try:
        cleverCursor.execute(update_query, values)
        mysqlConn.commit()

        if cleverCursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="No se realizaron cambios en el usuario")

    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error en la base de datos: {err}")

    return {"message": "Usuario actualizado correctamente"}



#Endpoint para eliminar usuario por id

@usuariosRtr.delete("/Borrar_usuario/{id_usuario}", status_code=status.HTTP_200_OK, tags=['Gestion de usuarios'])
def delete_clases_by_id(id_usuario: int):
    delete_query = "DELETE FROM Usuarios WHERE id_usuario = %s"
    values = (id_usuario,)

    try:
        cleverCursor.execute(delete_query, values)
        mysqlConn.commit()

        if cleverCursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Error en la eliminación: {err}")

    return {"message": "Usuario eliminado correctamente."}

#Endpoint para validar el correo y la contraseña del login

class LoginRequest(BaseModel):
    correo_electronico: str
    password: str

@usuariosRtr.post("/Validacion_Login/", status_code=status.HTTP_200_OK, tags=['Gestion de login'])
def validar_login(data: LoginRequest):
    select_query = """
    SELECT id_usuario, nombre, correo_electronico, telefono, cedula, id_rol, password_hash
    FROM Usuarios 
    WHERE correo_electronico = %s
    """

    try:
        cleverCursor.execute(select_query, (data.correo_electronico,))
        result = cleverCursor.fetchone()

        if result:
            stored_password_hash = result[6]  # La contraseña en la BD

            # Validamos con bcrypt
            if bcrypt.checkpw(data.password.encode("utf-8"), stored_password_hash.encode("utf-8")):
                return {
                    "id_usuario": result[0],
                    "nombre": result[1],
                    "correo_electronico": result[2],
                    "telefono": result[3],
                    "cedula": result[4],
                    "id_rol": result[5],
                    "message": "Bienvenido"
                }
            else:
                raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
        else:
            raise HTTPException(status_code=404, detail="Correo o contraseña incorrectos")

    except mysqlConn.Error as err:
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {err}")