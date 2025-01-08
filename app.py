import os
from dotenv import load_dotenv
import pymysql
import streamlit as st
import openai

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a la base de datos
db_user = "root"  # Usuario predeterminado
db_password = os.getenv("db_pass", "default_password")  # Contraseña desde .env
db_host = "google"  # Host predeterminado (local)
db_name = "travel_planner"  # Nombre de la base de datos

# Función para verificar la conexión a la base de datos
def verificar_conexion():
    try:
        # Intentamos conectar a la base de datos
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name
        )
        st.success("Conexión exitosa a la base de datos.")
        conn.close()  # Cerramos la conexión después de verificar
    except Exception as e:
        st.error(f"Error al conectar a la base de datos: {e}")

# Llamamos a la función para verificar la conexión
verificar_conexion()


# Función para mostrar la página de inicio con explicación del proyecto y registro de usuario
def pagina_inicio():
    st.title("Bienvenido a la Aplicación de Recomendación de Viajes")
    st.write("""
    Este proyecto tiene como objetivo ayudar a los usuarios a planificar sus viajes recomendándoles lugares
    según sus preferencias personales, como el tipo de viaje, actividades que les gustan y la duración del mismo.
    Podrás registrar tus datos, elegir tus preferencias de viaje y obtener recomendaciones personalizadas.
    """)
    st.write("### Pasos a seguir:")
    st.write("1. Registra tu nombre y correo electrónico (opcional).")
    st.write("2. Completa tus preferencias de viaje.")
    st.write("3. Obtén recomendaciones de lugares basadas en tus intereses.")
    st.write("4. Planifica tu itinerario.")
    st.write("**¡Vamos a empezar!**")

    # Formulario de registro de usuario (con contraseña)
    st.write("#### Registra tu información (opcional)")
    with st.form(key="form_usuario"):
        nombre = st.text_input("Nombre")
        email = st.text_input("Email")
        password = st.text_input("Contraseña", type="password")  # Campo para la contraseña
        submit_button = st.form_submit_button(label="Registrar Usuario")

    if submit_button:
        if nombre and email and password:
            # Aquí llamarías a una función que inserte al usuario en la base de datos
            st.success(f"Usuario {nombre} registrado con éxito.")
        else:
            st.error("Por favor, completa todos los campos para registrarte.")

# Función para ingresar las preferencias de viaje
def interfaz_preferencias():
    st.title("Ingrese sus Preferencias de Viaje")

    # Verificamos si el usuario está registrado, pero no es obligatorio
    if "id_usuario" in st.session_state:
        st.info(f"Registrado como: {st.session_state.get('id_usuario', 'Desconocido')}")

    with st.form(key="form_preferencias"):
        tipo_viaje = st.selectbox("Tipo de Viaje", ["Solo", "Pareja", "Amigos", "Familia", "Negocios"])
        actividades = st.multiselect("Actividades que le interesan", ["Cultura", "Aventura", "Relax", "Deportes", "Gastronomía", "Party"])
        duracion_viaje = st.number_input("Duración del Viaje (días)", min_value=1, max_value=365)

        submit_button = st.form_submit_button(label="Guardar Preferencias")

    if submit_button:
        if tipo_viaje and actividades and duracion_viaje:
            if "id_usuario" in st.session_state:
                # Si hay un usuario registrado, guardamos las preferencias en la base de datos
                st.success("Preferencias guardadas con éxito.")
            else:
                st.info("Preferencias guardadas localmente, pero no se asociaron con ningún usuario registrado.")
        else:
            st.error("Por favor, complete todos los campos.")

# Función para mostrar recomendaciones personalizadas
def interfaz_recomendaciones():
    st.title("Recomendaciones Personalizadas")
    st.write("Aquí se mostrarán lugares recomendados basados en tus preferencias.")
    # Aquí iría la lógica para mostrar las recomendaciones según las preferencias del usuario.

# Función para generar itinerario
def interfaz_itinerario():
    st.title("Generar Itinerario")
    st.write("Aquí podrás crear tu itinerario basado en las recomendaciones de lugares.")
    # Aquí iría la lógica para crear el itinerario basado en las recomendaciones.

# Llamamos a la interfaz principal con la barra lateral
def main():
    # Aseguramos que las variables de sesión estén inicializadas
    if "id_usuario" not in st.session_state:
        st.session_state.id_usuario = None

    # Barra lateral de navegación
    st.sidebar.title("Navegación")
    pagina_actual = st.sidebar.radio(
        "Selecciona una página", ["Inicio", "Preferencias de Viaje", "Recomendaciones", "Itinerario"]
    )

    # Condicionales para mostrar las páginas correspondientes
    if pagina_actual == "Inicio":
        pagina_inicio()
    elif pagina_actual == "Preferencias de Viaje":
        interfaz_preferencias()
    elif pagina_actual == "Recomendaciones":
        interfaz_recomendaciones()
    elif pagina_actual == "Itinerario":
        interfaz_itinerario()

# Ejecutamos la aplicación
if __name__ == "__main__":
    main()
