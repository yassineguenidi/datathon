import streamlit as st
import pandas as pd
import pickle
from joblib import load
from sklearn.preprocessing import LabelEncoder


# Charger les modèles
model_localisation = load(r"C:\Users\yassi\PycharmProjects\datathon\models\model_localisation.joblib")
model_intensite = load(r"C:\Users\yassi\PycharmProjects\datathon\models\model_intensite.joblib")

# Charger les règles d'association
with open(r"C:\Users\yassi\PycharmProjects\datathon\models\regles_association_des.pkl", "rb") as f:
    rules_df = pickle.load(f)

label_encoder_localisation = LabelEncoder()
df= pd.read_csv(r"C:\Users\yassi\PycharmProjects\datathon\data\df.csv")
# Encodage de la colonne
df['Localisation des tensions'] = label_encoder_localisation.fit_transform(df['Localisation des tensions'])



# Titre de l'application
st.title("Prédiction et Règles d'Association")

# Entrée des données utilisateur
age = st.number_input("Age", min_value=0, max_value=120, step=1, format="%d", value=25)
sexe = st.radio("Sexe", ["Homme", "Femme"], index=0)
taille = st.slider("Taille (cm)", 0.0, 250.0, 170.0, step=0.1)
poids = st.slider("Poids (kg)", 0.0, 300.0, 70.0, step=0.1)
type_pied = st.selectbox("Type de pied", ["Normal", "Plat", "Creux"], index=None)
desequilibres_posturaux = st.selectbox("Déséquilibres posturaux",
                                       ["Aucun", "Genoux valgum", "Cyphose dorsale",
                                        "Épaule antépulsée", "Hyperlordose lombaire"], index=None)

# Distances mesurées
distances = {
    "Acromion G": st.slider("Distance Acromion G (cm)", 0.0, 250.0, 50.0 ,step=0.01),
    "Acromion D": st.slider("Distance Acromion D (cm)", 0.0, 250.0, 50.0 ,step=0.01),
    "EIPS G": st.slider("Distance EIPS G (cm)", 0.0, 250.0, 50.0 ,step=0.01),
    "EIPS D": st.slider("Distance EIPS D (cm)", 0.0, 250.0, 50.0 ,step=0.01),
    "T4": st.slider("Distance T4 (cm)", 0.0, 250.0, 50.0 ,step=0.01),
    "L1": st.slider("Distance L1 (cm)", 0.0, 250.0, 50.0 ,step=0.01),
}

# Seuils définis pour détecter les tensions
seuils = {
    "Acromion G": 30,
    "Acromion D": 30,
    "EIPS G": 30,
    "EIPS D": 30,
    "T4": 30,
    "L1": 30
}

# Générer la transaction du patient
transaction_patient = set()
if desequilibres_posturaux != "Aucun":
    transaction_patient.add(f"Déséquilibres posturaux_{desequilibres_posturaux}")

for key, value in distances.items():
    if value >= seuils[key]:
        transaction_patient.add(f"Tension_{key.replace(' ', '_')}")

# Bouton de prédiction
if st.button("Prédire"):
    if None in [sexe, desequilibres_posturaux]:
        st.error("Veuillez remplir tous les champs obligatoires.")
    else:
        # Création du DataFrame pour la prédiction
        nouveau_patient_df = pd.DataFrame([{
            'Age': age,
            'Taille (cm)': taille,
            'Poids (kg)': poids,
            'Type du pied': type_pied,
            'Déséquilibres posturaux': desequilibres_posturaux,
            **distances
        }])

        # Encodage des données
        nouveau_patient_encoded = pd.get_dummies(nouveau_patient_df, columns=['Déséquilibres posturaux'])
        colonnes_attendues = list(model_localisation.feature_names_in_)

        for col in colonnes_attendues:
            if col not in nouveau_patient_encoded.columns:
                nouveau_patient_encoded[col] = 0

        nouveau_patient_encoded = nouveau_patient_encoded[colonnes_attendues]

        # Prédictions
        localisation_predite = model_localisation.predict(nouveau_patient_encoded)
        intensite_predite = model_intensite.predict(nouveau_patient_encoded)

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

        # nom_localisation = mapping_localisation.get(localisation_predite[0], "Inconnu")
        # Décodage pour retrouver le label original
        nom_localisation = label_encoder_localisation.inverse_transform(localisation_predite)[0]

        # Affichage des résultats
        st.success("Prédiction effectuée avec succès !")
        st.write(f"Localisation prédite : {nom_localisation}")
        st.write(f"Intensité prédite : {intensite_predite[0]:.6f} mm")

        # Vérifier quelles règles s'appliquent au patient
        applicable_rules = []
        for _, rule in rules_df.iterrows():
            antecedents_set = set(rule['antecedents'])  # 'antecedents' est un frozenset, pas besoin de split
            if antecedents_set.issubset(transaction_patient):
                applicable_rules.append(rule)

        # Afficher les règles applicables
        # if applicable_rules:
        #     applicable_df = pd.DataFrame(applicable_rules)
        #     st.write("### Règles applicables au patient :")
        #     st.dataframe(applicable_df[['antecedents', 'consequents', 'support', 'confidence', 'lift']])
        # else:
        #     st.write("Aucune règle applicable pour ce patient.")

        if applicable_rules:
            applicable_df = pd.DataFrame(applicable_rules)

            # Trouver la règle avec le lift maximal
            best_rule = applicable_df.loc[applicable_df['lift'].idxmax()]

            st.write("### Meilleure règle applicable :")
            st.write(f"**Antécédents :** {best_rule['antecedents']}")
            st.write(f"**Conséquence :** {best_rule['consequents']}")
            st.write(f"**Lift :** {best_rule['lift']:.2f}")
        else:
            st.write("Aucune règle applicable pour ce patient.")
        st.write("____________________________________________")
        # Mapping pour la traduction des déséquilibres posturaux
        mapping_desequilibre = {
            'Déséquilibres posturaux_Genoux valgum': "genoux valgum",
            'Déséquilibres posturaux_Cyphose dorsale': "cyphose dorsale",
            'Déséquilibres posturaux_Épaule antépulsée': "épaules antéversées",
            'Déséquilibres posturaux_Hyperlordose lombaire': "hyperlordose lombaire"
        }

        # Extraction des valeurs
        localisation = nom_localisation
        intensite = f"{intensite_predite[0]:.6f} mm"
        best_antecedent = list(best_rule['antecedents'])[0]  # Extraction de la première valeur du frozenset
        best_consequent = list(best_rule['consequents'])[0]  # Extraction de la première valeur du frozenset
        lift = f"{best_rule['lift']:.3f}"

        # Traduire le déséquilibre postural si possible
        antecedent_traduit = mapping_desequilibre.get(best_antecedent, best_antecedent)

        # Déterminer la catégorie d’intensité
        if float(intensite_predite[0]) < 0.05:
            categorie_intensite = "faible"
        elif 0.05 <= float(intensite_predite[0]) < 0.15:
            categorie_intensite = "moyenne"
        else:
            categorie_intensite = "élevée"

        # Générer le message d'interprétation
        interpretation = f"""
        ### **Interprétation**
        Si un patient présente **{antecedent_traduit}**, il est fortement probable (avec une confiance élevée) qu'il aura une tension à la **{localisation}** avec une épaisseur de **{intensite}**, classée dans la catégorie **{categorie_intensite}**.

        La relation entre ces deux événements est forte et significative, avec un **lift de {lift}**.
        """

        st.markdown(interpretation)


