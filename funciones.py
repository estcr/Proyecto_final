import bcrypt
from sqlalchemy import text
import openai
import config as c


def insertar_usuario(nombre, email, fecha_registro, travel_style):
    conn = c.conectar_bd()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO usuarios (nombre, email, fecha_registro, travel_style) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (nombre, email, fecha_registro, travel_style))
        conn.commit()
    except Exception as e:
        raise Exception(f"Error al insertar datos en la base de datos: {e}")
    finally:
        conn.close()
    
#---------------------------------------------------------------------------------------------------------------
def obtener_preferencias_usuario(id_usuario):
    import pymysql
    import config as c 
    try:
        # Conectar a la base de datos
        conn = pymysql.connect(
            host=c.db_host,
            user=c.db_user,
            password=c.db_password,
            db=c.db_name
        )
        cursor = conn.cursor()
        
        # Ejecutar la consulta para obtener las preferencias del usuario
        query = "SELECT preferencias FROM usuarios WHERE id = %s"
        cursor.execute(query, (id_usuario,))
        result = cursor.fetchone()
        
        # Cerrar la conexión
        conn.close()
        
        if result:
            return result[0]  # Retornar las preferencias del usuario
        else:
            return None
    except Exception as e:
        print(f"Error al obtener las preferencias del usuario: {e}")
        return None

def insertar_preferencias_viaje(id_usuario, tipo_viaje, actividades, duracion_viaje):
    conn = c.conectar_bd()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO preferencias_viaje (id_usuario, tipo_viaje, actividades, duracion_viaje)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (id_usuario, tipo_viaje, ",".join(actividades), duracion_viaje))
        conn.commit()
    except Exception as e:
        raise Exception(f"Error al insertar preferencias de viaje en la base de datos: {e}")
    finally:
        conn.close()

def analizar_preferencias(destino, preferencias):
    openai.api_key = config["openai"]["api_key"]
    
    # Crear el prompt para la API de ChatGPT
    prompt = f"Analiza las siguientes preferencias del usuario para el destino {destino}: {preferencias}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

def generar_recomendaciones(destino, id_usuario):
    # Obtener las preferencias del usuario desde la base de datos
    preferencias = obtener_preferencias_usuario(id_usuario)
    
    if preferencias:
        # Analizar las preferencias usando la API de ChatGPT
        recomendaciones = analizar_preferencias(destino, preferencias)
        
        # Cargar la tabla vectorial
        tabla_vectorial = pd.read_csv("ruta/a/tu/archivo/vectorial.csv")
        
        # Filtrar la tabla vectorial según las recomendaciones
        recomendaciones_filtradas = tabla_vectorial[tabla_vectorial["destino"] == destino]
        
        # Retornar las recomendaciones
        return recomendaciones, recomendaciones_filtradas
    else:
        return None, None