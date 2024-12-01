--Query para Hospitales
SELECT d.codigo_distrito AS codigo_distrito, d.nombre_corregido AS distrito, COUNT(cs.id) AS total_hospitales
FROM distritos d
LEFT JOIN centros_sanitarios cs
ON d.codigo_distrito = cs.coddistrit
GROUP BY d.nombre_corregido,d.codigo_distrito
ORDER BY d.nombre_corregido;

--Query para Escuelas
SELECT d.cod_dist AS codigo_distrito, d.nombre AS nombre_distrito, COUNT(c.id) AS total_centros_educativos
FROM distritos_cp d
LEFT JOIN centros_educativos c
ON d.codigo_postal = c.codpos
GROUP BY d.cod_dist, d.nombre
ORDER BY d.nombre;

--Query para Transporte
SELECT d.codigo_distrito AS codigo_distrito, d.nombre_corregido AS distrito, COUNT(tp.id) AS total_transporte
FROM distritos d
LEFT JOIN transporte_publico tp
ON d.codigo_distrito = tp.coddistrit
GROUP BY d.nombre_corregido,d.codigo_distrito
ORDER BY d.nombre_corregido;

--Query para Alquiler
SELECT coddistrit AS codigo_distrito, distrito AS nombre_distrito, ROUND(CAST(AVG(precio_2022_euros_m2) AS NUMERIC), 2) AS precio_medio_2022_m2
FROM precios_alquiler
GROUP BY coddistrit, distrito
ORDER BY distrito;
--Query para Compra
SELECT coddistrit AS codigo_distrito, distrito AS nombre_distrito, ROUND(CAST(AVG(precio_2022_euros_m2) AS NUMERIC), 2) AS precio_medio_2022_m2
FROM precios_compra
GROUP BY coddistrit, distrito
ORDER BY distrito;

--Query para Ocio
SELECT barrio AS distrito, numero_ocio
FROM zonas_de_ocio
ORDER BY distrito;

--Query para Zonas Verdes
SELECT barrio AS distrito, numero_parques AS zonas_verdes
FROM zonas_verdes
ORDER BY distrito;
