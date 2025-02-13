import streamlit as st

# Titre de l'application
st.title("Prédiction des Résultats")

# Entrée des données
age = st.number_input("Âge", min_value=0, max_value=120, step=1)
sexe = st.radio("Sexe", ["Homme", "Femme"])
taille = st.slider("Taille (cm)", 0, 250, 170)
poids = st.slider("Poids (kg)", 0, 300, 70)

type_pied = st.selectbox("Type de pied", ["Normal", "Plat", "Creux"])
presence_tension = st.radio("Présence de tensions", ["Oui", "Non"])
# localisation_tensions = st.multiselect("Localisation des tensions",
#                                         ["Aucun", "Genoux valgum", "Cyphose dorsale",
#                                          "Épaule antépulsée", "Hyperlordose lombaire"])

desequilibres_posturaux = st.multiselect("Déséquilibres posturaux",
                                          ["Aucun", "Genoux valgum", "Cyphose dorsale",
                                           "Épaule antépulsée", "Hyperlordose lombaire"])

# Distances
distance_acromion_g = st.slider("Distance Acromion G (cm)", 0, 250, 50)
distance_acromion_d = st.slider("Distance Acromion D (cm)", 0, 250, 50)
distance_eips_g = st.slider("Distance EIPS G (cm)", 0, 250, 50)
distance_eips_d = st.slider("Distance EIPS D (cm)", 0, 250, 50)
distance_t4 = st.slider("Distance T4 (cm)", 0, 250, 50)
distance_l1 = st.slider("Distance L1 (cm)", 0, 250, 50)

# Bouton de prédiction
if st.button("Prédire"):
    # Simulation de prédiction (remplacer avec un modèle réel)
    st.success("Prédiction effectuée avec succès !")

