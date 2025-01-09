import os
import funciones as f
import config as c
import streamlit as st
import pandas as pd
from datetime import datetime

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

    # Formulario de registro de usuario
    st.write("#### Registra tu información (opcional)")
    with st.form(key="form_usuario"):
        name = st.text_input("Nombre")
        email = st.text_input("Email")
        travel_style = st.selectbox("Estilo de viaje", ["solo", "pareja", "amigos", "trabajo"])
        registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        submit_button = st.form_submit_button(label="Registrar Usuario")

    if submit_button:
        if name and email:
            f.insertar_usuario(name, email, travel_style, registration_date)
            st.success(f"Usuario {name} registrado con éxito.")
        else:
            st.error("Por favor, completa todos los campos para registrarte.")

# Función para ingresar las preferencias de viaje
def interfaz_preferencias():
    st.title("Ingrese sus Preferencias de Viaje")

    # Verificamos si el usuario está registrado, pero no es obligatorio
    if "id_usuario" in st.session_state:
        st.info(f"Registrado como: {st.session_state.get('id_usuario', 'Desconocido')}")

    st.write("Por favor, seleccione sus actividades preferidas y el nivel de preferencia para cada una (1: Baja, 5: Muy Alta).")

    with st.form(key="form_preferencias"):
        actividades = {
            "Cultura": st.slider("Cultura", 1, 5, 3),
            "Aventura": st.slider("Aventura", 1, 5, 3),
            "Relax": st.slider("Relax", 1, 5, 3),
            "Deportes": st.slider("Deportes", 1, 5, 3),
            "Gastronomía": st.slider("Gastronomía", 1, 5, 3),
            "Party": st.slider("Party", 1, 5, 3)
        }
        duracion_viaje = st.number_input("Duración del Viaje (días)", min_value=1, max_value=365)

        submit_button = st.form_submit_button(label="Guardar Preferencias")

    if submit_button:
        if actividades and duracion_viaje:
            if "id_usuario" in st.session_state:
                f.insertar_preferencias_viaje(st.session_state.id_usuario, actividades, duracion_viaje)
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
    
    # Input para el destino
    destino = st.text_input("Introduce tu destino")
    
    if st.button("Generar Itinerario"):
        if destino: 
            # Llamar a la función para analizar preferencias y generar recomendaciones
            generar_recomendaciones(destino)
        else:
            st.error("Por favor, introduce un destino.")

# Función para obtener datos del usuario y guardarlos en la base de datos
def obtener_datos_usuario():
    st.title("Registro de Usuario")
    
    name = st.text_input("Nombre")
    email = st.text_input("Email")
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    travel_style = st.selectbox("Estilo de viaje", ["Aventura", "Relajación", "Cultural", "Negocios"])
    
    if st.button("Registrar"):
        f.insertar_usuario(name, email, travel_style, registration_date)
        st.success("Usuario registrado exitosamente")

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
    obtener_datos_usuario()
    main()
