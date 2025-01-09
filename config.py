import toml
import pymysql
import streamlit as st



# Función para conectarse a la base de datos
def conectar_bd():
    # Configuración de la conexión a la base de datos
    db_user = "root"  # Usuario predeterminado
    db_password = st.secrets["database"]["db_pass"]
    db_host = "34.175.207.112"  # Host predeterminado (local)
    db_name = "travel_planner"  # Nombre de la base de datos

    try:
        print("Intentando conectar a la base de datos")
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name
        )
        print("Conexión a la base de datos establecida correctamente")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise Exception(f"Error al conectar a la base de datos: {e}")


#------------------------------------------------------------

