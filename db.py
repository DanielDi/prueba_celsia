import sqlite3
import pandas as pd

# Creación de tablas
def create_database():
    """Crea la base de datos y la tabla si no existen."""
    conn = sqlite3.connect('incidencias.db')
    cursor = conn.cursor()

    # Crear tabla si no existe
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS incidencias_duracion (
        NRO_INCIDENTE TEXT,
        F_INICIO_INTERRUPCION TEXT,
        F_REPOSICION_SERVICIO TEXT,
        COD_TRAFO TEXT,
        CANT_CLIENTES INTEGER,
        COD_CIRCUITO TEXT,
        duracion_horas REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS llamadas (
        NRO_CUENTA TEXT,
        FECHA_VALIDACION TEXT,
        NODO TEXT,
        COD_TRAFO TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_data(incidencias_df, llamadas_df):
    conn = sqlite3.connect('incidencias.db')
    
    incidencias_df.to_sql('incidencias_duracion', conn, if_exists='replace', index=False)
    llamadas_df.to_sql('llamadas', conn, if_exists='replace', index=False)
    
    conn.close()    

def crear_informe():
    conn = sqlite3.connect('incidencias.db')

    query = '''
    WITH llamadas_por_trafo AS (
        SELECT
            i.NRO_INCIDENTE,
            i.COD_TRAFO,
            i.COD_CIRCUITO,
            i.F_INICIO_INTERRUPCION,
            i.F_REPOSICION_SERVICIO,
            i.duracion_horas,
            i.CANT_CLIENTES AS total_clientes_afectados,
            COUNT(l.NRO_CUENTA) AS cant_llamadas,
            COUNT(DISTINCT l.NRO_CUENTA) AS cant_clientes_uniq_llamadas,
            MIN(l.FECHA_VALIDACION) AS f_prim_llamada,
            MAX(l.FECHA_VALIDACION) AS f_ult_llamada,
            (julianday(MAX(l.FECHA_VALIDACION)) - julianday(MIN(l.FECHA_VALIDACION))) * 24 AS duracion_llamada_horas
        FROM incidencias_duracion i
        LEFT JOIN llamadas l
        ON i.COD_TRAFO = l.COD_TRAFO
        WHERE l.FECHA_VALIDACION BETWEEN i.F_INICIO_INTERRUPCION AND i.F_REPOSICION_SERVICIO
        GROUP BY i.NRO_INCIDENTE, i.COD_TRAFO, i.COD_CIRCUITO
        HAVING COUNT(l.NRO_CUENTA) > 0
    ),
    trafos_totales AS (
        SELECT 
            NRO_INCIDENTE,
            COUNT(DISTINCT COD_TRAFO) AS cant_trafo_unico_afect
        FROM incidencias_duracion
        GROUP BY NRO_INCIDENTE
    ),
    trafos_llamadas AS (
        SELECT 
            NRO_INCIDENTE,
            COUNT(DISTINCT COD_TRAFO) AS cant_trafo_unico_llamada
        FROM llamadas_por_trafo
        GROUP BY NRO_INCIDENTE
    )
    SELECT
        lpt.NRO_INCIDENTE,
        lpt.COD_TRAFO,
        lpt.COD_CIRCUITO,
        lpt.F_INICIO_INTERRUPCION,
        lpt.F_REPOSICION_SERVICIO,
        lpt.duracion_horas,
        lpt.total_clientes_afectados,
        lpt.cant_llamadas,
        lpt.cant_clientes_uniq_llamadas,
        lpt.f_prim_llamada,
        lpt.f_ult_llamada,
        lpt.duracion_llamada_horas,
        tt.cant_trafo_unico_afect,
        tl.cant_trafo_unico_llamada,
        (tl.cant_trafo_unico_llamada * 100.0 / tt.cant_trafo_unico_afect) AS porcent_llamada
    FROM llamadas_por_trafo lpt
    JOIN trafos_totales tt ON lpt.NRO_INCIDENTE = tt.NRO_INCIDENTE
    JOIN trafos_llamadas tl ON lpt.NRO_INCIDENTE = tl.NRO_INCIDENTE
    ORDER BY lpt.NRO_INCIDENTE, lpt.COD_TRAFO;
    '''

    df = pd.read_sql_query(query, conn)

    conn.close()    

    df.to_excel('data/resultado_final.xlsx', index=False)

    return df