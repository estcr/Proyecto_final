import streamlit as st
import funciones as f
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="TuGuía", page_icon="🌍")

# Función para mostrar el logo
def mostrar_logo():
    st.image("img/logo.png", width=200)  # Asegúrate de que la imagen esté en la carpeta correcta

# Función para la página de inicio
def pagina_inicio():
    mostrar_logo()
    
    # Contenedor principal con estilo moderno
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
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
                            user_id = f.obtener_usuario_por_email(email)
                            if user_id:
                                st.session_state.id_usuario = user_id
                                st.session_state.mostrar_login = False
                                st.rerun()
                            else:
                                st.error("Usuario no encontrado")
                                st.button("📝 ¿Quieres registrarte?", key="register_redirect")
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
        # Solo el texto "TuGuÍA" con emoji
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: white; font-size: 1.5rem; margin: 0;">🌍 TuGuÍA</h1>
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

