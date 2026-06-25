

def limpiar_tilde(texto):
    # 1. Normaliza el texto a la forma NFD (Descomposición)
    # Esto separa la 'á' en 'a' + 'tilde combinable'
    texto_normalizado = unicodedata.normalize('NFD', texto)
    
    # 2. Filtra y mantiene solo los caracteres que no sean "marcas" de acento (Mn)
    texto_sin_acentos = "".join(
        c for c in texto_normalizado if unicodedata.category(c) != 'Mn'
    )
   
    return texto_sin_acentos

def normalizar_encabezados(df)
  # 1_estandariza a minusculas
  # 2_elimina espacios en blanco
  # 3_reemplaza vacíos por '_'
  # 4_aplica función definida para limpiar tildes
  
  df.columns = df.columns.str.lower().str.strip().str.replace(' ','_')
  df.columns = [transformacion.limpiar_tilde(col) for col in df.columns]
  return df

def seleccionar_columnas(df)
  # seleccion de columnas relevantes a importar a la Base de Datos
  
  lista_columnas_seleccionadas = [ 'periodo', 'asesor', 'fecha_operacion','contrato','comision', 'valor_neto', 'porcentaje_comision','forma_pago', 'numero_recibo', 'hoja_origen'  ]
  df = df[lista_columnas_seleccionadas]
  return df
