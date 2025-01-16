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
                ¡Bienvenido a TuGuÍA! 🌎
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
            </div>
            """, unsafe_allow_html=True)
            
            # Formulario de inicio de sesión
            if st.session_state.get('mostrar_login', False):
                st.markdown("""
                <div style="background: #2E2E2E; padding: 20px; border-radius: 15px; margin-top: 20px;">
                    <h4 style="color: #FF4B4B; text-align: center; margin-bottom: 15px;">
                        🔑 Inicia Sesión
                    </h4>
                </div>
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
                                if st.button("📝 ¿Quieres registrarte?", key="register_redirect"):
                                    st.session_state.mostrar_login = False
                                    st.session_state.mostrar_registro = True
                                    st.rerun()
                else:
                    # Botones de acción
                    st.markdown("<div style='padding: 20px;'></div>", unsafe_allow_html=True)
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔑 Iniciar Sesión", use_container_width=True):
                            st.session_state.mostrar_login = True
                            st.session_state.mostrar_registro = False
                    with col2:
                        if st.button("📝 Registrarse", use_container_width=True):
                            st.session_state.mostrar_registro = True
                            st.session_state.mostrar_login = False
            else:
                # Contenedor de bienvenida para usuarios logueados
                st.markdown("""
                <div style="background: #1E1E1E; padding: 25px; border-radius: 15px; height: 100%;">
                    <h3 style="color: #FF4B4B; margin-bottom: 15px;">✨ ¡Bienvenido de nuevo!</h3>
                    <div style="color: white;">
                        <p style="margin-bottom: 20px;">¿Qué te gustaría hacer hoy?</p>
                        <ul style="list-style-type: none; padding: 0;">
                            <li style="margin: 15px 0;">⭐ Actualiza tus preferencias de viaje</li>
                            <li style="margin: 15px 0;">🎯 Descubre nuevos destinos recomendados</li>
                            <li style="margin: 15px 0;">📍 Planifica tu próxima aventura</li>
                            <li style="margin: 15px 0;">🌍 Explora destinos únicos</li>
                        </ul>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# Función principal
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
        # Solo el logo con el texto "TuGuÍA"
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <img src="https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png" 
                 style="width: 180px; margin: 0 auto;">
            <h1 style="color: white; font-size: 1.5rem; margin: 0;">TuGuÍA</h1>
        </div>
        """, unsafe_allow_html=True)

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

