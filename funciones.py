
from sqlalchemy import text
import config as c # Importamos la función que devuelve el engine

def insertar_usuario(nombre, email, password):
    """
    Inserta un nuevo usuario en la base de datos, asociando su nombre, email, contraseña hash y la fecha de registro actual.
    También devuelve el id_usuario del usuario insertado.

    Parámetros:
    nombre (str): Nombre del usuario.
    email (str): Email del usuario.
    password (str): Contraseña en texto plano del usuario.

    Retorna:
    id_usuario (int): El id del usuario recién insertado.
    """
    import bcrypt
    try:
        # Generar el hash de la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Obtener el engine utilizando la función get_db_engine()
        engine = c.get_db_engine()  # Cambiar c.engine por c.get_db_engine()

        # Establece la conexión con la base de datos
        with engine.connect() as connection:  # Usamos `.connect()` para la conexión
            # Consulta SQL para insertar un nuevo usuario con la fecha actual
            query = text("""
                INSERT INTO usuarios (nombre, email, password, fecha_registro) 
                VALUES (:nombre, :email, :password, CURDATE())
            """)
            # Ejecutamos la consulta con los parámetros proporcionados
            result = connection.execute(query, {
                "nombre": nombre,
                "email": email,
                "password": hashed_password.decode('utf-8')  # Convertimos a string para almacenar en la DB
            })

            # Obtenemos el id del usuario recién insertado
            id_usuario = result.lastrowid  # `lastrowid` obtiene el último id generado
            print(f"Usuario {nombre} agregado exitosamente con el id {id_usuario}.")
            return id_usuario  # Retorna el id del usuario

    except Exception as e:
        print(f"Error al insertar el usuario: {e}")
        return None  # Retorna None si hubo un error






def insertar_preferencia(id_usuario, tipo_viaje, actividades, duracion_viaje):
    """
    Inserta las preferencias de un usuario en la base de datos.

    Parámetros:
    id_usuario (int): El id del usuario al que pertenecen las preferencias.
    tipo_viaje (str): El tipo de viaje del usuario (ej. 'Solo', 'Familia', etc.).
    actividades (list): Lista de actividades que el usuario prefiere (ej. ['Cultura', 'Aventura']).
    duracion_viaje (int): Duración del viaje en días.
    """
    try:
        with c.engine.connect() as connection:
            # Convertimos la lista de actividades a un formato adecuado para SQL
            actividades_str = ', '.join(actividades)
            
            # Consulta SQL para insertar las preferencias del usuario
            query = text("""
                INSERT INTO preferencias (id_usuario, tipo_viaje, actividades, duracion_viaje)
                VALUES (:id_usuario, :tipo_viaje, :actividades, :duracion_viaje)
            """)
            
            # Ejecutamos la consulta con los parámetros proporcionados
            connection.execute(query, {
                "id_usuario": id_usuario,
                "tipo_viaje": tipo_viaje,
                "actividades": actividades_str,
                "duracion_viaje": duracion_viaje
            })
            print(f"Preferencias de usuario {id_usuario} guardadas con éxito.")
    except Exception as e:
        print(f"Error al insertar las preferencias: {e}")


def buscar_lugares_por_actividades(nombre_lugar, actividades, radio=1000):
    """
    Busca lugares cercanos basados en las actividades seleccionadas por el usuario.

    Parámetros:
    - nombre_lugar (str): Nombre del lugar (por ejemplo, "Buenos Aires").
    - actividades (list): Lista de actividades seleccionadas por el usuario.
    - radio (int): Radio de búsqueda en metros.

    Retorna:
    - dict: Resultados de los lugares encontrados.
    """
    import requests
    try:
        # Mapeo entre actividades y categorías de Foursquare (dentro de la función)
        CATEGORIAS_FOURSQUARE = {
            "Cultura": "10027,10032",  # Museos, sitios históricos
            "Aventura": "16014,16021",  # Parques nacionales, actividades al aire libre
            "Relax": "13035",  # Spas y centros de relajación
            "Deportes": "18018,18020",  # Estadios deportivos, gimnasios
            "Gastronomía": "13065",  # Restaurantes
            "Party": "19019,19020",  # Bares, clubes nocturnos
        }

        # Convertir actividades en categorías de Foursquare
        categorias = []
        for actividad in actividades:
            if actividad in CATEGORIAS_FOURSQUARE:
                categorias.append(CATEGORIAS_FOURSQUARE[actividad])

        # Unir categorías en un string separado por comas
        categorias_str = ",".join(categorias)

        # Endpoint de búsqueda de Foursquare
        url_busqueda = "https://api.foursquare.com/v3/places/search"

        # Configurar parámetros de la solicitud
        params = {
            "query": nombre_lugar,
            "radius": radio,
            "categories": categorias_str,  # Categorías basadas en actividades
            "limit": 10
        }

        # Encabezados de autorización
        headers = {
            "Authorization": c.FOURSQUARE_API_KEY
        }

        # Realizar la solicitud
        response = requests.get(url_busqueda, headers=headers, params=params)

        # Comprobar el estado de la respuesta
        if response.status_code == 200:
            return response.json()  # Retornar resultados como JSON
        else:
            print(f"Error en la solicitud: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error en buscar_lugares_por_actividades: {e}")
        return None

