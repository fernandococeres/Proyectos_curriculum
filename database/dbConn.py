#dbConn.py
import sqlite3

class dbConn():
    '''dbConn Clase para la conexión con la base de datos.
    '''
    def __init__(self, dbname: str):
        '''__init__ Constructor de la clase.

        Args:
            dbname (str): Nombre de la base de datos.
        '''
        self.dbname = dbname

    def __connect(self):
        '''__connect Establece una conexión con la base de datos.
        '''
        self.connection = sqlite3.connect(self.dbname)

    def __openCursor(self):
        '''__openCursor Abre un cursos a la base de datos para el procesamiento de datos.
        '''
        self.cursor = self.connection.cursor()

    def __closeCursor(self):
        '''__closeCursor Cierra el cursor de la base de datos.
        '''
        self.cursor.close()

    def createTable(self, tableName: str, fieldsDescripcion: str):
        '''createTable Crea la tabla especificada en tableName en la base de datos.

        Args:
            tableName (str): Nombre de la tabla a crear.
            fields (str): Nombre y especificaciones de los campos de la tabla.
        '''
        command = 'CREATE TABLE IF NOT EXISTS' + ' ' + tableName + ' ' + fieldsDescripcion
        #Abre la conexión con la base de datos.
        self.__connect()
        #Ejecuta el comando en la base de datos.
        self.connection.execute(command)
        #Confirma los cambios.
        self.connection.commit()
        #Cierra la conexión con la base de datos.
        self.connection.close()

    def execute(self, command: str, fields: tuple=()) -> list:
        '''execute Ejecuta un comando en la base de datos.

        Args:
            command (str): Comando a ejecutar en la base de datos.
            fields (tuple, optional): detalle de campos y valores de la tabla. Defaults to ().

        Returns:
            list: Devuelve un conjunto de valores de la base de datos.
        '''
        #Abre la conexión con la base de datos.
        self.__connect()
        #Abre un cursor a la base de datos.
        self.__openCursor()
        #Si se pasan campos para el comando, los ejecuta.
        if fields:
            self.cursor.execute(command, fields)
        else:
            self.cursor.execute(command)
        #Aplica los cambios en el cursor y devuelve un lista.
        result = self.cursor.fetchall()
        #Confirma los cambios.
        self.connection.commit()
        #Cierra el cursor.
        self.__closeCursor()
        #Cierra la conexión con la base de datos.
        self.connection.close()

        return result
