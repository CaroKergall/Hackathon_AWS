import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor

df = pd.read_csv("base_ml.csv", index_col=0)

X = df[~df["outlier"]][["mean",
                        "code_type_local",
                        "surface_reelle_bati",
                        "nombre_pieces_principales",
                        "surface_terrain",
                        "nature_mutation",
                            ]]

# Numérisation des colonnes non numériques

X["code_type_local"] = X["code_type_local"].astype(int)

X["nature_mutation"] = X["nature_mutation"].factorize()[0]

y = df[~df["outlier"]]["valeur_fonciere"]

scaler = StandardScaler()
scaler.fit(X)

X = scaler.transform(X)

knn = KNeighborsRegressor(algorithm='brute',
                          leaf_size=10,
                          n_neighbors=15)

knn.fit(X, y)

df_prix = pd.read_csv("df_prix.csv", index_col=0)