def genera_unico_DF(lista_df):
  import requests
  
  df_definitivo_por_libro = []   
  total_registros = 0
  
  #====== INICIO bucle externo: recorre archivos dentro del directorio ===============================
  for archivo in lista_df:
      
      # Filtrado para leer solo archivos .xls
      if archivo['name'].endswith('.xls'):
          print(f"Nombre de archivo encontrado: {archivo['name']}")
          print('----------------------------------------------------------------------')
          
      # lista para incorporar los df por cada hoja de cada libro.
      hojas_consolidadas_por_libro = [] 
      
      url_archivo = archivo['browser_download_url']
      respuesta_url_archivo = requests.get(url_archivo).content
      archivo = pd.read_excel(io.BytesIO(respuesta_url_archivo), engine='xlrd', sheet_name=None, header=None)
  
      #====== INICIO bucle interno: recorre hojas del archivo =======================================
      
          # se considera "df_crudo" a cada hoja sin procesar de un libro ".xls"
      for nombre_hoja, df_crudo in archivo.items():
          print(f" ✅ Hoja '{nombre_hoja}' leída correctamente.")
          
          #--------- Fragmento para obtener el df_limpio de cada hoja --------
          encabezado_clave = "Periodo"
          
          indice_encabezado_fila = df_crudo[df_crudo.apply(lambda row: encabezado_clave in row.astype(str).values, axis=1)].index
  
          if not indice_encabezado_fila.start == 0:
          
              fila_inicio = indice_encabezado_fila[0]
              
              print(f"  ✅ Encabezado clave '{encabezado_clave}' encontrado en la Fila: {fila_inicio}")
             
              fila_encabezado = df_crudo.iloc[fila_inicio]
              
              col_inicio = fila_encabezado[fila_encabezado.astype(str) == encabezado_clave].index[0]
       
              df_crudo.columns = df_crudo.iloc[fila_inicio] # Asignar la fila encontrada como nuevo encabezado
              
              df_limpio = df_crudo[fila_inicio + 1:].reset_index(drop=True) # Eliminar filas superiores haciendo un slicing del df_crudo
              
              #---------- Fin Fragmento -------------------------------------------
              
              df_final_hoja = df_limpio.copy()
              
              df_final_hoja['hoja_origen'] = nombre_hoja # Columna para identificar a quien corresponde la comisión (si al broker o a los asesores)
  
          else:
              print(f"   ✖️ Encabezado Clave NO encontrado en hoja: {nombre_hoja}. ")
              continue
  
          if not df_final_hoja.empty:
              hojas_consolidadas_por_libro.append(df_final_hoja)
              print(f"   ✅ DataFrame de Hoja '{nombre_hoja}' incorporada al listado. Registros: {len(df_final_hoja)}\n")
              
              total_registros += len(df_final_hoja)
          else:
              print(f"  Advertencia: Hoja '{nombre_hoja}' vacía después de la limpieza. No se añadió.")
              
      if not hojas_consolidadas_por_libro == []:
      
          df_archivo_unificado = pd.concat(hojas_consolidadas_por_libro, ignore_index=True)
          df_definitivo_por_libro.append(df_archivo_unificado)
  
      else:
          print('    ❌ No se consolidaron hojas para este archivo excel. \n')
  
      #====== FIN bucle interno =================================================
  #====== FIN bucle externo ====================================================
  
  # Concatenación final
  if not df_definitivo_por_libro == []:
      df_final = pd.concat(df_definitivo_por_libro, ignore_index=True)
      print('======================================================')
      print(f'📝 Suma de Registros del total de hojas: {total_registros}')
      print(f'📝 Total de Registros del df_final concatenado: {len(df_final)}')
      print('======================================================')
  else:
      print('======================================================')
      print(' ⚠️ No se han generado dataframes para los archivos excel leídos. ')
      print('======================================================')
    
  return df_final
