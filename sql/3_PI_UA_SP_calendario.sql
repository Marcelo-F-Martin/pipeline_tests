/* IMPORTANTE
    Este script esta diseñado para ejecutar con cliente desde python. Saltea el workbench y pega directo al motor de la BD.
    Si va a ejecutar el script desde MySQL Workbench, se debe descomentar los comentarios 1-, 2- y 3-   
*/

DROP PROCEDURE IF EXISTS cobranzas_capa_uno.llenar_calendario;
-- 1- DELIMITER //
CREATE PROCEDURE cobranzas_capa_uno.llenar_calendario(IN fecha_inicio DATE, IN fecha_fin DATE)
BEGIN
    DECLARE fecha_actual DATE;
    SET fecha_actual = fecha_inicio;
    
    WHILE fecha_actual <= fecha_fin DO
        INSERT INTO cobranzas_capa_uno.dim_calendario (
            fecha, anio, mes, nombre_mes, mes_corto, dia, 
            dia_semana, nombre_dia, trimestre, es_fin_de_semana, mes_id
        ) VALUES (
            fecha_actual,
            YEAR(fecha_actual),
            MONTH(fecha_actual),
            MONTHNAME(fecha_actual),
            LEFT(MONTHNAME(fecha_actual), 3),
            DAY(fecha_actual),
            WEEKDAY(fecha_actual) + 1,
            DAYNAME(fecha_actual),
            QUARTER(fecha_actual),
            IF(WEEKDAY(fecha_actual) IN (5, 6), 1, 0),
            (YEAR(fecha_actual) * 100) + MONTH(fecha_actual)
        );
        SET fecha_actual = DATE_ADD(fecha_actual, INTERVAL 1 DAY);
    END WHILE;
-- 2- Para esta linea reemplace END; ; END//
END;

-- 3- DELIMITER ;

CALL cobranzas_capa_uno.llenar_calendario('2025-01-01', '2025-12-31');
