import streamlit as st 
import pandas as pd 
import numpy as np

from ml import * 

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

st.markdown("<h1 style='text-align: center; color: black;'>Prévoyez le prix de votre bien</h1>",
            unsafe_allow_html=True)

col9, col10, col11 = st.columns(3)
with col9:
    st.write('')
with col10:
    st.image("https://upload.wikimedia.org/wikipedia/commons/7/75/Maison_Adam_de_Villiers.jpg",
    width=500)
with col11:
    st.write('')

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

valeurs = np.array([[df_prix['mean'].loc[commune],
                   Logement,
                   surface_sol,
                   nombre_de_pièces,
                   surface_terrain,
                   Type_de_vente]])
valeurs = scaler.transform(valeurs)
prediction = round(knn.predict(valeurs)[0], -3)

st.write(f"Pour un bien de ce genre, attendez-vous à un montant d'à peu près {int(prediction)} €")