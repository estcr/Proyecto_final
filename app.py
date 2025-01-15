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
    # Contenedor principal con fondo oscuro
    st.markdown("""
    <style>
    .main {
        background-color: #13151a;
    }
    .stButton > button {
        width: 100%;
        background-color: #FF4B4B !important;
        color: white !important;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #ff6b6b !important;
        transform: translateY(-2px);
    }
    .stTextInput > div > div > input {
        background-color: #1E1E1E;
        color: white;
        border: 1px solid #333;
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Layout con columnas
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        # Logo y título
        st.image("https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png", 
                width=150)
        
        # Contenedor del formulario
        st.markdown("""
        <div style="background: #1E1E1E; padding: 2rem; border-radius: 20px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.2); margin: 2rem 0;">
            <div style="text-align: center; margin-bottom: 2rem;">
                <h1 style="color: #FF4B4B; font-size: 2rem; margin-bottom: 0.5rem;">
                    ¡Bienvenido de nuevo! 👋
                </h1>
                <p style="color: #888; font-size: 1rem;">
                    Inicia sesión para continuar tu aventura
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Campo de email con icono
        st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <label style="color: #888; display: block; margin-bottom: 0.5rem;">
                📧 Email
            </label>
        </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("", placeholder="tucorreo@ejemplo.com", 
                             label_visibility="collapsed")
        
        # Botón de inicio de sesión
        if st.button("🚀 Iniciar Sesión"):
            if email:
                user_id = obtener_usuario_por_email(email)
                if user_id:
                    st.session_state.id_usuario = user_id
                    st.success("¡Inicio de sesión exitoso! 🎉")
                    st.session_state.pagina_actual = "🏠 Inicio"
                    st.rerun()
                else:
                    st.error("Usuario no encontrado 😕")
            else:
                st.warning("Por favor, ingresa tu email 📧")
        
        # Enlace para registro
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #888;">¿No tienes una cuenta?</p>
            <a href="#" style="color: #FF4B4B; text-decoration: none; font-weight: bold;">
                ¡Regístrate y comienza tu aventura! ✨
            </a>
        </div>
        </div>
        """, unsafe_allow_html=True)

# Función de registro modernizada
def obtener_datos_usuario():
    col1, col2, col3 = st.columns([1,3,1])
    
    with col2:
        # Logo centrado
        st.image("https://raw.githubusercontent.com/estcr/Proyecto_final/main/img/t-vectorizada.png", width=200)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #FF4B4B; font-size: 2.5em;">¡Únete a la aventura! 🌎</h1>
            <p style="color: #666; font-size: 1.2em;">Crea tu cuenta y descubre destinos increíbles</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Contenedor para el formulario
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
        """, unsafe_allow_html=True)
        
        name = st.text_input("👤 Nombre", placeholder="Tu nombre")
        email = st.text_input("📧 Email", placeholder="tucorreo@ejemplo.com")
        travel_style = st.selectbox("🎒 Estilo de viaje", 
            ["solo", "amigos", "pareja", "trabajo"],
            format_func=lambda x: {
                "solo": "Viajero solitario 🚶",
                "amigos": "Con amigos 👥",
                "pareja": "En pareja 💑",
                "trabajo": "Viaje de trabajo 💼"
            }[x]
        )
        
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if st.button("🚀 Registrarme", use_container_width=True):
            if name and email:
                if f.insertar_usuario(name, email, travel_style, registration_date):
                    st.success("¡Registro exitoso! 🎉")
                    st.balloons()
            else:
                st.warning("Por favor, completa todos los campos 📝")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mensaje para login
        st.markdown("""
        <div style="text-align: center; margin-top: 20px;">
            <p style="color: #666;">¿Ya tienes una cuenta?</p>
            <p style="color: #FF4B4B; font-weight: bold;">¡Inicia sesión y continúa tu aventura!</p>
        </div>
        """, unsafe_allow_html=True)

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
                                🗓️ {epoca}
                            </div>
                            """, unsafe_allow_html=True)
                        elif 'Duración sugerida:' in linea:
                            duracion = linea.replace('Duración sugerida:', '').strip()
                            st.markdown(f"""
                            <div style="display: inline-block; background: #2E2E2E; color: white;
                                padding: 8px 15px; border-radius: 20px; margin: 5px;">
                                ⏱️ {duracion}
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
                                    🎯 {nombre}
                                </div>
                            </a>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
            else:
                st.error(resultado)

# Función para generar itinerario
def mostrar_itinerario():
    st.title("✨ Planifica tus Actividades")
    
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
    
    if st.button("🗺️ Generar Itinerario", use_container_width=True):
        if not destino:
            st.warning("Por favor, ingresa un destino")
            return
            
        with st.spinner("Creando tu itinerario personalizado... 🌍"):
            resultado = f.generar_itinerario(destino, user_id)
            
            if isinstance(resultado, dict) and 'actividades' in resultado:
                st.markdown(f"""
                <div style="background: #1E1E1E; border-radius: 20px; margin: 40px 0; overflow: hidden;">
                    <div style="background: white; padding: 20px; text-align: center;">
                        <div style="color: #FF4B4B; font-size: 32px; font-weight: bold; text-transform: uppercase;
                            letter-spacing: 2px; margin-bottom: 5px;">Tu Itinerario en {destino}</div>
                        <div style="color: #666; font-size: 18px;">Actividades día a día</div>
                    </div>
                    <div style="padding: 25px;">
                """, unsafe_allow_html=True)
                
                for i, act in enumerate(resultado['actividades'], 1):
                    st.markdown(f"""
                    <div style="background: white; border-radius: 15px; margin-bottom: 25px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2); overflow: hidden;">
                        <div style="background: linear-gradient(45deg, #FF4B4B, #FF6B6B); padding: 15px 25px; 
                            color: white; font-weight: bold; font-size: 20px;">
                            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; 
                                border-radius: 20px; margin-right: 10px;">Actividad {i}</span>
                            {act['nombre']}
                        </div>
                        <div style="padding: 25px;">
                            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px;">
                                <div>
                                    <img src="{act['imagen_url']}" 
                                        style="width: 100%; height: 250px; object-fit: cover; border-radius: 10px;"
                                        onerror="this.onerror=null; this.src='https://via.placeholder.com/400x300?text=Imagen+no+disponible';">
                                </div>
                                <div>
                                    <div style="color: #333; line-height: 1.6; font-size: 16px; 
                                        background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                        {act['descripcion']}
                                    </div>
                                    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                                        <div style="background: #FFE5E5; color: #FF4B4B; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            ⏱️ {act['duracion']}
                                        </div>
                                        <div style="background: #f0f0f0; color: #333; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            🗓️ {act['mejor_epoca']}
                                        </div>
                                        <div style="background: #FFE5E5; color: #FF4B4B; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            ⭐ Score: {act['score']:.2f}
                                        </div>
                                    </div>
                                    <a href="{act['link']}" target="_blank" style="text-decoration: none;">
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
                
                st.markdown("""
                    </div>
                </div>
                """, unsafe_allow_html=True)
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
                ["🏠 Inicio", "⭐ Preferencias", "🎯 Lugares Recomendados", "📍 Planifica tus Actividades"]
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
    elif pagina_actual == "🎯 Lugares Recomendados":
        interfaz_recomendaciones()
    elif pagina_actual == "📍 Planifica tus Actividades":
        mostrar_itinerario()

# Ejecutamos la aplicación
if __name__ == "__main__":
    main()

