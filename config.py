import toml
import pymysql

config = toml.load(".streamlit/config.toml")

# Configuración de la conexión a la base de datos
db_user = "root"  # Usuario predeterminado
db_password = config["database"]["db_pass"]
db_host = "34.175.207.112"  # Host predeterminado (local)
db_name = "travel_planner"  # Nombre de la base de datos

# Función para conectarse a la base de datos
def conectar_bd():
    try:
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            db=db_name
        )
        return conn
    except Exception as e:
        raise Exception(f"Error al conectar a la base de datos: {e}")


#------------------------------------------------------------

