import pymysql
from openai import OpenAI
import numpy as np
import pinecone
import streamlit as st
import config as c
import requests
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

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

def obtener_clima(ciudad, fecha):
    """Obtiene el pronóstico del clima para una ciudad y fecha específica"""
    try:
        api_key = st.secrets["api_keys"]["weather_key"]
        # Primero obtener coordenadas de la ciudad
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={ciudad}&limit=1&appid={api_key}"
        geo_response = requests.get(geo_url)
        if geo_response.status_code != 200:
            return None
            
        geo_data = geo_response.json()
        if not geo_data:
            return None
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']
        
        # Obtener pronóstico
        weather_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_response = requests.get(weather_url)
        if weather_response.status_code != 200:
            return None
            
        return weather_response.json()
    except Exception as e:
        st.error(f"Error al obtener el clima: {e}")
        return None

def procesar_clima(info_clima, fecha_inicio, fecha_fin):
    """Procesa la información del clima y genera HTML para mostrar"""
    if not info_clima or 'list' not in info_clima:
        return None
        
    # Diccionario para traducir descripciones del clima
    traducciones = {
        'clear sky': 'Cielo despejado',
        'few clouds': 'Pocas nubes',
        'scattered clouds': 'Nubes dispersas',
        'broken clouds': 'Nublado parcial',
        'shower rain': 'Lluvia ligera',
        'rain': 'Lluvia',
        'thunderstorm': 'Tormenta',
        'snow': 'Nieve',
        'mist': 'Neblina',
        'overcast clouds': 'Nublado',
        'light rain': 'Lluvia ligera',
        'moderate rain': 'Lluvia moderada',
        'heavy rain': 'Lluvia fuerte',
        'light snow': 'Nieve ligera',
        'heavy snow': 'Nieve intensa',
        'drizzle': 'Llovizna',
        'fog': 'Niebla'
    }
        
    # Construir el HTML de forma más simple
    html = '<div style="background: #2E2E2E; padding: 20px; border-radius: 15px; margin-bottom: 20px;">'
    html += '<h4 style="color: white; text-align: center; margin-bottom: 15px;">🌤️ Pronóstico del tiempo para tu viaje</h4>'
    html += '<div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">'
    
    fecha_actual = fecha_inicio
    dias_procesados = 0
    
    while fecha_actual <= fecha_fin and dias_procesados < 5:
        encontrado = False
        for prediccion in info_clima['list']:
            pred_fecha = datetime.fromtimestamp(prediccion['dt']).strftime('%Y-%m-%d')
            if pred_fecha == fecha_actual.strftime('%Y-%m-%d'):
                desc_original = prediccion['weather'][0]['description']
                temp = round(prediccion['main']['temp'])
                desc = traducciones.get(desc_original, desc_original)
                icono = prediccion['weather'][0]['icon']
                
                html += f'''
                <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center;">
                    <div style="color: white; font-weight: bold;">{fecha_actual.strftime('%d/%m/%Y')}</div>
                    <img src="http://openweathermap.org/img/w/{icono}.png" style="width: 50px; height: 50px;">
                    <div style="color: white;">{temp}°C</div>
                    <div style="color: #ccc; font-size: 0.8em;">{desc}</div>
                </div>'''
                encontrado = True
                break
        
        if not encontrado:
            # Si no hay datos para este día, buscar la predicción más cercana
            ultima_prediccion = info_clima['list'][-1]
            desc_original = ultima_prediccion['weather'][0]['description']
            temp = round(ultima_prediccion['main']['temp'])
            desc = traducciones.get(desc_original, desc_original)
            icono = ultima_prediccion['weather'][0]['icon']
            
            html += f'''
            <div style="background: rgba(255,255,255,0.1); padding: 10px; border-radius: 10px; text-align: center;">
                <div style="color: white; font-weight: bold;">{fecha_actual.strftime('%d/%m/%Y')}</div>
                <img src="http://openweathermap.org/img/w/{icono}.png" style="width: 50px; height: 50px;">
                <div style="color: white;">{temp}°C</div>
                <div style="color: #ccc; font-size: 0.8em;">{desc}</div>
            </div>'''
            
        fecha_actual += timedelta(days=1)
        dias_procesados += 1
    
    html += '</div></div>'
    return html

def generar_itinerario(destino, user_id, fecha_inicio=None, fecha_fin=None, incluir_clima=False):
    """Genera un itinerario detallado para un destino específico"""
    try:
        # Obtener preferencias del usuario
        preferencias = obtener_preferencias_usuario(user_id)
        if not preferencias:
            return "No se encontraron preferencias para el usuario"

        # Calcular número de días
        if fecha_inicio and fecha_fin:
            dias = (fecha_fin - fecha_inicio).days + 1
        else:
            dias = 5  # valor por defecto

        # Obtener y procesar información del clima
        info_clima = None
        clima_html = None
        if incluir_clima:
            info_clima = obtener_clima(destino, fecha_inicio)
            clima_html = procesar_clima(info_clima, fecha_inicio, fecha_fin)
            
            # Agregar información del clima al prompt si está disponible
            if info_clima and 'list' in info_clima:
                clima_info = []
                fecha_actual = fecha_inicio
                while fecha_actual <= fecha_fin:
                    fecha_str = fecha_actual.strftime('%Y-%m-%d')
                    for prediccion in info_clima['list']:
                        pred_fecha = datetime.fromtimestamp(prediccion['dt']).strftime('%Y-%m-%d')
                        if pred_fecha == fecha_str:
                            temp = prediccion['main']['temp']
                            desc = prediccion['weather'][0]['description']
                            clima_info.append(f"Día {fecha_actual.strftime('%d/%m')}: {desc}, {temp}°C")
                            break
                    fecha_actual += timedelta(days=1)
                
                clima_texto = "\n".join(clima_info)
                prompt_clima = f"\nCondiciones climáticas durante tu viaje:\n{clima_texto}\n"
            else:
                prompt_clima = ""
        else:
            prompt_clima = ""

        # Crear prompt con fechas específicas
        prompt = f"""Como experto guía turístico, genera un itinerario detallado para {destino} con EXACTAMENTE {dias} días.
        El viaje será del {fecha_inicio.strftime('%d/%m/%Y')} al {fecha_fin.strftime('%d/%m/%Y')}.
        El viajero tiene las siguientes preferencias: {preferencias}
        {prompt_clima}
        IMPORTANTE: Genera EXACTAMENTE {dias} actividades, una para cada día del viaje.
        
        Para cada día, proporciona la siguiente información en este formato exacto:
        ACTIVIDAD: [nombre de la actividad principal del día]
        DESCRIPCION: [descripción detallada incluyendo lugares específicos, consejos y recomendaciones]
        TIPO: [tipo de actividad: cultural/aventura/gastronomía/etc]
        DURACION: [duración estimada de la actividad]
        MEJOR_EPOCA: [mejor momento del día para esta actividad]
        LINK: [URL de la atracción principal o lugar recomendado]
        ---
        """

        # Crear cliente OpenAI
        client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])

        # Obtener respuesta del GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        # Procesar la respuesta
        texto_completo = response.choices[0].message.content
        texto_completo = texto_completo.lstrip('---').strip()
        actividades_raw = [act.strip() for act in texto_completo.split('---') if act.strip()]
        
        actividades_procesadas = []
        for actividad_texto in actividades_raw:
            lineas = [l.strip() for l in actividad_texto.split('\n') if l.strip()]
            actividad = {}
            
            for linea in lineas:
                if linea.startswith('ACTIVIDAD:'):
                    actividad['nombre'] = linea.replace('ACTIVIDAD:', '').strip()
                elif linea.startswith('DESCRIPCION:'):
                    actividad['descripcion'] = linea.replace('DESCRIPCION:', '').strip()
                elif linea.startswith('TIPO:'):
                    actividad['tipo'] = linea.replace('TIPO:', '').strip()
                elif linea.startswith('DURACION:'):
                    actividad['duracion'] = linea.replace('DURACION:', '').strip()
                elif linea.startswith('MEJOR_EPOCA:'):
                    actividad['mejor_epoca'] = linea.replace('MEJOR_EPOCA:', '').strip()
                elif linea.startswith('LINK:'):
                    actividad['link'] = linea.replace('LINK:', '').strip()
            
            if actividad:
                # Generar URL de imagen para la actividad
                actividad['imagen_url'] = obtener_imagen_lugar(f"{actividad['nombre']} {destino}")
                # Calcular score basado en preferencias y tipo de actividad
                actividad['score'] = calcular_score_actividad(actividad['tipo'], preferencias)
                actividades_procesadas.append(actividad)

        # Asegurarnos de que tenemos el número correcto de actividades
        if len(actividades_procesadas) < dias:
            st.warning(f"El itinerario generado tiene menos actividades ({len(actividades_procesadas)}) que los días solicitados ({dias})")
            # Repetir la generación si es necesario
            return generar_itinerario(destino, user_id, fecha_inicio, fecha_fin, incluir_clima)

        return {
            'destino': destino,
            'actividades': actividades_procesadas[:dias],
            'clima_html': clima_html if incluir_clima else None
        }

    except Exception as e:
        st.error(f"Error al generar itinerario: {str(e)}")
        return f"Error al generar itinerario: {str(e)}"

def calcular_score_actividad(tipo_actividad, preferencias):
    """Calcula un score basado en las preferencias del usuario y el tipo de actividad"""
    try:
        # Convertir preferencias a diccionario para fácil acceso
        pref_dict = {pref[0].lower(): pref[1] for pref in preferencias}
        
        # Mapear tipos de actividad a categorías de preferencias
        tipo_mapping = {
            'cultural': ['cultural', 'urbano'],
            'aventura': ['aventura', 'deportivo'],
            'gastronomía': ['gastronomía'],
            'naturaleza': ['naturaleza', 'aventura'],
            'relax': ['relax'],
            'urbano': ['urbano', 'cultural'],
            'nocturno': ['nocturno']
        }
        
        # Obtener categorías relacionadas
        categorias = tipo_mapping.get(tipo_actividad.lower(), [tipo_actividad.lower()])
        
        # Calcular score promedio
        scores = [pref_dict.get(cat, 3) for cat in categorias]
        score_final = sum(scores) / len(scores) / 5.0  # Normalizar a 0-1
        
        return min(max(score_final, 0.1), 1.0)  # Asegurar que esté entre 0.1 y 1.0
        
    except Exception as e:
        return 0.5  # Valor por defecto si hay error

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

def obtener_usuario_actual():
    """Obtiene el ID del usuario actual desde la sesión de Streamlit"""
    if "id_usuario" in st.session_state and st.session_state.id_usuario is not None:
        return st.session_state.id_usuario
    return None

def obtener_imagen_lugar(lugar):
    """Obtiene la imagen de un lugar usando Google Places API"""
    try:
        api_key = st.secrets["api_keys"]["google_places_key"]
        
        # Limpiar el nombre del lugar
        lugar_limpio = lugar.strip()
        
        # Primero buscar el lugar
        search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        search_params = {
            "input": lugar_limpio,
            "inputtype": "textquery",
            "fields": "photos,place_id",
            "key": api_key
        }
        
        response = requests.get(search_url, params=search_params)
        if response.status_code != 200:
            return f"https://source.unsplash.com/800x400/?{lugar_limpio.replace(' ', '+')},city"
            
        result = response.json()
        
        if result.get("candidates") and result["candidates"][0].get("photos"):
            photo_reference = result["candidates"][0]["photos"][0]["photo_reference"]
            
            # Obtener la imagen
            photo_url = "https://maps.googleapis.com/maps/api/place/photo"
            photo_params = {
                "maxwidth": 800,
                "photo_reference": photo_reference,
                "key": api_key
            }
            
            return photo_url + "?" + "&".join(f"{k}={v}" for k, v in photo_params.items())
            
    except Exception as e:
        st.error(f"Error al obtener imagen: {e}")
    
    # Si algo falla, usar Unsplash como respaldo
    return f"https://source.unsplash.com/800x400/?{lugar_limpio.replace(' ', '+')},city"

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

def generar_recomendaciones_destinos(user_id):
    """Genera recomendaciones de destinos basadas en las preferencias del usuario"""
    try:
        # Obtener preferencias del usuario
        preferencias = obtener_preferencias_usuario(user_id)
        if not preferencias:
            return "No se encontraron preferencias para el usuario"

        # Crear cliente OpenAI
        client = OpenAI(api_key=st.secrets["api_keys"]["apigpt_key"])

        # Prompt para el GPT
        prompt = f"""Como experto en viajes, recomienda 5 destinos basados en estas preferencias:
        {preferencias}
        
        Proporciona la información en este formato exacto, empezando cada destino con '---':
        ---
        Destino: [Ciudad], [País]
        ¿Por qué?: [Explicación breve de por qué este destino]
        Mejor época: [Mejor temporada para visitar]
        Duración sugerida: [Tiempo recomendado de estadía]
        Actividad destacada: [Nombre de la actividad] | [URL de la actividad]
        """

        # Obtener respuesta del GPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            'recomendaciones_gpt': response.choices[0].message.content.strip()
        }

    except Exception as e:
        st.error(f"Error al generar recomendaciones: {str(e)}")
        return f"Error al generar recomendaciones: {str(e)}"

def generar_pdf_itinerario(destino, actividades, clima_html=None):
    """Genera un PDF con el itinerario"""
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        styles = getSampleStyleSheet()
        
        # Estilo personalizado para títulos
        titulo_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#FF4B4B'),
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        # Título del itinerario
        story.append(Paragraph(f"Tu Itinerario en {destino}", titulo_style))
        story.append(Spacer(1, 20))
        
        # Agregar cada actividad
        for i, act in enumerate(actividades, 1):
            # Título de la actividad
            story.append(Paragraph(
                f"Día {i}: {act.get('nombre', 'Actividad sin nombre')}",
                styles['Heading2']
            ))
            story.append(Spacer(1, 10))
            
            # Descripción
            descripcion = act.get('DESCRIPCION', act.get('descripcion', 'No hay descripción disponible'))
            story.append(Paragraph(descripcion, styles['Normal']))
            story.append(Spacer(1, 10))
            
            # Detalles
            detalles = [
                f"🕒 Duración: {act.get('DURACION', act.get('duracion', 'No especificada'))}",
                f"📅 Mejor momento: {act.get('MEJOR_EPOCA', act.get('mejor_epoca', 'No especificado'))}",
                f"🔗 Más información: {act.get('LINK', act.get('link', 'No disponible'))}"
            ]
            
            for detalle in detalles:
                story.append(Paragraph(detalle, styles['Normal']))
            
            story.append(Spacer(1, 20))
        
        # Generar el PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()

        except Exception as e:
        st.error(f"Error al generar el PDF: {str(e)}")
        return None