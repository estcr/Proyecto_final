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
        display: block !important;
        text-transform: uppercase;
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
    
    st.markdown("""
    ### ¿No sabes dónde viajar? 🤔
    Basándonos en tus preferencias y estilo de viaje, hemos seleccionado estos destinos 
    increíbles que creemos que te encantarán. Cada recomendación está personalizada 
    según tus intereses y la forma en que te gusta viajar. ¡Descubre tu próxima aventura! ✨
    """)
    
    user_id = st.session_state.id_usuario
    
    if st.button("Descubrir Destinos Perfectos ✨"):
        with st.spinner("Creando tu lista de destinos soñados... 🌍"):
            resultado = f.generar_recomendaciones_destinos(user_id)
            
            if isinstance(resultado, dict):
                recomendaciones = [rec.strip() for rec in resultado['recomendaciones_gpt'].split('---') if rec.strip()]
                
                for i, rec in enumerate(recomendaciones, 1):
                    try:
                        # Limpiar y dividir las líneas, eliminando líneas vacías
                        lines = [line.strip() for line in rec.split('\n') if line.strip()]
                        
                        # Obtener el destino de manera más robusta
                        destino_line = next((line for line in lines if line.startswith('Destino:')), '')
                        destino = destino_line.replace('Destino:', '').strip()
                        
                        # Separar ciudad y país
                        ciudad, pais = [part.strip() for part in destino.split(',')] if ',' in destino else (destino, '')
                        
                        # Crear la tarjeta del destino
                        st.markdown(f"""
                        <div class="destino-card">
                        <div class="numero-destino">#{i}</div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([1, 2])
                        
                        # Columna de imagen
                        with col1:
                            try:
                                imagen_url = f.obtener_imagen_lugar(f"{ciudad}, {pais}")
                                if imagen_url:
                                    response = requests.get(imagen_url)
                                    if response.status_code == 200:
                                        img = Image.open(BytesIO(response.content))
                                        st.markdown('<div class="imagen-container">', unsafe_allow_html=True)
                                        st.image(img, width=200, use_container_width=True)
                                        st.markdown('</div>', unsafe_allow_html=True)
                                    else:
                                        st.warning("🖼️ Imagen no disponible")
                            except Exception as e:
                                st.warning("🖼️ Imagen no disponible")
                        
                        # Columna de información
                        with col2:
                            # Mostrar el título del destino de manera consistente
                            if ciudad and pais:
                                st.markdown(f"""
                                <div class="destino-titulo">
                                    {ciudad}<br>
                                    <span style="font-size: 18px; color: #666;">{pais}</span>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="destino-titulo">{destino}</div>', 
                                          unsafe_allow_html=True)
                            
                            # Procesar el resto de la información
                            for line in lines:
                                if not line.startswith('Destino:'):
                                    if 'Mejor época:' in line:
                                        epoca = line.replace('Mejor época:', '').strip()
                                        st.markdown(f'<span class="info-tag">🗓️ {epoca}</span>', 
                                                  unsafe_allow_html=True)
                                    elif 'Duración sugerida:' in line:
                                        duracion = line.replace('Duración sugerida:', '').strip()
                                        st.markdown(f'<span class="info-tag">⏱️ {duracion}</span>', 
                                                  unsafe_allow_html=True)
                                    elif '|' in line and 'http' in line:
                                        nombre, link = line.split('|', 1)
                                        link = link.strip()
                                        st.markdown(f"<a href='{link}' target='_blank' class='actividad-link'>🎯 {nombre.strip()}</a>", 
                                                  unsafe_allow_html=True)
                                    elif '¿Por qué?' in line:
                                        texto = line.replace('¿Por qué?:', '').strip()
                                        st.markdown(f"<div class='porque-texto'>💡 {texto}</div>", 
                                                  unsafe_allow_html=True)
                                    else:
                                        st.markdown(f"<p>{line}</p>", unsafe_allow_html=True)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Error al procesar destino {i}: {str(e)}")
                        continue
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
