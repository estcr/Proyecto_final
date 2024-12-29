# Conectar el notebook con la base de datos
# Load .evn file with password db_pass


def get_db_engine():
    from dotenv import load_dotenv
    import os
    import pandas as pd
    import pymysql
    from sqlalchemy import create_engine
    
    # Especificar la ruta relativa al archivo .env
    load_dotenv(dotenv_path='Sql/.env')
    
    db_pass = os.getenv("db_pass")
    
    if db_pass is None:
        raise ValueError("La variable de entorno 'db_pass' no se ha encontrado.")
    
    # Obtener la contraseña de forma segura
    password = db_pass
    
    # Configuración de la base de datos y la conexión
    bd = "planificador_viajes"
    connection_string = 'mysql+pymysql://root:' + password + '@127.0.0.1/' + bd
    engine = create_engine(connection_string)
    
    return engine

#------------------------------------------------------------
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Clave de la API de Foursquare
FOURSQUARE_API_KEY = os.getenv("foursquaresapikey")

# Base URL para las solicitudes
FOURSQUARE_BASE_URL = "https://api.foursquare.com/v3/places/search"