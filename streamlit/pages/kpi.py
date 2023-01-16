import streamlit as st 
import pandas as pd 
import numpy as np 
from datetime import datetime
import requests
import json
import csv 
import folium 
import os
import seaborn as sns
import matplotlib.pyplot as plt

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://media.istockphoto.com/id/1199334022/fr/photo/vue-floue-de-la-tour-eiffel-%C3%A0-paris-avec-lespace-de-copie.jpg?s=612x612&w=0&k=20&c=kzN1py3FRoYtCaV35dv9uJVitGHK6KWdbUi5gHm5xyE=");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )



st.markdown("<h1 style='text-align: center; color: black;'>Quelques informations sur l'immobilier</h1>",
            unsafe_allow_html=True)
@st.cache(allow_output_mutation=True)
def baseviz():
    df_full_raw = pd.read_csv('df_full_raw.csv.gz', index_col=[0])
    df_full = df_full_raw.copy()

    # calcul du prix au m²

    df_full['prix_m2'] = round(df_full['valeur_fonciere']/df_full['surface_reelle_bati'], 0)

    # ajout d'une colonne année

    df_full['année'] = df_full['date_mutation'].apply(lambda x: x[:4])

    # identification des outliers par commune et par année

    def Q1(array):
        return np.quantile(array,0.25)

    def Q3(array):
        return np.quantile(array,0.75)

    def IQR(array):
        return np.quantile(array,0.75) - np.quantile(array,0.25)

    df_IQR = pd.pivot_table(data = df_full,
                            values = 'prix_m2',
                            index =  ['code_commune', 'année'],
                            aggfunc = {'prix_m2' : [Q1, Q3, IQR]})

    df_full = df_full.merge(df_IQR,
                            how = 'left',
                            on = ['code_commune','année'])

    df_full['outlier'] = (df_full['prix_m2'] < (df_full['Q1'] - 1.5 * df_full['IQR'])) | (df_full['prix_m2'] > (df_full['Q3'] + 1.5 * df_full['IQR']))

    df_full_clean = df_full[~df_full['outlier']]

    # df_full_clean = pd.read_csv('df_full_clean_2.csv', index_col=0)

    df_full_clean['date_mutation'] = pd.to_datetime(df_full_clean['date_mutation'], format= '%Y/%m/%d')

    # df_full_clean.loc[(df_full_clean['date_mutation'] >= '2017-01-01') & (df_full_clean['date_mutation'] <= '2017-12-31')]

    # La quantité de vente par mois entre 2018 et 2021

    df_full_clean['month'] = df_full_clean['date_mutation'].dt.month
    df_viz_17 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2017-01-01') & (df_full_clean['date_mutation'] <= '2017-12-31')]
    df_viz_18 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2018-01-01') & (df_full_clean['date_mutation'] <= '2018-12-31')]
    df_viz_19 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2019-01-01') & (df_full_clean['date_mutation'] <= '2019-12-31')]
    df_viz_20 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2020-01-01') & (df_full_clean['date_mutation'] <= '2020-12-31')]
    df_viz_21 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2021-01-01') & (df_full_clean['date_mutation'] <= '2021-12-31')]
    df_viz_22 = df_full_clean.loc[(df_full_clean['date_mutation'] >= '2022-01-01') & (df_full_clean['date_mutation'] <= '2022-12-31')]

    return df_full_clean, df_viz_17, df_viz_18, df_viz_19, df_viz_20, df_viz_21, df_viz_22

df_full_clean, df_viz_17, df_viz_18, df_viz_19, df_viz_20, df_viz_21, df_viz_22 = baseviz()
### STREAMLIT

sns.set_theme(context='notebook', palette='pastel', font='sans-serif', font_scale=1, color_codes=True, rc=None)
sns.set_style("whitegrid", {'axes.grid' : False},)

intro = st.container()
volume_ventes = st.container()
evolution_prix = st.container()
type_bien = st.container()

# Volume de mutation entre 2018 et 2021

with volume_ventes:
    st.header('Evolution du volume de ventes')
    left_col1, right_col1 = st.columns(2)

    with left_col1:
        # volume de mutation global par année
        @st.cache(allow_output_mutation=True)
        def globalvol():
            global_volume_viz, ax = plt.subplots()
            global_volume_viz.suptitle('Nombre de ventes par an en Île-de-France')
            ax = sns.countplot(data = df_full_clean[df_full_clean['année'].isin(['2018','2019','2020','2021'])],
                            x = 'année',
                            color='#3964e7')
            return global_volume_viz
        st.pyplot(globalvol())


    with right_col1:
        @st.cache(allow_output_mutation=True)
        def mutation():
            mutations_per_year_dpt = pd.pivot_table(df_full_clean[df_full_clean['année'].isin(['2018','2019','2020','2021'])],
                                                    values = 'nature_mutation',
                                                    index = ['code_departement','année'],
                                                    aggfunc = 'count')

            # volume de mutation par année et par département
            dpt_volume_viz, ax = plt.subplots()
            dpt_volume_viz.suptitle('Nombre de ventes par an et par département')
            ax = sns.lineplot(data = mutations_per_year_dpt,
                            x = 'année',
                            y = 'nature_mutation',
                            hue = 'code_departement',
                            legend = 'full',
                            palette = 'pastel')
            ax.legend().set_title('')
            plt.legend(bbox_to_anchor=(1.05, 1))
            return dpt_volume_viz
        st.pyplot(mutation())

    @st.cache(allow_output_mutation=True)
    def nombrevente():
        fig, axes = plt.subplots(2,2, figsize=(20,11))
        fig.suptitle('Nombre de ventes par mois entre 2018 et 2021')

        sns.countplot(ax=axes[0, 0], x='month', data=df_viz_18 , color='#3964e7')
        sns.countplot(ax=axes[0, 1], x='month', data=df_viz_19 , color='#3964e7')
        sns.countplot(ax=axes[1, 0], x='month', data=df_viz_20 , color='#3964e7')
        sns.countplot(ax=axes[1, 1], x='month', data=df_viz_21 , color='#3964e7')

        # définir les limites de l'axe y
        y_min = 0 
        y_max = 35000

        # Appliquer les limites de l'axe y sur tous les graphiques
        for ax in axes.flat:
            ax.set_ylim(y_min, y_max)

        axes[0,0].set_title('2018')
        axes[0,1].set_title('2019')
        axes[1,0].set_title('2020')
        axes[1,1].set_title('2021')
        return fig

    st.pyplot(nombrevente())


with evolution_prix :
    left_col2, right_col2 = st.columns(2)

    with left_col2 :

        st.header('Evolution des prix au m²')
        @st.cache(allow_output_mutation=True)
        def priceevol():
            price_evol_mean = pd.pivot_table(df_full_clean[df_full_clean['année'].isin(['2018','2019','2020','2021'])],
                                                values = 'prix_m2',
                                                index = ['code_departement','année'],
                                                aggfunc = np.mean)

            evol_prix_dpt, ax = plt.subplots()
            evol_prix_dpt.suptitle('Evolution des prix au m² par année et par département')
            ax = sns.lineplot(data = price_evol_mean,
                    x = 'année',
                    y = 'prix_m2',
                    hue = 'code_departement',
                    legend = 'full',
                    palette='pastel')
            ax.legend().set_title('')
            plt.legend(bbox_to_anchor=(1.2, 1))
            return evol_prix_dpt
        st.pyplot(priceevol())

with type_bien:
    st.header('Répartition des types de bien')
    @st.cache(allow_output_mutation=True)
    def apptmaison():
        appt_maison = df_full_clean[df_full_clean['année'].isin(['2018','2019','2020','2021'])].groupby(['code_departement', 'type_local','année'])['nature_mutation'].count().to_frame().reset_index()

        appt_maison_viz, axes = plt.subplots(2,2, figsize=(20,11))
        appt_maison_viz.suptitle('Répartition des ventes entre appartements et maisons par année et par département')

        sns.barplot(ax=axes[0, 0], data = appt_maison[appt_maison['année']=='2018'], x = 'code_departement', y = 'nature_mutation', hue = 'type_local', palette='pastel')
        sns.barplot(ax=axes[0, 1], data = appt_maison[appt_maison['année']=='2019'], x = 'code_departement', y = 'nature_mutation', hue = 'type_local', palette='pastel')
        sns.barplot(ax=axes[1, 0], data = appt_maison[appt_maison['année']=='2020'], x = 'code_departement', y = 'nature_mutation', hue = 'type_local', palette='pastel')
        sns.barplot(ax=axes[1, 1], data = appt_maison[appt_maison['année']=='2021'], x = 'code_departement', y = 'nature_mutation', hue = 'type_local', palette='pastel')
        # définir les limites de l'axe y
        y_min = 0 
        y_max = 35000

        # Appliquer les limites de l'axe y sur tous les graphiques
        for ax in axes.flat:
            ax.set_ylim(y_min, y_max)

        axes[0,0].set_title('2018')
        axes[0,1].set_title('2019')
        axes[1,0].set_title('2020')
        axes[1,1].set_title('2021')
        return appt_maison_viz
    st.pyplot(apptmaison())