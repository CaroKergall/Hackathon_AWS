import streamlit as st 
import pandas as pd 
import numpy as np 
from datetime import datetime
import requests
import json
import csv 
import folium 

from ml import * 

if "visibility" not in st.session_state:
   st.session_state.visibility = "visible"
   st.session_state.disabled = False

st.markdown("<h1 style='text-align: center; color: grey;'>Bienvenue au Hackathon</h1>", unsafe_allow_html=True)

with st.sidebar:
   pass
   st.markdown("<h1 style='text-align: center; color: grey;'>Application des filtres</h1>", unsafe_allow_html=True)
   st.markdown("----------------")

   col1, col2 = st.columns(2)
   st.markdown("----------------") 
   with col1:
    st.checkbox("Disable text input widget", key="disabled")
    st.radio(
        "Set text input label visibility 👉",
        key="visibility",
        options=["visible", "hidden", "collapsed"],
    )
    st.text_input(
        "Placeholder for the other text input widget",
        "This is a placeholder",
        key="placeholder",
    )

   with col2:
    text_input = st.text_input(
        "Enter some text 👇",
        label_visibility=st.session_state.visibility,
        disabled=st.session_state.disabled,
        placeholder=st.session_state.placeholder,
    )

    if text_input:
        st.write("You entered: ", text_input)   
     
tab1, tab2, tab3 ,tab4 = st.tabs(["Map", "KPI", "Outliers","Predictions"])

with tab1:
   st.header("Map")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("KPI")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("Outliers")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

with tab4:

   st.header("Prévoyez le prix de votre bien")
   
   st.image("https://upload.wikimedia.org/wikipedia/commons/7/75/Maison_Adam_de_Villiers.jpg", width=200)
   
   dico = {"Maison":0,
         "Appartement":1,
         "Vente sur plan":1,
         "Vente en l'état":0}
   
   col7, col8 = st.columns(2)
   with col7:
      commune = st.selectbox(
                           'Commune',
                           sorted(tuple(df_prix.index)),
                           )

   with col8:   
      Type_de_vente = st.selectbox(
                        'Type_de_vente',
                        ("Vente en l'état",
                         "Vente sur plan",),
                        )


   col3, col4 = st.columns(2)
   
   with col3:
      
      Logement = st.selectbox( 
         'Logement',
         ('Appartement','Maison'),
      )

   with col4:
      nombre_de_pièces = st.number_input("Nombre de pièces",
            min_value=1,
            max_value=40,
            value=5,
            step=1,
            )

   col5, col6 = st.columns(2)
   
   with col5:

      surface_sol = st.slider("Surface au sol (m²)",
                     min_value=9,
                     max_value=500,
                     value=100,
                     step=1,
                     )
   
   with col6:
      surface_terrain = st.slider("Surface terrain (m²)",
               min_value=0,
               max_value=1000,
               step=10,
               )
   

   Type_de_vente = dico[Type_de_vente]
   Logement = dico[Logement]
   
   valeurs = np.array([[df_prix['mean'].loc[commune],Logement,surface_sol,nombre_de_pièces,surface_terrain,Type_de_vente]])
   valeurs = scaler.transform(valeurs)
   prediction = round(knn.predict(valeurs)[0], -3)

   st.write(f"Pour un bien de ce genre, attendez-vous à un montant d'à peu près {int(prediction)} €")
            
#