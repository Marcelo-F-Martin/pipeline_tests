import pandas as pd
import os
import requests
from sqlalchemy import create_engine, text
import pymysql
from pymysql.constants import CLIENT
from dotenv import load_dotenv

def guardar_archivo(df):
    # Función para exportar archivo en formato .CSV al directorio local.
    try:
        ingreso_ruta = input('Copie y pegue el directorio donde guardar el archivo .CSV: ')
        ruta_archivo = f"{ingreso_ruta}"
        nombre_csv_salida = "comisiones_consolidadas.csv"
        ruta_salida_completa = os.path.join(ruta_archivo, nombre_csv_salida)
        df.to_csv(ruta_salida_completa, index=False, encoding='utf-8')
        mensaje = print('✅ ¡Archivo guardado exitosamente!')

    except Exception as e:
            mensaje = print('⚠️ No se pudo guardar el archivo por el siguiente error:')
            print(type(e))    
    
    return mensaje

def recuperar_script_sql():
    #url_sql_ddl = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/1_PI_UA_DDL.sql'
    #url_sql_inserts = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/2_PI_UA_inserts.sql'
    #url_sql_vistas = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/4_PI_UA_capa_dos_vistas.sql'
    #url_sql_sp = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL/3_PI_UA_SP_calendario.sql'

    ruta_repo_scriptSQL = 'https://raw.githubusercontent.com/Marcelo-F-Martin/PI_UA_pipeline_analisis_de_cobranza/refs/heads/main/SQL'

    url_sql_ddl = f"{ruta_repo_scriptSQL}/1_PI_UA_DDL.sql"
    url_sql_inserts = f"{ruta_repo_scriptSQL}/2_PI_UA_inserts.sql"
    url_sql_vistas = f"{ruta_repo_scriptSQL}/4_PI_UA_capa_dos_vistas.sql"
    url_sql_sp = f"{ruta_repo_scriptSQL}/3_PI_UA_SP_calendario.sql"
    
    respuesta_1 = requests.get(url_sql_ddl)
    respuesta_2 = requests.get(url_sql_sp)  
    respuesta_3 = requests.get(url_sql_inserts)    
    respuesta_4 = requests.get(url_sql_vistas)

    if respuesta_1.status_code == 200 and respuesta_2.status_code == 200 and respuesta_3.status_code == 200 and respuesta_4.status_code == 200:
     
        script_sql_1 = respuesta_1.text
        script_sql_2 = respuesta_2.text
        script_sql_3 = respuesta_3.text
        script_sql_4 = respuesta_4.text

        return script_sql_1, script_sql_2, script_sql_3, script_sql_4
        
    else:
        return print(f'✖️ Error al acceder al archivo Nº 1: Estado {respuesta_1.status_code}'),
        print(f'✖️ Error al acceder al archivo Nº 2: Estado {respuesta_2.status_code}'),
        print(f'✖️ Error al acceder al archivo Nº 3: Estado {respuesta_3.status_code}'),
        print(f'✖️ Error al acceder al archivo Nº 4: Estado {respuesta_4.status_code}')

def ejecutar_script_sql(df):
    
    load_dotenv()
    
    usuario = os.getenv("BD_USER")
    host = os.getenv("BD_HOST")
    puerto = os.getenv("BD_PORT")
    clave = os.getenv("BD_PASS")
    bd_capa_uno = os.getenv("BD_CAPA_UNO")
    bd_capa_dos = os.getenv("BD_CAPA_DOS")
    tabla_temp = os.getenv("TABLA_TEMP_CAPA_UNO")
    
    
    script_sql_1, script_sql_2, script_sql_3, script_sql_4 = recuperar_script_sql()

    # se crean motores para diferentes acciones 
    engine_create = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}") # crea nuevas BD.
    engine_insert = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}/{bd_capa_uno}") # inserta datos en tabla temp_cobranzas.
    engine_vista = create_engine(f"mysql+pymysql://{usuario}:{clave}@{host}:{puerto}/{bd_capa_dos}") # crea vistas

    #------------------------------------------
    # Inicia proceso de ingesta de datos
    #------------------------------------------
    try:
        print('---------------------------------------------------------------')
        print('⏳Inicio de ingesta en base de datos...\n')

        #__________________________________________________
        # 1.DDL crea base de datos y tablas
        #__________________________________________________
        with engine_create.begin() as connection:

            for statement in script_sql_1.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 1 de 5 ...')
        print(f"✅ Estructuras creadas para las bases de datos:\n - '{bd_capa_uno}'\n - '{bd_capa_dos}'\n")

        #__________________________________________________
        # 2.Crea Stored Procedure en BD cobranzas_capa_uno
        #__________________________________________________
        conn = pymysql.connect(
                                host=host,
                                user=usuario,
                                password=clave,
                                db=bd_capa_uno,
                                port=int(puerto),
                                client_flag=CLIENT.MULTI_STATEMENTS
                               )     

        with conn.cursor() as cursor:
             cursor.execute(script_sql_2)
        
        conn.commit()
        conn.close()
        
        print('⏳...script 2 de 5 ...')
        print(f"✅ Stored Procedure 'llenar_calendario' creado en BD '{bd_capa_uno}'\n")        


        #__________________________________________________
        # 3.Ingesta el dataframe en tabla temporal (truncate + insert)
        #__________________________________________________
        with engine_insert.begin() as connection:
            connection.execute(text(f"TRUNCATE TABLE {tabla_temp}"))
            
            df.to_sql(
                        name=tabla_temp,
                        con=connection,
                        if_exists='append', 
                        index=False,
                        chunksize=1000, 
                        method='multi' # Para que sea masivo y no registro por registro
                      )
        print('⏳...script 3 de 5 ...')   
        print(f"✅ Datos ingestados en tabla '{tabla_temp}' de BD '{bd_capa_uno}':\n - {len(df)} registros insertados\n")

        #__________________________________________________
        # 4.Pasa datos de tabla_temp a tabla_fact
        #__________________________________________________
        with engine_insert.begin() as connection:
 
            for statement in script_sql_3.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 4 de 5 ...')
        print(f"✅ Datos transferidos en BD '{bd_capa_uno}':  '{tabla_temp}' => 'fact_cobranzas'\n")

        #__________________________________________________
        # 5.Crea vistas en BD cobranzas_capa_dos
        #__________________________________________________
        with engine_vista.begin() as connection:
             
            for statement in script_sql_4.split(';'):
                if statement.strip():
                    connection.execute(text(statement))

        print('⏳...script 5 de 5')
        print(f"✅ Vistas creadas en BD '{bd_capa_dos}'\n")


        print('===============================================================')
        print('🎉🎉 Orquestación de ETL finalizada con Éxito!! 🎉🎉')
        print('===============================================================\n')
    
    except Exception as e:
        print(e)
    #------------------------------------------
    # Fin proceso de ingesta de datos

def check_env_y_conn_MySQL():
    # Verifique sus credenciales de acceso a MySQL en el archivo ".env"
    load_dotenv()
    
    usuario = os.getenv("BD_USER")
    host = os.getenv("BD_HOST")
    puerto = os.getenv("BD_PORT")
    clave = os.getenv("BD_PASS")
    bd_capa_uno = os.getenv("BD_CAPA_UNO")
    bd_capa_dos = os.getenv("BD_CAPA_DOS")
    tabla_temp = os.getenv("TABLA_TEMP_CAPA_UNO")
    
    print("======= ⏳...Inicio check de conexión a MySQL... ========")
    try:
        conn = pymysql.connect(
        host=host,
        user=usuario,
        password=clave,
                )
        if conn.open:
            print(" 1) => Conexion Exitosa !!!")
    except pymysql.Error as e:
        print(e)
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()
            print(" 2) => Se cierra conexión")
            print("================== Fin check de conexión =================")

def ini_pbi():
    # Inicializa aplicación Power BI.

    nombre_arch_pbi = "PI_UA_analisis_cobranzas.pbit"
    
    if os.path.exists(nombre_arch_pbi):
        print("===============================================")
        print(" Archivo para Visualizar los datos detectado.")
        print("   ⏳... Espere un instante mientras inicia Power BI...")
        print("===============================================")
        os.startfile(nombre_arch_pbi)
    else:
        print("===============================================")
        print(f"✖️ Archivo '{nombre_arch_pbi}' NO detectado en el directorio actual.")
        print("===============================================")
