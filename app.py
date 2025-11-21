import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from matplotlib.cm import get_cmap

import streamlit as st
import pandas as pd
import plotly.express as px

# --- Chargement des données ---
df = pd.read_csv('air_qualité.csv', sep=';')
df.columns = df.columns.str.strip()

# --- Création de la date complète ---
df['date'] = pd.to_datetime(df[['day', 'month', 'year']])

# --- Configuration page ---
st.set_page_config(
    page_title="Analyse Qualité de l'air 2025 - Saint-Germain-des-Prés",
    layout="wide"
)
st.title("Analyse de la qualité de l'air en 2025")
st.subheader("Étude des particules fines PM10 et facteurs associés")
# --- Titre principal et introduction ---
st.write("""
Cette analyse porte sur la qualité de l’air en 2025 dans la station située à la gare **Saint-Germain-des-Prés**, à Paris.  
La base de données contient des mesures quotidiennes comprenant :  

- **PM10 :** particules fines de diamètre inférieur ou égal à 10 µm, exprimées en µg/m³. Ces particules peuvent pénétrer profondément dans les poumons et affecter la santé respiratoire.  
- **TEMP :** température en degrés Celsius, qui peut influencer la dispersion des polluants dans l’air.  
- **HUMI :** humidité relative en pourcentage, un facteur pouvant moduler la concentration de particules fines.  
- **day, month, year :** informations permettant de situer chaque mesure dans le temps.  

Cette base permet d’examiner les variations quotidiennes de la pollution et d’étudier les relations entre PM10, température et humidité sur l’ensemble de l’année 2025.  
Les données sont représentées sous forme de séries temporelles, indicateurs statistiques, matrices de corrélation et tableaux filtrés pour faciliter l’analyse et la compréhension.
""")


# --- Onglets ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Série temporelle",
    "KPI",
    "Matrice de corrélation",
    "Tableau filtré"
])

# ----------------------
# Onglet 1 :  + Série temporelle
# ----------------------
with tab1:
    # Série temporelle PM10
    st.subheader("Évolution quotidienne de PM10")
    fig_line = px.line(
        df,
        x='date',
        y='PM10',
        title="Évolution quotidienne de PM10 (pollution de l’air) durant l'année 2025",
        markers=True
    )
    fig_line.update_layout(
        xaxis_title="Date",
        yaxis_title="PM10 (µg/m³)",
        title_font_size=20,
        font=dict(size=14)
    )
    st.plotly_chart(fig_line, use_container_width=True)
    
    st.write("""
    Cette série temporelle montre l’évolution quotidienne des particules fines PM10 tout au long de l'année 2025.  
    On observe globalement des variations régulières, mais un pic notable apparaît le 5 août, correspondant à une journée où la concentration de PM10 est particulièrement élevée.  
    Cette visualisation permet de suivre la pollution de l’air au fil du temps et d’identifier rapidement les journées avec des niveaux de particules fines plus élevés.
    """)
# ----------------------
# Onglet 2 : KPI / indicateurs
# ----------------------
with tab2:
    st.header("Indicateurs clés (KPI) interactifs")

    # Choix de la variable
    variable = st.selectbox(
        "Choisissez la variable à analyser :",
        ["PM10", "TEMP", "HUMI"]
    )

    # Définition des unités
    units = {
        "PM10": "µg/m³",
        "TEMP": "°C",
        "HUMI": "%"
    }

    # Calcul des indicateurs
    mean_val = df[variable].mean()
    median_val = df[variable].median()
    min_val = df[variable].min()
    max_val = df[variable].max()

    # Affichage des KPI
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(f"Moyenne ({units[variable]})", f"{mean_val:.1f}")
    col2.metric(f"Médiane ({units[variable]})", f"{median_val:.1f}")
    col3.metric(f"Min ({units[variable]})", f"{min_val:.1f}")
    col4.metric(f"Max ({units[variable]})", f"{max_val:.1f}")

    st.write(f"Distribution de {variable} ({units[variable]}) :")
    # Boxplot avec Plotly
    fig_box = px.box(
        df,
        y=variable,
        points="all",  # montre tous les points
        title=f"Boxplot de {variable}"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# ----------------------
# Onglet 3 : Matrice de corrélation
# ----------------------
with tab3:
    st.header("Matrice de corrélation")
    corr = df[['PM10','TEMP','HUMI']].corr()

    fig_corr = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title='Matrice de corrélation entre PM10, Température et Humidité'
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.write("""
    Cette matrice montre les corrélations entre PM10, température et humidité.  
    - Une valeur proche de 1 indique une forte corrélation positive, proche de -1 une corrélation négative.  
    - **Observation :** une forte corrélation positive entre la température et PM10 suggère que les journées plus chaudes tendent à être associées à une pollution plus élevée.  
    - L’humidité a une influence moins marquée sur PM10.
    """)

# ----------------------
# Onglet 4 : Tableau filtré
# ----------------------
with tab4:
    st.header("Tableau de données filtrées")

    # Filtrer par date
    start_date = st.date_input("Date de début", df['date'].min())
    end_date = st.date_input("Date de fin", df['date'].max())

    # Filtrage du dataframe
    df_filtered = df[(df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))]

    st.write(f"Affichage des données du {start_date} au {end_date} :")
    st.dataframe(df_filtered)

