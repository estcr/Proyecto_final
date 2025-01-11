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

def obtener_puntos_actividades(destino):
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        
        # Ejecutar la consulta para obtener puntos de actividades
        query = "SELECT actividad, descripcion FROM actividades WHERE destino = %s"
        cursor.execute(query, (destino,))
        result = cursor.fetchall()
        
        # Cerrar la conexión
        conn.close()
        
        if result:
            return result  # Retornar los puntos de actividades
        else:
            return None
    except Exception as e:
        print(f"Error al obtener puntos de actividades: {e}")
        return None



import openai

def vectorizar_actividades(actividades):
    from openai import OpenAI
    client= OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])
    
    embeddings = []
    for actividad in actividades:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=actividad,
            encoding_format="float")
        embeddings.append(response['data'][0]['embedding'])
    
    return embeddings


import pinecone
import numpy as np


# Initialize Pinecone
pc = pinecone.Pinecone(api_key=st.secrets["api_keys"]["apipinecone"])
pinecone.init(api_key=st.secrets["api_keys"]["apipinecone"])
index = pc.Index('tuguia')


def obtener_mejores_actividades(destino, embeddings):
    # Convertir los embeddings a un formato adecuado para Pinecone
    query_vectors = [embedding.tolist() for embedding in embeddings]
    
    # Realizar la búsqueda en Pinecone
    response = index.query(queries=query_vectors, top_k=5, include_values=True)
    
    # Procesar la respuesta para obtener las mejores actividades
    mejores_actividades = []
    for match in response['matches']:
        actividad = match['metadata']['actividad']
        descripcion = match['metadata']['descripcion']
        mejores_actividades.append((actividad, descripcion))
    
    return mejores_actividades

def generar_recomendaciones(destino, user_id):
    from openai import OpenAI
    # Obtener las preferencias del usuario desde la base de datos
    preferencias = obtener_preferencias_usuario(user_id)
    
    if preferencias:
        # Crear el mensaje de entrada para la API
        actividades = [pref[0] for pref in preferencias]
        prompt = f"Quiero recomendaciones de viaje para {destino}. Me interesan las siguientes actividades: {', '.join(actividades)}."

        try:
            # Llamar a la API de OpenAI utilizando la nueva interfaz de completions.create
            client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un asistente experto en recomendaciones de viajes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1,
                max_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            # Obtener la respuesta del modelo
            recomendaciones = response.choices[0].message['content'].strip()
            # Procesar las recomendaciones en una lista de tuplas
            recomendaciones_list = [tuple(rec.split(': ')) for rec in recomendaciones.split('\n') if ': ' in rec]
            return recomendaciones_list

        except Exception as e:
            return f"Error al generar recomendaciones: {str(e)}"
    else:
        return "No se encontraron preferencias para el usuario."

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))