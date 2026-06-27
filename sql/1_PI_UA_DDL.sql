/* 1 - BASE DE DATOS Y DEFINICION DE ESCHEMAS
*/

/* 1.1 - BASE DE DATOS
	Se crean dos capas de Base de datos: Drop + Create 
		Capa Uno: Ingesta de datos en tablas.
        Capa dos: Consulta de capa uno y almacena Vistas para servicio de BI.
*/

DROP DATABASE IF EXISTS cobranzas_capa_uno;
CREATE DATABASE cobranzas_capa_uno;
DROP DATABASE IF EXISTS cobranzas_capa_dos;
CREATE DATABASE cobranzas_capa_dos;


/* 1.2 - TABLAS DE HECHO
	1.2.1 - Crea tabla de hechos para estacionamiento de datos ingestados, previo a la carga en tabla principal fact_cobranzas.
			Esta tabla se sobreescribe con cada ingesta (truncate + insert) desde script python.
    1.2.2 - Crea tabla de hechos principal fact_cobranzas.
*/
DROP TABLE IF EXISTS cobranzas_capa_uno.temp_cobranzas;
CREATE TABLE cobranzas_capa_uno.temp_cobranzas (
	id_cobro int not null auto_increment, -- es PK autoincremental
	periodo varchar(10),
	asesor varchar(10),
	fecha_operacion date,
	contrato varchar(50),
	comision float,
	valor_neto float,
	porcentaje_comision float,
	forma_pago varchar(10),
	numero_recibo varchar(20),
	hoja_origen varchar(20),	
	ultimo_update DATETIME DEFAULT CURRENT_TIMESTAMP, # se incorpora para tracking de registros
	PRIMARY KEY (id_cobro)
); 

DROP TABLE IF EXISTS cobranzas_capa_uno.fact_cobranzas;
CREATE TABLE cobranzas_capa_uno.fact_cobranzas (
	id_cobro int not null auto_increment, -- es PK autoincremental
	periodo varchar(10),
	asesor varchar(10),
	fecha_operacion date,
	contrato varchar(50),
	comision float,
	valor_neto float,
	porcentaje_comision float,
	forma_pago varchar(10),
	numero_recibo varchar(20),
	hoja_origen varchar(20),	
	ultimo_update DATETIME DEFAULT CURRENT_TIMESTAMP, # se incorpora para tracking de registros
	PRIMARY KEY (id_cobro)
);

/* 1.3 - TABLAS DIMENSIONES
	1.3.1 - Crea tabla dimensión calendario. Esta tabla se ingesta con SP "llenar_calendario".
	1.3.2 - Crea tablas que dimensionan fact_cobranzas
*/

DROP TABLE IF EXISTS cobranzas_capa_uno.dim_calendario;
CREATE TABLE cobranzas_capa_uno.dim_calendario (
    fecha DATE PRIMARY KEY,
    anio INT NOT NULL,
    mes INT NOT NULL,
    nombre_mes VARCHAR(15) NOT NULL,
    mes_corto CHAR(3) NOT NULL,
    dia INT NOT NULL,
    dia_semana INT NOT NULL, -- 1 para Lunes, 7 para Domingo
    nombre_dia VARCHAR(15) NOT NULL,
    trimestre INT NOT NULL,
    es_fin_de_semana BOOLEAN NOT NULL,
    mes_id INT NOT NULL -- Ejemplo: 202603
);

DROP TABLE IF EXISTS cobranzas_capa_uno.dim_provincia;
CREATE TABLE cobranzas_capa_uno.dim_provincia (
    id_provincia	VARCHAR(10),
    nombre_provincia	VARCHAR(25),
    PRIMARY KEY (id_provincia)
);

DROP TABLE IF EXISTS cobranzas_capa_uno.dim_ciudad;
CREATE TABLE cobranzas_capa_uno.dim_ciudad (
    id_ciudad	VARCHAR(10),
    nombre_ciudad	VARCHAR(50),
    id_provincia	VARCHAR(10),
    PRIMARY KEY (id_ciudad)
);
  
DROP TABLE IF EXISTS cobranzas_capa_uno.dim_especialidad;
CREATE TABLE cobranzas_capa_uno.dim_especialidad (
    id_especialidad	VARCHAR(10),
    especialidad	VARCHAR(100),
    rama	VARCHAR(100),
    com_broker	float,
    com_asesor	float,
    PRIMARY KEY (id_especialidad)
);
   
DROP TABLE IF EXISTS cobranzas_capa_uno.dim_clientes;
CREATE TABLE cobranzas_capa_uno.dim_clientes (
    Id_cliente	VARCHAR(10),
    nombre_cliente	VARCHAR(512),
    id_ciudad	VARCHAR(10),
    PRIMARY KEY (id_cliente)
);
    
DROP TABLE IF EXISTS cobranzas_capa_uno.dim_comercial;
CREATE TABLE cobranzas_capa_uno.dim_comercial (
    id_comercial	VARCHAR(10),
    nombre_comercial	VARCHAR(512),
    tipo_comercial	VARCHAR(210),
    id_ciudad	VARCHAR(10),
    PRIMARY KEY (id_comercial)
);
    
DROP TABLE IF EXISTS cobranzas_capa_uno.dim_contratos;
CREATE TABLE cobranzas_capa_uno.dim_contratos (
    id_contrato	VARCHAR(10),
    id_cliente	VARCHAR(10),
    id_especialidad	VARCHAR(10),
    PRIMARY KEY (id_contrato)
);

/* FOREIGN KEYS
	Una vez creadas todas las tablas se establecen las claves foraneas relacionadas
*/

ALTER TABLE cobranzas_capa_uno.fact_cobranzas 
	ADD CONSTRAINT fk_fact_asesor
		FOREIGN KEY (asesor) REFERENCES cobranzas_capa_uno.dim_comercial(id_comercial) ON DELETE SET NULL,
	ADD CONSTRAINT fk_fact_fecha
		FOREIGN KEY (fecha_operacion) REFERENCES cobranzas_capa_uno.dim_calendario(fecha) ON DELETE SET NULL,
	ADD CONSTRAINT fk_factcontrato
		FOREIGN KEY (contrato) REFERENCES cobranzas_capa_uno.dim_contratos(id_contrato) ON DELETE SET NULL;

ALTER TABLE cobranzas_capa_uno.dim_ciudad ADD CONSTRAINT fk_dim_ciudad_ciudad
	FOREIGN KEY (id_provincia) REFERENCES cobranzas_capa_uno.dim_provincia(id_provincia) ON DELETE SET NULL;

ALTER TABLE cobranzas_capa_uno.dim_clientes ADD CONSTRAINT fk_dim_clientes_ciudad
	FOREIGN KEY (id_ciudad) REFERENCES cobranzas_capa_uno.dim_ciudad(id_ciudad) ON DELETE SET NULL;

ALTER TABLE cobranzas_capa_uno.dim_comercial ADD CONSTRAINT fk_dim_comercial_ciudad
	FOREIGN KEY (id_ciudad) REFERENCES cobranzas_capa_uno.dim_ciudad(id_ciudad) ON DELETE SET NULL;

ALTER TABLE cobranzas_capa_uno.dim_contratos 
	ADD CONSTRAINT fk_dim_contratos_cliente
		FOREIGN KEY (id_cliente) REFERENCES cobranzas_capa_uno.dim_clientes(id_cliente) ON DELETE SET NULL,
	ADD CONSTRAINT fk_dim_contratos_especialidad
		FOREIGN KEY (id_especialidad) REFERENCES cobranzas_capa_uno.dim_especialidad(id_especialidad) ON DELETE SET NULL;
