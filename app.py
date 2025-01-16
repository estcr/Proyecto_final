import os
import funciones as f
import config as c
import streamlit as st
import pandas as pd
from datetime import datetime
import requests
from PIL import Image
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfkit

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
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    
    .pais {
        font-size: 18px;
    }
    
    .destino-content {
        margin-top: 20px;
    }
    
    .descripcion {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        line-height: 1.6;
        color: black;
    }
    
    .info-tag {
        display: inline-block;
        padding: 8px 15px;
        margin: 5px;
        border-radius: 20px;
        font-size: 14px;
        color: black;
    }
    
    .epoca {
        background: #e3f2fd;
    }
    
    .duracion {
        background: #f3e5f5;
    }
    
    .separador {
        height: 2px;
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
    # Grid principal con logo y título
    col_logo, col_title = st.columns([1, 2])
    
    with col_logo:
        try:
            st.image("img/t-vectorizada.png", width=300)
        except:
            st.image("https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png", width=300)
    
    with col_title:
        st.markdown("""
        <div style="padding: 20px;">
            <h1 style="color: #FF4B4B; font-size: 2.5rem; margin-bottom: 1rem;">
                ¡Bienvenido a TuGuIA! 🌎
            </h1>
            <p style="color: #888; font-size: 1.2rem;">
                Tu compañero perfecto para planificar aventuras inolvidables
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Espacio entre el título y los contenedores
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Contenedores principales
    if st.session_state.id_usuario:
        # Si está logueado, mostrar solo la información básica
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; height: 100%;">
                <h3 style="color: #FF4B4B; margin-bottom: 15px;">🎯 Tu Destino, Tu Aventura</h3>
                <p style="color: white; margin-bottom: 20px;">
                    Descubre lugares increíbles basados en tus preferencias personales.
                    Planifica tu próximo viaje con recomendaciones personalizadas y
                    consejos de expertos.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; height: 100%;">
                <h3 style="color: #FF4B4B; margin-bottom: 15px;">✨ Características</h3>
                <ul style="list-style-type: none; padding: 0; color: white;">
                    <li style="margin: 10px 0;">🎯 Recomendaciones personalizadas</li>
                    <li style="margin: 10px 0;">🗺️ Planificación de itinerarios</li>
                    <li style="margin: 10px 0;">🌟 Destinos únicos</li>
                    <li style="margin: 10px 0;">📅 Organización de viajes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Si no está logueado, mostrar contenido completo
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; height: 100%;">
                <h3 style="color: #FF4B4B; margin-bottom: 15px;">🎯 Tu Destino, Tu Aventura</h3>
                <p style="color: white; margin-bottom: 20px;">
                    Descubre lugares increíbles basados en tus preferencias personales.
                    Planifica tu próximo viaje con recomendaciones personalizadas y
                    consejos de expertos.
                </p>
                <div style="color: white;">
                    <h4 style="color: #FF4B4B;">✨ Características</h4>
                    <ul style="list-style-type: none; padding: 0;">
                        <li style="margin: 10px 0;">🎯 Recomendaciones personalizadas</li>
                        <li style="margin: 10px 0;">🗺️ Planificación de itinerarios</li>
                        <li style="margin: 10px 0;">🌟 Destinos únicos</li>
                        <li style="margin: 10px 0;">📅 Organización de viajes</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.get('mostrar_login', False):
                st.markdown("""
                <div style="background: #1E1E1E; padding: 25px; border-radius: 15px;">
                    <h3 style="color: #FF4B4B; margin-bottom: 15px;">🔑 Inicia Sesión</h3>
                """, unsafe_allow_html=True)
                
                email = st.text_input("📧 Email", placeholder="tucorreo@ejemplo.com", key="login_email")
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                    if st.button("🚀 ¡Comenzar la Aventura!", key="login_button"):
                        if email:
                            user_id = obtener_usuario_por_email(email)
                            if user_id:
                                st.session_state.id_usuario = user_id
                                st.session_state.mostrar_login = False
                                st.rerun()
                            else:
                                st.error("Usuario no encontrado")
                                if st.button("📝 Registrarme ahora"):
                                    st.session_state.mostrar_login = False
                                    st.session_state.mostrar_registro = True
                                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #1E1E1E; padding: 25px; border-radius: 15px;">
                    <h3 style="color: #FF4B4B; margin-bottom: 15px;">🚀 Comienza Tu Viaje</h3>
                    <div style="color: white;">
                        <p style="margin-bottom: 20px;">Sigue estos pasos para comenzar:</p>
                        <ol style="padding-left: 20px;">
                            <li style="margin: 10px 0;">Regístrate o inicia sesión</li>
                            <li style="margin: 10px 0;">Completa tus preferencias</li>
                            <li style="margin: 10px 0;">Obtén recomendaciones personalizadas</li>
                            <li style="margin: 10px 0;">¡Planifica tu aventura!</li>
                        </ol>
                    </div>
                    <div style="margin-top: 20px;">
                        <div class="row">
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔑 Iniciar Sesión", use_container_width=True):
                        st.session_state.mostrar_login = True
                        st.session_state.mostrar_registro = False
                with col2:
                    if st.button("📝 Registrarse", use_container_width=True):
                        st.session_state.mostrar_registro = True
                        st.session_state.mostrar_login = False
                
                st.markdown("""
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Función para obtener datos del usuario y guardarlos en la base de datos
def obtener_datos_usuario():
    st.title("Registro de Usuario")
    
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    travel_style = st.selectbox("Estilo de viaje", ["solo", "amigos", "pareja", "trabajo"])
    
    if st.button("Registrar"):
        if name and email:
            if f.insertar_usuario(name, email, travel_style, registration_date):
                st.success("¡Registro exitoso! 🎉")
                st.balloons()
        else:
            st.warning("Por favor, completa todos los campos 📝")

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
    st.title("✨ Descubre Lugares Increíbles")
    
    # Agregar sección explicativa
    st.markdown("""
    <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; margin-bottom: 30px;">
        <h3 style="color: #FF4B4B; margin-bottom: 15px;">🎯 Sistema de Recomendación Inteligente</h3>
        <p style="color: #fff; margin-bottom: 15px;">
            Nuestro algoritmo analiza tus preferencias y utiliza inteligencia artificial para sugerirte 
            destinos perfectamente adaptados a tus gustos. Para cada destino, te proporcionamos:
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; color: #fff;">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">📸 Visualización</h4>
                <p>Imágenes reales del destino para inspirarte</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">🗓️ Planificación</h4>
                <p>Mejor época para visitar y duración recomendada</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">🎯 Actividades</h4>
                <p>Experiencias destacadas con enlaces directos</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if "id_usuario" not in st.session_state or st.session_state.id_usuario is None:
        st.warning("Por favor, inicia sesión primero")
        return
    
    user_id = st.session_state.id_usuario
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(45deg, #FF4B4B, #FF8F8F); 
        border-radius: 15px; margin: 20px 0; color: white;">
        <h3 style="margin: 0;">¿Listo para tu próxima aventura? 🌎</h3>
        <p style="margin: 10px 0 0 0;">Hemos seleccionado estos destinos increíbles basados en tus preferencias</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Descubrir Destinos", use_container_width=True):
        with st.spinner("Creando tu lista de destinos soñados... 🌍"):
            resultado = f.generar_recomendaciones_destinos(user_id)
            
            if isinstance(resultado, dict):
                # Dividir y limpiar las recomendaciones
                destinos = [d for d in resultado['recomendaciones_gpt'].split('---') if d.strip()]
                
                for i, destino in enumerate(destinos, 1):
                    lineas = [l.strip() for l in destino.split('\n') if l.strip()]
                    if not lineas:
                        continue
                        
                    ciudad_pais = lineas[0].replace('Destino:', '').strip().split(',')
                    ciudad = ciudad_pais[0].strip()
                    pais = ciudad_pais[1].strip() if len(ciudad_pais) > 1 else ""
                    
                    # Obtener imagen del destino
                    imagen_url = f.obtener_imagen_lugar(f"{ciudad}, {pais}")
                    
                    st.markdown(f"""
                    <div style="background: #1E1E1E; border-radius: 20px; margin: 40px 0; overflow: hidden;">
                        <div style="background: white; padding: 20px; text-align: center;">
                            <div style="color: #FF4B4B; font-size: 32px; font-weight: bold; text-transform: uppercase;
                                letter-spacing: 2px; margin-bottom: 5px;">{ciudad}</div>
                            <div style="color: #666; font-size: 18px;">{pais}</div>
                        </div>
                        <div style="padding: 20px;">
                            <div style="margin-bottom: 20px;">
                                <img src="{imagen_url}" 
                                    style="width: 100%; height: 300px; object-fit: cover; border-radius: 12px;"
                                    onerror="this.onerror=null; this.src='https://via.placeholder.com/800x400?text=Imagen+no+disponible';">
                            </div>
                    """, unsafe_allow_html=True)
                    
                    # Procesar cada línea del destino
                    for linea in lineas[1:]:  # Saltamos la primera línea que ya procesamos
                        if '¿Por qué?:' in linea:
                            descripcion = linea.replace('¿Por qué?:', '').strip()
                            st.markdown(f"""
                            <div style="background: #2E2E2E; padding: 20px; border-radius: 12px; 
                                margin: 10px 0; color: white;">
                                {descripcion}
                            </div>
                            """, unsafe_allow_html=True)
                        elif 'Mejor época:' in linea:
                            epoca = linea.replace('Mejor época:', '').strip()
                            st.markdown(f"""
                            <div style="display: inline-block; background: #2E2E2E; color: white;
                                padding: 8px 15px; border-radius: 20px; margin: 5px;">
                                🗓️ Estación recomendada para viajar: {epoca}
                            </div>
                            """, unsafe_allow_html=True)
                        elif 'Duración sugerida:' in linea:
                            duracion = linea.replace('Duración sugerida:', '').strip()
                            st.markdown(f"""
                            <div style="display: inline-block; background: #2E2E2E; color: white;
                                padding: 8px 15px; border-radius: 20px; margin: 5px;">
                                ⏱️ Rango de días recomendados: {duracion}
                            </div>
                            """, unsafe_allow_html=True)
                        elif 'Actividad destacada:' in linea:
                            nombre, link = linea.split('|')
                            nombre = nombre.replace('Actividad destacada:', '').strip()
                            link = link.strip()
                            st.markdown(f"""
                            <a href="{link}" target="_blank" style="text-decoration: none;">
                                <div style="background: #FF4B4B; color: white; padding: 12px 20px;
                                    border-radius: 12px; margin-top: 15px; display: inline-block;">
                                    🎯 Actividad recomendada: {nombre}
                                </div>
                            </a>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.error(resultado)

# Función para generar itinerario
def mostrar_itinerario():
    st.title("✨ Planifica tus Actividades")
    
    # Agregar sección explicativa
    st.markdown("""
    <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; margin-bottom: 30px;">
        <h3 style="color: #FF4B4B; margin-bottom: 15px;">🗺️ Planificador Inteligente de Itinerarios</h3>
        <p style="color: #fff; margin-bottom: 15px;">
            Utilizando tecnología de IA avanzada, creamos itinerarios personalizados que maximizan tu experiencia de viaje.
            Nuestro sistema considera:
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; color: #fff;">
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">⭐ Score Personalizado</h4>
                <p>Actividades puntuadas según tus preferencias</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">📅 Optimización Temporal</h4>
                <p>Organización eficiente de actividades por día</p>
            </div>
            <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px;">
                <h4 style="color: #FF4B4B;">🎯 Experiencias Únicas</h4>
                <p>Recomendaciones basadas en datos reales</p>
            </div>
        </div>
        <p style="color: #888; font-size: 0.9em; margin-top: 15px; text-align: center;">
            Powered by OpenAI GPT & Google Places API
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if "id_usuario" not in st.session_state or st.session_state.id_usuario is None:
        st.warning("Por favor, inicia sesión primero")
        return
    
    user_id = st.session_state.id_usuario
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(45deg, #FF4B4B, #FF8F8F); 
        border-radius: 15px; margin: 20px 0; color: white;">
        <h3 style="margin: 0;">¿A dónde te gustaría ir? 🌎</h3>
        <p style="margin: 10px 0 0 0;">Generaremos un itinerario personalizado para tu próxima aventura</p>
    </div>
    """, unsafe_allow_html=True)
    
    destino = st.text_input(
        label="Destino",
        placeholder="Escribe tu destino aquí...",
        help="Por ejemplo: 'Tokio', 'Barcelona', 'Nueva York'",
        label_visibility="collapsed"
    )
    
    # Contenedor de fechas más compacto
    col_main1, col_main2, col_main3 = st.columns([1,2,1])
    with col_main2:
        st.markdown("""
        <div style="background: #1E1E1E; padding: 20px; border-radius: 15px; margin: 20px 0; max-width: 600px;">
            <h4 style="color: #FF4B4B; margin-bottom: 15px; text-align: center;">📅 Fechas del Viaje</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Checkbox y texto informativo en la misma línea
        col_check1, col_check2 = st.columns([1.5, 2])
        with col_check1:
            incluir_clima = st.checkbox("🌤️ Incluir información del clima")
        with col_check2:
            st.markdown("""
            <div style="padding-top: 5px;">
                <span style="background: #FF4B4B; color: white; padding: 3px 8px; border-radius: 10px; font-size: 0.8em;">
                    Solo para viajes en los próximos 15 días
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Fecha de inicio", min_value=datetime.now().date())
        with col2:
            fecha_fin = st.date_input("Fecha de fin", min_value=fecha_inicio)
    
    # Validar fechas y mostrar mensajes
    dias_hasta_viaje = (fecha_inicio - datetime.now().date()).days
    if incluir_clima and dias_hasta_viaje > 15:
        st.warning("⚠️ El pronóstico del clima solo está disponible para los próximos 15 días. Se generará un itinerario sin información del clima.")
        incluir_clima = False
    
    if st.button("🗺️ Generar Itinerario", use_container_width=True):
        if not destino:
            st.warning("Por favor, ingresa un destino")
            return
            
        with st.spinner("Creando tu itinerario personalizado... 🌍"):
            resultado = f.generar_itinerario(
                destino, 
                user_id, 
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                incluir_clima=incluir_clima
            )
            
            if isinstance(resultado, dict) and 'actividades' in resultado:
                st.markdown(f"""
                <div style="background: #1E1E1E; border-radius: 20px; margin: 40px 0; overflow: hidden;">
                    <div style="background: white; padding: 20px; text-align: center;">
                        <div style="color: #FF4B4B; font-size: 32px; font-weight: bold; text-transform: uppercase;
                            letter-spacing: 2px; margin-bottom: 5px;">Tu Itinerario en {destino}</div>
                        <div style="color: #666; font-size: 18px;">Elige tus actividades favoritas</div>
                    </div>
                """, unsafe_allow_html=True)

                # Mostrar el clima si está disponible
                if incluir_clima and resultado.get('clima_html'):
                    st.markdown(resultado['clima_html'], unsafe_allow_html=True)

                # Contenedor para las actividades
                st.markdown("""
                <div style="padding: 25px;">
                """, unsafe_allow_html=True)

                # Mostrar actividades
                for i, act in enumerate(resultado['actividades'], 1):
                    st.markdown(f"""
                    <div style="background: white; border-radius: 15px; margin-bottom: 25px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2); overflow: hidden;">
                        <div style="background: linear-gradient(45deg, #FF4B4B, #FF6B6B); padding: 15px 25px; 
                            color: white; font-weight: bold; font-size: 20px;">
                            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; 
                                border-radius: 20px; margin-right: 10px;">Día {i}</span>
                            {act['nombre']}
                        </div>
                        <div style="padding: 25px;">
                            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px;">
                                <div>
                                    <img src="{act.get('imagen_url', 'https://via.placeholder.com/400x300?text=Imagen+no+disponible')}" 
                                        style="width: 100%; height: 250px; object-fit: cover; border-radius: 10px;"
                                        onerror="this.onerror=null; this.src='https://via.placeholder.com/400x300?text=Imagen+no+disponible';">
                                </div>
                                <div>
                                    <div style="color: #333; line-height: 1.6; font-size: 16px; 
                                        background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                        {act.get('DESCRIPCION', act.get('descripcion', 'No hay descripción disponible'))}
                                    </div>
                                    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                                        <div style="background: #FFE5E5; color: #FF4B4B; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            ⏱️ {act.get('DURACION', act.get('duracion', 'Duración no especificada'))}
                                        </div>
                                        <div style="background: #f0f0f0; color: #333; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            🗓️ {act.get('MEJOR_EPOCA', act.get('mejor_epoca', 'Época no especificada'))}
                                        </div>
                                        <div style="background: #FFE5E5; color: #FF4B4B; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            ⭐ Score: {act.get('score', 0.0):.2f}
                                        </div>
                                    </div>
                                    <a href="{act.get('LINK', act.get('link', '#'))}" target="_blank" style="text-decoration: none;">
                                        <div style="background: #FF4B4B; color: white; padding: 12px 20px;
                                            border-radius: 10px; display: inline-block; transition: all 0.3s ease;">
                                            🔗 Ver más detalles
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Cerrar todos los contenedores
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Contenedor de descarga más compacto
                col_pdf1, col_pdf2, col_pdf3 = st.columns([1,2,1])
                with col_pdf2:
                    st.markdown("""
                    <div style="background: #1E1E1E; padding: 15px; border-radius: 15px; margin: 20px auto; max-width: 400px; text-align: center;">
                        <h4 style="color: #FF4B4B; margin-bottom: 10px;">📥 Descarga tu Itinerario</h4>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Primero generamos el PDF
                    pdf_buffer = f.generar_pdf_itinerario(
                        destino,
                        resultado['actividades'],
                        resultado.get('clima_html')
                    )
                    
                    # Botón de descarga
                    st.download_button(
                        label="📄 Descargar PDF",
                        data=pdf_buffer,
                        file_name=f"itinerario_{destino.lower().replace(' ', '_')}.pdf",
                        mime="application/pdf"
                    )
            else:
                st.error("No se pudo generar el itinerario. Por favor, intenta de nuevo.")

# Función para obtener datos del usuario y guardarlos en la base de datos
def obtener_datos_usuario():
    st.title("Registro de Usuario")
    
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    travel_style = st.selectbox("Estilo de viaje", ["solo", "amigos", "pareja", "trabajo"])
    
    if st.button("Registrar"):
        if name and email:
            if f.insertar_usuario(name, email, travel_style, registration_date):
                st.success("¡Registro exitoso! 🎉")
                st.balloons()
        else:
            st.warning("Por favor, completa todos los campos 📝")

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
    # Inicializar variables de sesión
    if "id_usuario" not in st.session_state:
        st.session_state.id_usuario = None
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = "🏠 Inicio"
    if "mostrar_login" not in st.session_state:
        st.session_state.mostrar_login = False
    if "mostrar_registro" not in st.session_state:
        st.session_state.mostrar_registro = False

    # Barra lateral
    with st.sidebar:
        st.markdown("### 🌍 TuGuía")
    if st.session_state.id_usuario:
            st.success("Sesión iniciada ✅")
            if st.button("Cerrar Sesión 👋"):
                st.session_state.id_usuario = None
                st.session_state.pagina_actual = "🏠 Inicio"
                st.session_state.mostrar_login = False
                st.session_state.mostrar_registro = False
                st.rerun()
            
            pagina_actual = st.radio(
                "Navegación",
                ["🏠 Inicio", "⭐ Preferencias", "🎯 Lugares Recomendados", "📍 Planifica tus Actividades"]
            )
            st.session_state.pagina_actual = pagina_actual
    else:
            # Mostrar solo Inicio en el sidebar cuando no hay sesión
            st.radio(
                "Navegación",
                ["🏠 Inicio"],
                key="nav_no_session"  # Agregamos una key única para este radio
            )
            st.session_state.pagina_actual = "🏠 Inicio"
        
        # Agregar información del autor al final del sidebar
        st.markdown("---")  # Línea separadora
        st.markdown("""
        <div style="position: fixed; bottom: 20px; left: 20px; width: calc(100% - 40px);">
            <p style="color: white; font-size: 0.9em; margin-bottom: 10px;">
                Autor: Esteban Daniel Cristos Muzzupappa
            </p>
            <div style="display: flex; gap: 10px;">
                <a href="https://www.linkedin.com/in/esteban-daniel-cristos-muzzupappa-37b72635/" target="_blank" 
                   style="color: white; text-decoration: none; transition: opacity 0.3s ease;">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" 
                         width="20" style="vertical-align: middle;"> LinkedIn
                </a>
                <a href="https://github.com/estcr" target="_blank" 
                   style="color: white; text-decoration: none; transition: opacity 0.3s ease;">
                    <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                         width="20" style="vertical-align: middle;"> GitHub
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar la página correspondiente
    if st.session_state.pagina_actual == "🏠 Inicio":
        pagina_inicio()
    elif st.session_state.pagina_actual == "⭐ Preferencias":
        interfaz_preferencias()
    elif st.session_state.pagina_actual == "🎯 Lugares Recomendados":
        interfaz_recomendaciones()
    elif st.session_state.pagina_actual == "📍 Planifica tus Actividades":
        mostrar_itinerario()

# Ejecutamos la aplicación
if __name__ == "__main__":
    main()

