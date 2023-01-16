import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

st.markdown("<h1 style='text-align: center; color: black;'>Bienvenue</h1>",
            unsafe_allow_html=True)

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


#Centrer une image
col1, col2, col3 = st.columns(3)
with col1:
    st.write('')
with col2:
    st.image("clef.png",
             width=500)
with col3:
    st.write('')