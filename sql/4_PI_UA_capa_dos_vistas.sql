/* CREA VISTAS PARA BD: cobranzas_capa_dos
   El propósito es aislar los datos para consumo de la base principal donde se produce ingesta y transformaciones.
   Las vistas se crean en base a la lógica del negocio, conservando solo los campos relevantes para su análisis,
   y agrupando algunas tabla de dimensiones para representar un modelo estrella más simplificado.
   Se utiliza el condicional WHEN dar más claridad a ciertos valores de registros.	
*/

/* Vista fact_cobranzas 
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_fact_cobranzas;
CREATE VIEW cobranzas_capa_dos.vista_fact_cobranzas AS
	SELECT 
		id_cobro,
		asesor,
        contrato,
        comision,
        valor_neto,
        porcentaje_comision AS porc_liquidado_comision,
        fecha_operacion AS fecha_cobro,
        CASE WHEN forma_pago = 'efe' THEN 'efectivo'
			 WHEN forma_pago = 'transf' THEN 'transferencia'
             WHEN forma_pago = 'tc' THEN 'tarjeta de credito'
             ELSE 'no disponible'
		END AS medio_de_pago,
		CASE WHEN hoja_origen LIKE 'B%' THEN 'broker'
			 WHEN hoja_origen LIKE 'AI%' THEN 'asesores interno'
			 ELSE 'no identificado'
		END AS comision_de
	FROM cobranzas_capa_uno.fact_cobranzas;

/* Vista dim_contratos
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_contratos ;
CREATE VIEW cobranzas_capa_dos.vista_dim_contratos AS
SELECT 
	dc.id_contrato,
	de.especialidad,
	de.rama,
    dcl.nombre_cliente ,
    dci.nombre_ciudad AS 'ciudad_cliente',
    dp.nombre_provincia AS 'provincia_cliente',
	de.com_broker AS 'comision_broker',
	de.com_asesor AS 'comision_asesor'
FROM cobranzas_capa_uno.dim_contratos dc
LEFT JOIN cobranzas_capa_uno.dim_especialidad de ON dc.id_especialidad = de.id_especialidad
LEFT JOIN cobranzas_capa_uno.dim_clientes dcl ON dc.id_cliente = dcl.id_cliente
LEFT JOIN cobranzas_capa_uno.dim_ciudad dci ON dcl.id_ciudad = dci.id_ciudad
LEFT JOIN cobranzas_capa_uno.dim_provincia dp ON dci.id_provincia = dp.id_provincia;

/* Vista dim_comercial
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_comercial ;
CREATE VIEW cobranzas_capa_dos.vista_dim_comercial AS
	SELECT 
		dco.id_comercial,
		dco.nombre_comercial,
		dco.tipo_comercial,
        dci.nombre_ciudad AS 'ciudad_asesor',
        dp.nombre_provincia AS 'provincia_asesor'
 	FROM cobranzas_capa_uno.dim_comercial dco
    LEFT JOIN cobranzas_capa_uno.dim_ciudad dci ON dco.id_ciudad = dci.id_ciudad
    LEFT JOIN cobranzas_capa_uno.dim_provincia dp ON dci.id_provincia = dp.id_provincia;

/* Vista dim_calendario
*/
DROP VIEW IF EXISTS cobranzas_capa_dos.vista_dim_calendario;
CREATE VIEW cobranzas_capa_dos.vista_dim_calendario AS
	select
		fecha,
        anio,
        mes as num_mes,
        elt(mes,'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre') AS nombre_mes,
        LEFT(elt(mes,'Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'), 3) AS mes_corto,
        dia_semana as num_dia,
        elt(dia_semana,'Lunes','Martes','Miércoles','Jueves','Viernes','Sabado','Domingo') AS nombre_dia,
        trimestre as num_trimestre,
        mes_id        
    from cobranzas_capa_uno.dim_calendario;
