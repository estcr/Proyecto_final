import bcrypt
from sqlalchemy import text

def insertar_usuario(nombre, email, password):
    """
    Inserta un nuevo usuario en la base de datos con su nombre, email, contraseña cifrada y la fecha de registro.
    """
    try:
        # Generar el hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Usar el engine para realizar la conexión
        with engine.begin() as connection:
            # Consulta SQL para insertar un nuevo usuario
            query = text("""
                INSERT INTO usuarios (nombre, email, password, fecha_registro)
                VALUES (:nombre, :email, :password, CURDATE())
            """)
            
            # Ejecutar la consulta
            result = connection.execute(query, {
                "nombre": nombre,
                "email": email,
                "password": hashed_password.decode('utf-8')  # Convertir el hash a string
            })
            
            # Obtener el id del usuario recién insertado
            id_usuario = result.lastrowid
            print(f"Usuario {nombre} insertado con éxito, ID: {id_usuario}")
            return id_usuario  # Retornar el id del usuario insertado

    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return None  # Retornar None si ocurre un error