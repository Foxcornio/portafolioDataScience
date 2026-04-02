# Creamos una clase que almacenara funciones de transformación necesarias para nuestros datos
import pandas as pd
class Transform:
    def parse_financial(value):
        '''
        Transforma los datos str(texto) a int(enteros)

        Args:
            value (object): Recibimos la columna de datos a convertir
        
        Returns:
            int : Los datos formateados en enteros
        '''
        # En caso de que el valor sea nulo se dejara tal cual
        if pd.isna(value): 
            return pd.NA
        
        # Limpieza del texto
        # Remplazamos de la cadena los simbolos $ y , por un espacio
        # Con strip() eliminamos los espacios de los costados
        # con upper() formateamos si existen las letras a mayusculas
        val_str= str(value).replace('$','').replace(',','').strip().upper()
        multiplier = 1

        # Checamos si existen sufijos
        if val_str.endswith('M'): # Primero M de millions
            multiplier = 1_000_000 # Cantidad por la que multiplicaremos
            val_str = val_str[:-1] # Quitamos el ultimo caracter
        elif val_str.endswith('B'):
            multiplier = 1_000_000_000 # Cantidad por la que multiplicaremos
            val_str = val_str[:-1] # Quitamos el ultimo caracter

        try:
        # Usamos float temporalmente por si hay decimales (ej. 1.5 * 1000000)
            return int(float(val_str) * multiplier)
        except ValueError:
            return pd.NA # En caso de que el valor sea un texto irreconocible
