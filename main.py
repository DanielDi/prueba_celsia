import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import db

def load_data():
    """Carga los datos desde CSV y calcula la duración en horas de las incidencias."""
    # Cargar los datos desde un archivo CSV (ajusta el nombre del archivo según sea necesario)
    llamadas_df = pd.read_excel('data/llamadas_adms.xlsx')
    incidencias_df = pd.read_excel('data/incidencias_adms.xlsx')

    # Convertir las fechas a datetime y calcular la duración en horas
    incidencias_df = incidencias_df.dropna(subset=['NRO_INCIDENTE'])
    incidencias_df['F_INICIO_INTERRUPCION'] = pd.to_datetime(incidencias_df['F_INICIO_INTERRUPCION'])
    incidencias_df['F_REPOSICION_SERVICIO'] = pd.to_datetime(incidencias_df['F_REPOSICION_SERVICIO'])
    
    # Calcular la duración en horas
    incidencias_df['duracion_horas'] = (incidencias_df['F_REPOSICION_SERVICIO']
                                        - incidencias_df['F_INICIO_INTERRUPCION']).dt.total_seconds() / 3600
    
    # Eliminar filas con NRO_INCIDENTE vacío
    incidencias_df = incidencias_df[incidencias_df['NRO_INCIDENTE'].notna()]

    return incidencias_df, llamadas_df

def agrupar_metricas(df):
    circuito_metricas = df.groupby('COD_CIRCUITO').agg(
        mean_duracion_llamada_horas=('duracion_llamada_horas', 'mean'),
        mean_porcent_llamada=('porcent_llamada', 'mean')
    ).reset_index()

    return circuito_metricas

def generar_cluster(df):
    # Estandarizar las variables
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[['mean_duracion_llamada_horas', 'mean_porcent_llamada']])

    # Método del codo para determinar el número óptimo de clusters
    inertia = []  # Para guardar la inercia
    K = range(1, 10)  # Probar de 1 a 10 clusters
    for k in K:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertia.append(kmeans.inertia_)

    # Graficar el método del codo
    plt.figure(figsize=(8, 6))
    plt.plot(K, inertia, 'bx-')
    plt.xlabel('Número de clusters (k)')
    plt.ylabel('Inercia')
    plt.title('Método del codo para determinar el número óptimo de clusters')
    plt.show()

    # Aplicar K-means con el número óptimo de clusters
    kmeans_optimo = KMeans(n_clusters=3, random_state=42)
    df['cluster'] = kmeans_optimo.fit_predict(X_scaled)

    # Visualizar los resultados usando seaborn
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='mean_duracion_llamada_horas', y='mean_porcent_llamada', hue='cluster', data=df, palette='viridis', s=100)
    plt.title('Clusters de Circuitos Basados en Duración de Llamadas y Porcentaje de Llamadas')
    plt.xlabel('Media de Duración de Llamadas (horas)')
    plt.ylabel('Promedio de Porcentaje de Clientes que Llamaron')
    plt.show()

# Bloque principal
if __name__ == "__main__":
    db.create_database()  # Crear la base de datos y la tabla
    incidencias_df, llamadas_df = load_data()  # Cargar y procesar datos
    db.insert_data(incidencias_df, llamadas_df)  # Insertar datos en la base de datos
    informe_df = db.crear_informe() #Crear y generar informe en excel

    metricas_df = agrupar_metricas(informe_df)

    generar_cluster(metricas_df)