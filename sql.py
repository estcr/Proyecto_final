from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Cargar las variables de entorno
load_dotenv(dotenv_path='.env')

# Obtener la contraseña desde las variables de entorno
db_pass = os.getenv("db_pass")

# Verificar si la contraseña se carga correctamente
if db_pass is None:
    raise ValueError("No se ha encontrado la variable de entorno 'db_pass'")

# Configuración de la base de datos
bd = "travel_planner"  # Nombre de tu base de datos
connection_string = f'mysql+pymysql://root:{db_pass}@localhost/{bd}'

# Crear el engine de conexión
engine = create_engine(connection_string)

# Probar la conexión
try:
    with engine.connect() as connection:
        print("Conexión exitosa")
except Exception as e:
    print(f"Error en la conexión: {e}")