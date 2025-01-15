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
    # Estilos para la página de inicio de sesión
    st.markdown("""
        <style>
        .main {
            background-color: #13151a;
        }
        .stButton > button {
            background-color: #1a1c23;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 5px;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #2e3138;
        }
        .stTextInput > div > div > input {
            background-color: #1a1c23;
            color: white;
            border: none;
            padding: 15px;
            border-radius: 5px;
        }
        .login-title {
            color: white;
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
        }
        .email-label {
            color: white;
            font-size: 16px;
            margin-bottom: 10px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logo y título
    mostrar_logo()
    st.markdown('<h1 class="login-title">Inicio de Sesión</h1>', unsafe_allow_html=True)
    
    # Formulario de inicio de sesión
    with st.form("login_form", clear_on_submit=True):
        st.markdown('<p class="email-label">Email</p>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="tucorreo@ejemplo.com", label_visibility="collapsed")
        submitted = st.form_submit_button("Iniciar Sesión")
        
        if submitted:
            if email:
                user_id = obtener_usuario_por_email(email)
                if user_id:
                    st.session_state.id_usuario = user_id
                    st.success("¡Inicio de sesión exitoso!")
                    st.session_state.pagina_actual = "🏠 Inicio"
                    st.rerun()
                else:
                    st.error("Usuario no encontrado")
            else:
                st.warning("Por favor, ingresa tu email")

# Función de registro modernizada
def obtener_datos_usuario():
    # Estilos para el registro
    st.markdown("""
        <style>
        .main {
            background-color: #1a1a1a;
        }
        .registro-container {
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            margin: 20px auto;
            max-width: 600px;
        }
        .registro-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .registro-input {
            background: #f8f9fa;
            border: none;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            width: 100%;
        }
        .registro-button {
            background: #FF4B4B;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            font-weight: bold;
            width: 100%;
            margin-top: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .registro-button:hover {
            background: #ff6b6b;
            transform: translateY(-2px);
        }
        .travel-style-option {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .travel-style-option:hover {
            background: #e9ecef;
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Logo y contenido
    mostrar_logo()
    
    st.markdown("""
        <div class="registro-container">
            <div class="registro-header">
                <h1 style="color: #2e7bcf;">¡Únete a la Aventura! ✈️</h1>
                <p style="color: #666; font-size: 1.1em;">
                    Crea tu cuenta y descubre destinos increíbles
                </p>
            </div>
    """, unsafe_allow_html=True)
    
    with st.form("registro_form"):
        name = st.text_input("👤 Nombre", placeholder="Tu nombre")
        email = st.text_input("📧 Email", placeholder="tucorreo@ejemplo.com")
        
        st.markdown("#### ¿Cómo te gusta viajar? 🌎")
        travel_style = st.selectbox("", [
            "Solo aventurero 🚶",
            "Con amigos 👥",
            "En pareja 💑",
            "Por trabajo 💼"
        ])
        
        submitted = st.form_submit_button("¡Crear mi cuenta!", use_container_width=True)
        
        if submitted:
            if name and email:
                registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                travel_style_clean = travel_style.split(" ")[0].lower()
                
                if f.insertar_usuario(name, email, travel_style_clean, registration_date):
                    st.balloons()
                    st.success("¡Bienvenido a bordo! 🎉")
                    if st.button("¡Comenzar mi aventura! 🚀", use_container_width=True):
                        st.session_state.pagina_actual = "⭐ Preferencias"
                        st.rerun()
                else:
                    st.error("Este email ya está registrado 📧")
            else:
                st.warning("Por favor, completa todos los campos 🙏")

    st.markdown("</div>", unsafe_allow_html=True)

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
    st.title("✨ Descubre Tu Próximo Destino")
    
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
                    
                    # Extraer información
                    info_destino = {}
                    for linea in lineas:
                        if linea.startswith('Destino:'):
                            ciudad_pais = linea.replace('Destino:', '').strip().split(',')
                            info_destino['ciudad'] = ciudad_pais[0].strip()
                            info_destino['pais'] = ciudad_pais[1].strip() if len(ciudad_pais) > 1 else ""
                        elif linea.startswith('¿Por qué?:'):
                            info_destino['descripcion'] = linea.replace('¿Por qué?:', '').strip()
                        elif linea.startswith('Mejor época:'):
                            info_destino['epoca'] = linea.replace('Mejor época:', '').strip()
                        elif linea.startswith('Duración sugerida:'):
                            info_destino['duracion'] = linea.replace('Duración sugerida:', '').strip()
                        elif linea.startswith('Actividad destacada:'):
                            actividad_info = linea.replace('Actividad destacada:', '').split('|')
                            info_destino['actividad'] = actividad_info[0].strip()
                            info_destino['link'] = actividad_info[1].strip() if len(actividad_info) > 1 else "#"
                    
                    # Obtener imagen del destino
                    imagen_url = f.obtener_imagen_lugar(f"{info_destino['ciudad']}, {info_destino['pais']}")
                    
                    # Mostrar el destino en un contenedor bonito
                    st.markdown(f"""
                    <div style="background: white; border-radius: 15px; margin-bottom: 25px; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.2); overflow: hidden;">
                        <div style="background: linear-gradient(45deg, #FF4B4B, #FF6B6B); padding: 15px 25px; 
                            color: white; font-weight: bold; font-size: 20px;">
                            <span style="background: rgba(255,255,255,0.2); padding: 5px 15px; 
                                border-radius: 20px; margin-right: 10px;">#{i}</span>
                            {info_destino['ciudad']}, {info_destino['pais']}
                        </div>
                        
                        <div style="padding: 25px;">
                            <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 20px;">
                                <div>
                                    <img src="{imagen_url}" 
                                        style="width: 100%; height: 250px; object-fit: cover; border-radius: 10px;"
                                        onerror="this.onerror=null; this.src='https://via.placeholder.com/400x300?text=Imagen+no+disponible';">
                                </div>
                                <div>
                                    <div style="color: #333; line-height: 1.6; font-size: 16px; 
                                        background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                                        {info_destino['descripcion']}
                                    </div>
                                    
                                    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                                        <div style="background: #FFE5E5; color: #FF4B4B; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            🗓️ {info_destino['epoca']}
                                        </div>
                                        <div style="background: #f0f0f0; color: #333; padding: 8px 15px; 
                                            border-radius: 20px; font-size: 14px;">
                                            ⏱️ {info_destino['duracion']}
                                        </div>
                                    </div>
                                    
                                    <a href="{info_destino['link']}" target="_blank" style="text-decoration: none;">
                                        <div style="background: #FF4B4B; color: white; padding: 12px 20px;
                                            border-radius: 10px; display: inline-block; transition: all 0.3s ease;">
                                            🎯 {info_destino['actividad']}
                                        </div>
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(resultado)

# Función para generar itinerario
def mostrar_itinerario():
    st.title("✨ Planifica Tu Aventura")
    
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
                                border-radius: 20px; margin-right: 10px;">Día {i}</span>
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

