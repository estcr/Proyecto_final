import pymysql
from openai import OpenAI
import numpy as np
import pinecone
import streamlit as st

def obtener_preferencias_usuario(user_id):
    """Obtiene las preferencias del usuario desde la base de datos"""
    conn = pymysql.connect(
        host=st.secrets["host"],
        user=st.secrets["user"],
        password=st.secrets["password"],
        database=st.secrets["database"]
    )
    try:
        cursor = conn.cursor()
        query = "SELECT activity_name, preference_level FROM user_activity_preferences WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        conn.close()
        return result if result else None
    except Exception as e:
        st.error(f"Error al obtener las preferencias del usuario: {e}")
        return None

def generar_recomendaciones_gpt(destino, preferencias):
    """Genera recomendaciones usando ChatGPT"""
    client = OpenAI(api_key=st.secrets["apigpt_key"])
    
    actividades = [f"{pref[0]} (nivel de interés: {pref[1]})" for pref in preferencias]
    prompt = f"""Actúa como un experto guía turístico y genera 5 recomendaciones específicas de actividades para hacer en {destino}.
    El viajero tiene las siguientes preferencias: {', '.join(actividades)}.
    Para cada actividad, proporciona:
    1. Nombre de la actividad
    2. Breve descripción
    3. Por qué se ajusta a las preferencias del viajero
    Formato: Actividad: [nombre] | Descripción: [descripción] | Relevancia: [explicación]"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error al generar recomendaciones con GPT: {e}")
        return None

def vectorizar_actividades(texto):
    """Genera embeddings para las actividades"""
    client = OpenAI(api_key=st.secrets["apigpt_key"])
    try:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=texto
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Error al generar embedding: {e}")
        return None

def obtener_actividades_similares(embedding):
    """Obtiene actividades similares desde Pinecone"""
    pc = pinecone.Pinecone(api_key=st.secrets["apipinecone"])
    index = pc.Index('tuguia')
    
    try:
        results = index.query(
            vector=embedding,
            top_k=5,
            include_metadata=True
        )
        
        actividades_similares = []
        for match in results['matches']:
            actividad = {
                'Actividad': match['metadata'].get('Actividad', 'No disponible'),
                'Descripción': match['metadata'].get('Descripción', 'No disponible'),
                'score': match['score']
            }
            actividades_similares.append(actividad)
        
        return actividades_similares
    except Exception as e:
        st.error(f"Error al consultar Pinecone: {e}")
        return []

def generar_recomendaciones_completas(destino, user_id):
    """Función principal para generar todas las recomendaciones"""
    try:
        # 1. Obtener preferencias del usuario
        preferencias = obtener_preferencias_usuario(user_id)
        if not preferencias:
            return "No se encontraron preferencias para el usuario."

        # 2. Generar recomendaciones con ChatGPT
        recomendaciones_gpt = generar_recomendaciones_gpt(destino, preferencias)
        if not recomendaciones_gpt:
            return "Error al generar recomendaciones con GPT."

        # 3. Generar embedding para las recomendaciones
        embedding = vectorizar_actividades(recomendaciones_gpt)
        if embedding is None:
            return "Error al generar el embedding."

        # 4. Obtener actividades similares de la tabla vectorial
        actividades_similares = obtener_actividades_similares(embedding)

        return {
            'recomendaciones_gpt': recomendaciones_gpt,
            'actividades_similares': actividades_similares
        }

    except Exception as e:
        st.error(f"Error en generar_recomendaciones_completas: {e}")
        return f"Error: {str(e)}"

def obtener_usuario_actual():
    """Obtiene el ID del usuario actual desde la sesión de Streamlit"""
    if "id_usuario" in st.session_state and st.session_state.id_usuario is not None:
        return st.session_state.id_usuario
    return None