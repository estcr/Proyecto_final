import pymysql
from openai import OpenAI
import numpy as np
import pinecone
import streamlit as st
import config as c

def obtener_preferencias_usuario(user_id):
    """Obtiene las preferencias del usuario desde la base de datos"""
    conn = c.conectar_bd()
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

def generar_recomendaciones_gpt(destino, preferencias, travel_style):
    """Genera recomendaciones usando ChatGPT"""
    client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])
    
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
    client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])
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
    pc = pinecone.Pinecone(api_key=st.secrets["api_keys"]["apipinecone"])
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
        travel_style = obtener_travel_style(user_id)
        
        if not preferencias:
            return "No se encontraron preferencias para el usuario."

        # 2. Generar recomendaciones con ChatGPT
        recomendaciones_gpt = generar_recomendaciones_gpt(destino, preferencias, travel_style)
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

def generar_recomendaciones_destinos(user_id):
    """Genera recomendaciones de destinos basados en las preferencias del usuario"""
    try:
        # Obtener preferencias y estilo de viaje del usuario
        preferencias = obtener_preferencias_usuario(user_id)
        travel_style = obtener_travel_style(user_id)  # Nueva función
        
        if not preferencias:
            return "No se encontraron preferencias para el usuario."

        client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])
        
        actividades = [f"{pref[0]} (nivel de interés: {pref[1]})" for pref in preferencias]
        prompt = f"""Actúa como un experto agente de viajes y recomienda los 5 mejores destinos del mundo 
        para un viajero que viaja {travel_style} y tiene las siguientes preferencias: {', '.join(actividades)}.
        
        Para cada destino, proporciona:
        1. Nombre del destino
        2. País
        3. Por qué es ideal según las preferencias del viajero y su estilo de viaje ({travel_style})
        4. Mejor época para visitar
        5. Duración recomendada de la visita
        6. Una actividad destacada con su link de reserva o sitio web oficial
        7. Una imagen representativa (URL de una imagen libre de derechos)
        
        Formato para cada recomendación:
        Destino: [ciudad, país]
        ¿Por qué?: [explicación basada en preferencias y estilo de viaje]
        Mejor época: [temporada]
        Duración sugerida: [días recomendados]
        Actividad destacada: [nombre] | [link]
        Imagen: [url_imagen]
        ---"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        recomendaciones_destinos = response.choices[0].message.content

        # 3. Generar embedding para las recomendaciones
        embedding = vectorizar_actividades(recomendaciones_destinos)
        if embedding is None:
            return "Error al generar el embedding."

        # 4. Obtener destinos similares de la tabla vectorial
        destinos_similares = obtener_actividades_similares(embedding)

        return {
            'recomendaciones_gpt': recomendaciones_destinos,
            'destinos_similares': destinos_similares
        }

    except Exception as e:
        st.error(f"Error al generar recomendaciones de destinos: {e}")
        return f"Error: {str(e)}"

def insertar_preferencias_viaje(user_id, preferencias):
    """Actualiza o inserta las preferencias del usuario"""
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        
        # Primero eliminamos las preferencias existentes del usuario
        delete_query = "DELETE FROM user_activity_preferences WHERE user_id = %s"
        cursor.execute(delete_query, (user_id,))
        
        # Luego insertamos las nuevas preferencias
        insert_query = """INSERT INTO user_activity_preferences 
                         (user_id, activity_name, preference_level) 
                         VALUES (%s, %s, %s)"""
        
        for actividad, nivel in preferencias.items():
            cursor.execute(insert_query, (user_id, actividad, nivel))
        
        conn.commit()
        st.success("Preferencias actualizadas exitosamente")
    except Exception as e:
        conn.rollback()
        st.error(f"Error al actualizar preferencias: {e}")
    finally:
        conn.close()

def insertar_usuario(name, email, travel_style, registration_date):
    """Inserta un nuevo usuario en la base de datos"""
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        
        # Verificar si el email ya existe
        check_query = "SELECT user_id FROM users WHERE email = %s"
        cursor.execute(check_query, (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            st.warning("Este email ya está registrado")
            return False
        
        # Insertar nuevo usuario
        query = """
        INSERT INTO users (name, email, travel_style, registration_date) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, email, travel_style, registration_date))
        conn.commit()
        
        # Obtener el ID del usuario recién insertado
        user_id = cursor.lastrowid
        st.session_state.id_usuario = user_id
        
        return True
        
    except Exception as e:
        conn.rollback()
        st.error(f"Error al registrar usuario: {e}")
        return False
    finally:
        conn.close()

def obtener_travel_style(user_id):
    """Obtiene el estilo de viaje del usuario desde la base de datos"""
    conn = c.conectar_bd()
    try:
        cursor = conn.cursor()
        query = "SELECT travel_style FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else "solo"
    except Exception as e:
        st.error(f"Error al obtener el estilo de viaje: {e}")
        return "solo"
    finally:
        conn.close()