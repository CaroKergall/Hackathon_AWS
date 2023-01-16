import streamlit as st 
import pandas as pd 
import folium 
from streamlit_folium import st_folium
import geopandas as gpd
from shapely.geometry import shape as geoshape
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

with st.sidebar:
   st.markdown("<h1 style='text-align: center; color: grey;'>Application des filtres</h1>", unsafe_allow_html=True)
   st.markdown("----------------")
   annee = st.slider("Année observée",
                  min_value=2017,
                  max_value=2022,
                  value=2022,
                  step=1,
                  )

st.markdown("<h1 style='text-align: center; color: black;'>Map Île-de-France</h1>",
            unsafe_allow_html=True)

# st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

df_map = pd.read_csv('df_map.csv', index_col = 0)

def geometry_polygon(data):
   geom = geoshape(eval(data))
   return geom

df_map['geometry'] = df_map['geo_shape'].apply(geometry_polygon)

gdf = gpd.GeoDataFrame(df_map, crs = 4326)

m = folium.Map(location = [48.75044312, 2.25171297214], zoom_start = 9, tiles='Stamen Toner')

m.choropleth(
   geo_data = gdf[gdf['année']==annee],
   name = 'Choropleth',
   data = gdf[gdf['année']==annee],
   columns = ['Code INSEE','quantile'],
   key_on = 'feature.properties.Code INSEE',
   fill_color = 'RdYlGn_r',
   threshold_scale = [1,2,3,4,5,6,7,8],
   fill_opacity = 1,
   line_opacity = 1,
   legend_name = 'Prix moyen au m² (quantile)',
   smooth_factor =  0
)

# ajout de l'interactivité au survol

style_function = lambda x: {'fillColor': '#ffffff', 
                           'color':'#000000', 
                           'fillOpacity': 0.1, 
                           'weight': 0.1}
highlight_function = lambda x: {'fillColor': '#000000', 
                              'color':'#000000', 
                              'fillOpacity': 0.50, 
                              'weight': 0.1}
NIL = folium.features.GeoJson(
   gdf[gdf['année']==annee],
   style_function=style_function, 
   control=False,
   highlight_function=highlight_function, 
   tooltip=folium.features.GeoJsonTooltip(
      fields=['Commune','prix_m2','conso'],
      aliases=['Commune : ','Prix moyen au m² :','Consommation moyenne par m² (KWh) :'],
      style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
   )
)
m.add_child(NIL)
m.keep_in_front(NIL)
folium.LayerControl().add_to(m)

st_folium(m, width=1080)