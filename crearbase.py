import sqlite3

# Crear una conexión a la base de datos
conexion = sqlite3.connect('codigopython.db')

# Crear un cursor para ejecutar comandos SQL
cursor = conexion.cursor()

# Crear la tabla "codigo"
cursor.execute('''CREATE TABLE codigo (
                    idcodigo INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT,
                    scriptcodigo TEXT
                )''')

# Guardar los cambios y cerrar la conexión
conexion.commit()
conexion.close()