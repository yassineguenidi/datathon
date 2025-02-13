import streamlit as st
import pandas as pd
from joblib import load

# Charger les modèles
model_localisation = load(r"C:\Users\yassi\PycharmProjects\datathon\models\model_localisation.joblib")
model_intensite = load(r"C:\Users\yassi\PycharmProjects\datathon\models\model_intensite.joblib")

from sklearn.preprocessing import LabelEncoder

# Création du label encoder
label_encoder_localisation = LabelEncoder()
df= pd.read_csv(r"C:\Users\yassi\PycharmProjects\datathon\data\df.csv")


# Encodage de la colonne
df['Localisation des tensions'] = label_encoder_localisation.fit_transform(df['Localisation des tensions'])

# Exemple de prédiction (supposons que ton modèle renvoie un nombre)
prediction = 7  # Exemple de valeur prédite

# Décodage pour retrouver le label original
label_original = label_encoder_localisation.inverse_transform([prediction])[0]

print(f"Prédiction : {label_original}")



# Titre de l'application
st.title("Prédiction des Résultats")

# Entrée des données
age = st.number_input("Age", min_value=0, max_value=120, step=1, format="%d",value=25)
sexe = st.radio("Sexe", ["Homme", "Femme"], index=None)
taille = st.slider("Taille (cm)", 0, 250, 170)
poids = st.slider("Poids (kg)", 0, 300, 70)

type_pied = st.selectbox("Type de pied", ["Normal", "Plat", "Creux"], index=None)
# presence_tension = st.radio("Présence de tensions", ["Oui", "Non"], index=None)
# localisation_tensions = st.multiselect("Localisation des tensions",
#                                        ["Aucun", "Genoux valgum", "Cyphose dorsale",
#                                         "Épaule antépulsée", "Hyperlordose lombaire"])

desequilibres_posturaux = st.selectbox("Déséquilibres posturaux",
                                       ["Aucun", "Genoux valgum", "Cyphose dorsale",
                                        "Épaule antépulsée", "Hyperlordose lombaire"], index=None)

# Distances
distance_acromion_g = st.slider("Distance Acromion G (cm)", 0, 250, 50)
distance_acromion_d = st.slider("Distance Acromion D (cm)", 0, 250, 50)
distance_eips_g = st.slider("Distance EIPS G (cm)", 0, 250, 50)
distance_eips_d = st.slider("Distance EIPS D (cm)", 0, 250, 50)
distance_t4 = st.slider("Distance T4 (cm)", 0, 250, 50)
distance_l1 = st.slider("Distance L1 (cm)", 0, 250, 50)

# Bouton de prédiction
if st.button("Prédire"):
    if None in [sexe, type_pied,  desequilibres_posturaux]:
        st.error("Veuillez remplir tous les champs obligatoires.")
    else:
        # Création du dictionnaire avec les données saisies
        nouveau_patient = {
            'Age': [age],
            'Taille (cm)': [taille],
            'Poids (kg)': [poids],
            'Déséquilibres posturaux': [desequilibres_posturaux],
            'Distance_Acromion_G': [distance_acromion_g],
            'Distance_Acromion_D': [distance_acromion_d],
            'Distance_EIPS_G': [distance_eips_g],
            'Distance_EIPS_D': [distance_eips_d],
            'Distance_T4': [distance_t4],
            'Distance_L1': [distance_l1]
        }

        # Convertir en DataFrame
        nouveau_patient_df = pd.DataFrame(nouveau_patient)

        # Encodage des données
        nouveau_patient_encoded = pd.get_dummies(nouveau_patient_df, columns=['Déséquilibres posturaux'])

        # Assurer que les colonnes correspondent au modèle
        colonnes_attendues = [col for col in model_localisation.feature_names_in_]

        # Ajouter des colonnes manquantes avec des valeurs de 0
        for col in colonnes_attendues:
            if col not in nouveau_patient_encoded.columns:
                nouveau_patient_encoded[col] = 0

        # Réorganiser les colonnes
        nouveau_patient_encoded = nouveau_patient_encoded[colonnes_attendues]

        # Dictionnaire de correspondance des labels
        mapping_localisation = {
            0: 'Bas du dos',
            1: 'Bas droite',
            2: 'Bas gauche',
            3: 'Droite',
            4: 'Gauche',
            5: 'Haut droite',
            6: 'Haut gauche',
            7: 'Haut du dos'
        }

        # Prédictions
        localisation_predite = model_localisation.predict(nouveau_patient_encoded)
        intensite_predite = model_intensite.predict(nouveau_patient_encoded)

        # Conversion du code numérique en nom de localisation
        nom_localisation = mapping_localisation.get(localisation_predite[0], "Inconnu")

        # Affichage des résultats
        st.success("Prédiction effectuée avec succès !")
        label_original = label_encoder_localisation.inverse_transform(localisation_predite[0])
        st.write(f"Localisation prédite : {localisation_predite[0]}")
        st.write(f"Localisation prédite : {label_original}")
        st.write(f"Localisation prédite : {nom_localisation}")
        st.write(f"Intensité prédite : {intensite_predite[0]:.6f} mm")
