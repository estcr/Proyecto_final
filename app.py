import os
import funciones as f
import config as c
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO

# Configuración de la página y eliminación del mensaje de Streamlit
st.set_page_config(
    page_title="TuGuía - Tu Planificador de Viajes",
    page_icon="https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Estilos CSS personalizados actualizados
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: auto;
        border-radius: 5px;
        height: 2.5em;
        background-color: #FF4B4B;
        color: white !important;
        border: none;
        padding: 0 20px;
        font-weight: bold;
    }
    .stButton>button:active {
        color: white !important;
        background-color: #E04141;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    h1 {
        color: #FF4B4B;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h2 {
        color: #2e7bcf;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .stSuccess {
        background-color: #28a745;
    }
    .destino-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        border-left: 5px solid #FF4B4B;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
        color: #000;
    }
    
    .numero-destino {
        position: absolute;
        top: -10px;
        right: -10px;
        background-color: #FF4B4B;
        color: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    
    .destino-titulo {
        color: #FF4B4B;
        font-size: 28px !important;
        margin-bottom: 15px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .pais-texto {
        font-size: 18px;
        color: #666;
        text-transform: none;
    }
    
    .info-tag {
        background-color: #2e7bcf;
        color: white !important;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 14px;
        margin-right: 10px;
        display: inline-block;
        margin-bottom: 10px;
    }
    
    .porque-texto {
        margin: 15px 0;
        padding: 15px;
        background-color: #FF4B4B;
        border-radius: 5px;
        color: white !important;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .destino-card p {
        color: #000 !important;
        margin-bottom: 10px;
        font-size: 16px;
    }
    
    .actividad-link {
        color: #FF4B4B;
        text-decoration: none;
        padding: 8px 15px;
        border: 2px solid #FF4B4B;
        border-radius: 20px;
        display: inline-block;
        margin-top: 10px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .actividad-link:hover {
        background-color: #FF4B4B;
        color: white;
        transform: translateY(-2px);
    }
    
    .imagen-destino {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .imagen-destino:hover {
        transform: scale(1.05);
    }
    
    .separador-titulo {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        color: #2e7bcf;
        margin: 30px 0;
        padding: 10px;
        border-bottom: 3px solid #FF4B4B;
    }
    
    .separador {
        height: 2px;
        background: linear-gradient(to right, transparent, #e0e0e0, transparent);
        margin: 40px 0;
    }
    
    .destino-card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        border-left: 5px solid #FF4B4B;
    }
    
    .ranking-badge {
        position: absolute;
        top: -15px;
        right: -15px;
        background-color: #FF4B4B;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .destino-header {
        margin-bottom: 20px;
        border-bottom: 2px solid #f0f0f0;
        padding-bottom: 10px;
    }
    
    .destino-titulo {
        color: #FF4B4B;
        font-size: 28px;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    .destino-subtitulo {
        color: #666;
        font-size: 18px;
        margin-top: 5px;
    }
    
    .destino-content {
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    
    .destino-card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        position: relative;
        border-left: 5px solid #FF4B4B;
    }
    
    .titulo-seccion {
        font-size: 2em;
        font-weight: bold;
        text-align: center;
        color: #2e7bcf;
        margin: 2em 0;
        padding: 1em;
        border-bottom: 3px solid #FF4B4B;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .destino-container {
        position: relative;
        margin: 3em 0;
        padding: 1em;
    }
    
    .ranking {
        position: absolute;
        top: -20px;
        left: 50%;
        transform: translateX(-50%);
        background: #FF4B4B;
        color: white;
        padding: 0.5em 1em;
        border-radius: 20px;
        font-weight: bold;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 2;
    }
    
    .destino-card {
        background: white;
        border-radius: 20px;
        padding: 2em;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-top: 1em;
    }
    
    .destino-header {
        text-align: center;
        margin-bottom: 1.5em;
    }
    
    .ciudad {
        font-size: 2em;
        font-weight: bold;
        color: #FF4B4B;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .pais {
        font-size: 1.2em;
        color: #666;
        margin-top: 0.3em;
    }
    
    .descripcion {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        line-height: 1.8;
        color: #333;
        font-size: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .info-tag {
        display: inline-block;
        padding: 10px 20px;
        margin: 8px;
        border-radius: 25px;
        font-size: 15px;
        font-weight: 500;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .epoca {
        background: #e3f2fd;
        color: #1976d2;
        border: 1px solid #bbdefb;
    }
    
    .duracion {
        background: #f3e5f5;
        color: #7b1fa2;
        border: 1px solid #e1bee7;
    }
    
    .actividad-btn {
        display: inline-block;
        background: #FF4B4B;
        color: white !important;
        padding: 12px 25px;
        border-radius: 25px;
        text-decoration: none;
        margin-top: 15px;
        transition: all 0.3s ease;
        font-weight: 500;
        font-size: 15px;
        box-shadow: 0 2px 4px rgba(255,75,75,0.2);
    }
    
    .actividad-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .imagen-placeholder {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        overflow: hidden;
    }
    
    .placeholder-text {
        font-size: 24px;
        color: #666;
        text-align: center;
        padding: 20px;
    }
    
    .destinos-wrapper {
        display: flex;
        flex-direction: column;
        gap: 2em;
        padding: 1em;
    }
    
    .separador {
        height: 2px;
        background: linear-gradient(to right, transparent, #e0e0e0, transparent);
        margin: 2em 0;
    }
    
    .destino-content {
        display: flex;
        flex-direction: column;
        gap: 1em;
        padding: 1em;
    }
    
    .titulo-seccion {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: #2e7bcf;
        margin: 40px 0;
        padding: 15px;
    }
    
    .destino-container {
        background: #1a1a1a;
        border-radius: 20px;
        padding: 30px;
        margin: 40px 0;
        position: relative;
    }
    
    .ranking {
        position: absolute;
        top: -15px;
        left: 50%;
        transform: translateX(-50%);
        background: #FF4B4B;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 16px;
        z-index: 2;
    }
    
    .destino-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin-top: 20px;
    }
    
    .destino-header {
        text-align: center;
        margin-bottom: 25px;
    }
    
    .ciudad {
        font-size: 32px;
        font-weight: bold;
        color: #FF4B4B;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    
    .pais {
        font-size: 18px;
        color: #666;
    }
    
    .descripcion {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        line-height: 1.6;
        color: #333;
    }
    
    .info-tag {
        display: inline-block;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        font-size: 14px;
    }
    
    .epoca {
        background: #e3f2fd;
        color: #1976d2;
    }
    
    .duracion {
        background: #f3e5f5;
        color: #7b1fa2;
    }
    
    .actividad-btn {
        display: inline-block;
        background: #FF4B4B;
        color: white !important;
        padding: 10px 20px;
        border-radius: 25px;
        text-decoration: none;
        margin-top: 15px;
        transition: all 0.3s ease;
    }
    
    .actividad-btn:hover {
        background: #ff6b6b;
        transform: translateY(-2px);
    }
    
    .imagen-placeholder {
        background: #f8f9fa;
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3em;
        border-radius: 10px;
    }
    
    .destino-content {
        margin-top: 20px;
    }
    
    .separador {
        height: 1px;
        background: rgba(255,255,255,0.1);
        margin: 40px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Función para mostrar el logo
def mostrar_logo():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        try:
            st.image("img/t-vectorizada.png", width=300)
        except:
            # Fallback a la URL de GitHub si la imagen local no se encuentra
            st.image("https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png", width=300)

# Función para la página de inicio actualizada
def pagina_inicio():
    mostrar_logo()
    st.title("¡Bienvenido a TuGuía! 🌎")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Tu Destino, Tu Aventura
        Descubre lugares increíbles basados en tus preferencias personales.
        Planifica tu próximo viaje con recomendaciones personalizadas y
        consejos de expertos.
        """)
        
        st.markdown("""
        ### ✨ Características
        - 🎯 Recomendaciones personalizadas
        - 🗺️ Planificación de itinerarios
        - 🌟 Destinos únicos
        - 📅 Organización de viajes
        """)
    
    with col2:
        st.markdown("""
        ### 🚀 Comienza Tu Viaje
        1. Regístrate o inicia sesión
        2. Completa tus preferencias
        3. Obtén recomendaciones personalizadas
        4. ¡Planifica tu aventura!
        """)

# Función de login modernizada
def login():
    mostrar_logo()
    st.title("Inicio de Sesión 🔐")
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="tucorreo@ejemplo.com")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            submitted = st.form_submit_button("Iniciar Sesión", use_container_width=True)
    
    if submitted:
        user_id = f.obtener_usuario_por_email(email)
        if user_id:
            st.session_state.id_usuario = user_id
            st.success("¡Bienvenido de nuevo! 👋")
            st.balloons()
            
            # Botón para continuar
            if st.button("¡Comenzar mi aventura! 🚀"):
                st.session_state.pagina_actual = "🏠 Inicio"
                st.rerun()
        else:
            st.error("Usuario no encontrado 😕")

# Función de registro modernizada
def obtener_datos_usuario():
    mostrar_logo()
    st.title("Únete a la Aventura ✈️")
    
    with st.form("registro_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nombre", placeholder="Tu nombre")
        with col2:
            email = st.text_input("Email", placeholder="tucorreo@ejemplo.com")
            
        travel_style = st.selectbox("¿Cómo te gusta viajar?", 
            ["Solo 🚶", "Con amigos 👥", "En pareja 💑", "Por trabajo 💼"])
        
        submitted = st.form_submit_button("¡Comenzar mi aventura!")
    
    if submitted:
        if name and email:
            registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.insertar_usuario(name, email, travel_style, registration_date)
            st.success("¡Bienvenido a bordo! 🎉")
            st.balloons()
        else:
            st.error("Por favor, completa todos los campos 🙏")

# Función de preferencias modernizada
def interfaz_preferencias():
    st.title("Cuéntanos Sobre Tus Gustos 🌟")
    
    if "id_usuario" in st.session_state:
        st.info(f"Personalizando tu experiencia...")
    
    st.write("Califica tus intereses del 1 al 5 (1: Poco interés, 5: Me encanta)")
    
    with st.form("preferencias_form"):
        col1, col2 = st.columns(2)
        
        actividades = {}
        
        with col1:
            actividades["Aventura"] = st.slider("🏃‍♂️ Aventura", 1, 5, 3)
            actividades["Cultural"] = st.slider("🏛️ Cultural", 1, 5, 3)
            actividades["Gastronomía"] = st.slider("🍽️ Gastronomía", 1, 5, 3)
            actividades["Relax"] = st.slider("🌅 Relax", 1, 5, 3)
        
        with col2:
            actividades["Naturaleza"] = st.slider("🌲 Naturaleza", 1, 5, 3)
            actividades["Urbano"] = st.slider("🌆 Urbano", 1, 5, 3)
            actividades["Nocturno"] = st.slider("🌙 Nocturno", 1, 5, 3)
            actividades["Deportivo"] = st.slider("⚽ Deportivo", 1, 5, 3)
        
        submitted = st.form_submit_button("Guardar mis preferencias")
    
    if submitted:
        if "id_usuario" in st.session_state:
            f.insertar_preferencias_viaje(st.session_state.id_usuario, actividades)
            st.success("¡Preferencias actualizadas! 🎯")
        else:
            st.warning("Inicia sesión para guardar tus preferencias 🔒")

# Función para mostrar recomendaciones personalizadas
def interfaz_recomendaciones():
    st.title("Recomendaciones de Destinos")
    
    if "id_usuario" not in st.session_state or st.session_state.id_usuario is None:
        st.warning("Por favor, inicia sesión primero")
        return
    
    # Obtener el ID del usuario de la sesión
    user_id = st.session_state.id_usuario
    
    st.markdown("""
    ### ¿No sabes dónde viajar? 🤔
    Basándonos en tus preferencias y estilo de viaje, hemos seleccionado estos destinos 
    increíbles que creemos que te encantarán. ¡Descubre tu próxima aventura! ✨
    """)
    
    if st.button("Descubrir Destinos Perfectos ✨"):
        with st.spinner("Creando tu lista de destinos soñados... 🌍"):
            resultado = f.generar_recomendaciones_destinos(user_id)
            
            if isinstance(resultado, dict):
                recomendaciones = [rec.strip() for rec in resultado['recomendaciones_gpt'].split('---') if rec.strip()]
                
                # Título principal
                st.markdown("""
                <div class="titulo-seccion">
                    TOP 5 DESTINOS PARA TI
                </div>
                """, unsafe_allow_html=True)
                
                # Contenedor para todos los destinos
                st.markdown("""<div class="destinos-wrapper">""", unsafe_allow_html=True)
                
                for i, rec in enumerate(recomendaciones, 1):
                    try:
                        lines = [line.strip() for line in rec.split('\n') if line.strip()]
                        destino_line = next((line for line in lines if line.startswith('Destino:')), None)
                        if not destino_line:
                            continue
                            
                        destino = destino_line.replace('Destino:', '').strip()
                        ciudad, pais = [part.strip() for part in destino.split(',')] if ',' in destino else (destino, '')
                        
                        # Contenedor individual para cada destino
                        st.markdown(f"""
                        <div class="destino-container">
                            <div class="ranking">#{i}</div>
                            <div class="destino-card">
                                <div class="destino-header">
                                    <div class="ciudad">{ciudad}</div>
                                    <div class="pais">{pais}</div>
                                </div>
                                <div class="destino-content">
                        """, unsafe_allow_html=True)
                        
                        # Columnas para imagen e información
                        col1, col2 = st.columns([1, 1.5])
                        
                        with col1:
                            try:
                                imagen_url = f.obtener_imagen_lugar(f"{ciudad}, {pais}")
                                if imagen_url:
                                    response = requests.get(imagen_url, timeout=10)  # Agregamos timeout
                                    if response.status_code == 200:
                                        try:
                                            img = Image.open(BytesIO(response.content))
                                            st.image(img, use_container_width=True)
                                        except:
                                            # Si falla al abrir la imagen, intentamos con Unsplash
                                            unsplash_url = f"https://source.unsplash.com/800x600/?{ciudad.replace(' ', '+')},{pais.replace(' ', '+')},landmark"
                                            st.image(unsplash_url, use_container_width=True)
                                    else:
                                        # Si falla la primera URL, intentamos con Unsplash
                                        unsplash_url = f"https://source.unsplash.com/800x600/?{ciudad.replace(' ', '+')},{pais.replace(' ', '+')},landmark"
                                        st.image(unsplash_url, use_container_width=True)
                            except:
                                # Si todo falla, mostramos un placeholder con estilo
                                st.markdown(f"""
                                <div class="imagen-placeholder">
                                    <div class="placeholder-text">🌄 {ciudad}</div>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        with col2:
                            for line in lines:
                                if line.startswith('Destino:'):
                                    continue
                                elif '¿Por qué?' in line:
                                    texto = line.replace('¿Por qué?:', '').strip()
                                    st.markdown(f"""<div class="descripcion">💫 {texto}</div>""", 
                                              unsafe_allow_html=True)
                                elif 'Mejor época:' in line:
                                    epoca = line.replace('Mejor época:', '').strip()
                                    st.markdown(f"""<div class="info-tag epoca">🗓️ {epoca}</div>""", 
                                              unsafe_allow_html=True)
                                elif 'Duración sugerida:' in line:
                                    duracion = line.replace('Duración sugerida:', '').strip()
                                    st.markdown(f"""<div class="info-tag duracion">⏱️ {duracion}</div>""", 
                                              unsafe_allow_html=True)
                                elif 'Actividad destacada:' in line:
                                    nombre = line.split('|')[0].replace('Actividad destacada:', '').strip()
                                    link = line.split('|')[1].strip() if '|' in line else '#'
                                    st.markdown(f"""
                                    <a href="{link}" target="_blank" class="actividad-btn">
                                        🎯 {nombre}
                                    </a>""", unsafe_allow_html=True)
                        
                        # Cerrar los divs de cada destino
                        st.markdown("""
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Agregar separador entre destinos
                        if i < len(recomendaciones):
                            st.markdown("""<div class="separador"></div>""", unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error al procesar destino {i}: {str(e)}")
                
                # Cerrar el contenedor principal
                st.markdown("""</div>""", unsafe_allow_html=True)
            else:
                st.error(resultado)

# Función para generar itinerario
def mostrar_itinerario():
    st.title("Generar Itinerario de Viaje")
    
    # Verificar si hay un usuario en la sesión
    if "id_usuario" not in st.session_state or st.session_state.id_usuario is None:
        st.warning("Por favor, inicia sesión primero")
        return
    
    user_id = st.session_state.id_usuario
    
    # Input para el destino
    destino = st.text_input("¿A dónde quieres viajar?")
    
    if st.button("Generar Recomendaciones"):
        if not destino:
            st.warning("Por favor, ingresa un destino")
            return
            
        with st.spinner("Generando recomendaciones personalizadas..."):
            resultado = f.generar_recomendaciones_completas(destino, user_id)
            
            if isinstance(resultado, dict):
                # Mostrar recomendaciones de ChatGPT
                st.subheader("Recomendaciones Personalizadas")
                st.write(resultado['recomendaciones_gpt'])
                
                # Mostrar actividades similares
                st.subheader("Actividades Similares de Nuestra Base de Datos")
                for i, act in enumerate(resultado['actividades_similares'], 1):
                    with st.expander(f"{i}. {act['Actividad']}"):
                        st.write(f"**Descripción:** {act['Descripción']}")
                        st.write(f"**Relevancia:** {act['score']:.2f}")
            else:
                st.error(resultado)

# Función para obtener datos del usuario y guardarlos en la base de datos
def obtener_datos_usuario():
    st.title("Registro de Usuario")
    
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    travel_style = st.selectbox("Estilo de viaje", ["solo", "amigos", "pareja", "trabajo"])
    
    if st.button("Registrar"):
        f.insertar_usuario(name, email, travel_style, registration_date)
        st.success("Usuario registrado exitosamente")

# Función para manejar el inicio de sesión
def login():
    st.title("Inicio de Sesión")
    email = st.text_input("Email")
    if st.button("Iniciar Sesión"):
        user_id = obtener_usuario_por_email(email)
        if user_id:
            st.session_state.id_usuario = user_id
            st.success("Inicio de sesión exitoso")
        else:
            st.error("Usuario no encontrado")

# Función para manejar el cierre de sesión
def logout():
    st.session_state.id_usuario = None
    st.success("Sesión cerrada exitosamente")

# Función para obtener el ID del usuario por email
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
        st.error(f"Error al obtener el usuario: {e}")
        return None

# Función para mostrar una imagen de forma segura
def mostrar_imagen_segura(url):
    """Muestra una imagen de forma segura, con manejo de errores"""
    try:
        import requests
        from PIL import Image
        from io import BytesIO
        
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        st.image(img, width=200)
    except Exception as e:
        st.warning("No se pudo cargar la imagen 🖼️")

# Llamamos a la interfaz principal con la barra lateral
def main():
    # Aseguramos que las variables de sesión estén inicializadas
    if "id_usuario" not in st.session_state:
        st.session_state.id_usuario = None

    # Barra lateral modernizada
    with st.sidebar:
        st.markdown("### 🌍 TuGuía")
        if st.session_state.id_usuario:
            st.success("Sesión iniciada ✅")
            if st.button("Cerrar Sesión 👋"):
                st.session_state.id_usuario = None
                st.rerun()
            
            pagina_actual = st.radio(
                "Navegación",
                ["🏠 Inicio", "⭐ Preferencias", "🎯 Recomendaciones", "📍 Itinerario"]
            )
        else:
            pagina_actual = st.radio(
                "Navegación",
                ["🔑 Inicio de Sesión", "📝 Registro"]
            )

    # Manejo de páginas
    if pagina_actual == "🔑 Inicio de Sesión":
        login()
    elif pagina_actual == "📝 Registro":
        obtener_datos_usuario()
    elif pagina_actual == "🏠 Inicio":
        pagina_inicio()
    elif pagina_actual == "⭐ Preferencias":
        interfaz_preferencias()
    elif pagina_actual == "🎯 Recomendaciones":
        interfaz_recomendaciones()
    elif pagina_actual == "📍 Itinerario":
        mostrar_itinerario()

# Ejecutamos la aplicación
if __name__ == "__main__":
    main()
