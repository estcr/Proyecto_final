import streamlit as st
from sqlalchemy import text
import openai
import config as c
import pinecone


def insertar_usuario(name, email, travel_style, registration_date):
    print(f"Intentando insertar usuario: {name}, {email}, {travel_style}, {registration_date}")
    conn = c.conectar_bd()
    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO users (name, email, travel_style, registration_date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (name, email, travel_style, registration_date))
        conn.commit()
        print("Usuario insertado correctamente")
    except Exception as e:
        print(f"Error al insertar datos en la base de datos: {e}, Datos: {name}, {email}, {travel_style}, {registration_date}")
        raise Exception(f"Error al insertar datos en la base de datos: {e}, Datos: {name}, {email}, {travel_style}, {registration_date}")
    finally:
        conn.close()
    
#---------------------------------------------------------------------------------------------------------------
def obtener_preferencias_usuario(user_id):
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        
        # Ejecutar la consulta para obtener las preferencias del usuario
        query = "SELECT activity_name, preference_level FROM user_activity_preferences WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        
        # Cerrar la conexión
        conn.close()
        
        if result:
            return result  # Retornar las preferencias del usuario
        else:
            return None
    except Exception as e:
        print(f"Error al obtener las preferencias del usuario: {e}")
        return None

def obtener_usuario_por_email(email):
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        query = "SELECT user_id FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        else:
            return None
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        return None

def insertar_preferencias_viaje(user_id, actividades):
    conn = c.conectar_bd()
    try:
        with conn.cursor() as cursor:
            for actividad, nivel in actividades.items():
                sql = """
                INSERT INTO user_activity_preferences (user_id, activity_name, preference_level)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (user_id, actividad, nivel))
        conn.commit()
    except Exception as e:
        raise Exception(f"Error al insertar preferencias de viaje en la base de datos: {e}")
    finally:
        conn.close()

def analizar_preferencias(destino, preferencias):
    openai.api_key = st.secrets["database"]["apigpt_key"]
    
    # Crear el prompt para la API de ChatGPT
    prompt = f"Analiza las siguientes preferencias del usuario para el destino {destino}: {preferencias}"
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    
    return response.choices[0].text.strip()

def generar_recomendaciones(destino, user_id):
    # Obtener las preferencias del usuario desde la base de datos
    preferencias = obtener_preferencias_usuario(user_id)
    
    if preferencias:
        # Analizar las preferencias usando la API de ChatGPT
        recomendaciones = analizar_preferencias(destino, preferencias)

        # Inicializar Pinecone
        pinecone.init(api_key=st.secrets["database"]["apipinecone"], environment=st.secrets["database"]["pinecone_env"])

        # Conectar a un índice de Pinecone
        index = pinecone.Index("tuguia")

        # Convertir las recomendaciones en un vector de consulta
        query_vector = [recomendaciones]

        # Buscar en el índice de Pinecone
        search_results = index.query(queries=query_vector, top_k=10, include_values=True)

        # Filtrar los resultados según el destino
        recomendaciones_filtradas = [result for result in search_results['matches'] if result['metadata']['destino'] == destino]

        # Retornar las recomendaciones
        return recomendaciones, recomendaciones_filtradas
    else:
        return None, None