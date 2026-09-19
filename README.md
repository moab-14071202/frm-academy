# FRM Academy — V0.2

Prototype Streamlit d'une plateforme d'apprentissage FRM Part I, avec un design validé en **mode clair** (blanc / beige / noir) et **mode sombre** type codeur/geek.

## Contenu de cette V0.2

- Dashboard d'accueil sobre
- Navigation : **Accueil / Cours / QCM / À revoir**
- **Light mode** + **Dark mode**
- Flamme 🔥 de streak avec micro-animation au chargement
- Progression globale
- 4 matières FRM Part I
- Pages de cours par étape
- QCM cliquables + correction immédiate
- Réponses libres (sur certains items)
- Sauvegarde locale simple dans `.frm_academy_progress.json`

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

- La persistance est **locale** : le fichier `.frm_academy_progress.json` se crée dans le dossier du projet.
- Le contenu pédagogique détaillé n'est pour l'instant fourni que sur quelques chapitres pilotes, pour valider l'UX.
- Le reste du curriculum est déjà structuré, prêt à être enrichi.

## Roadmap V0.3 possible

- vraie base de données / utilisateur
- moteur de révision espacée
- meilleure page statistiques
- plus de contenu FRM réel chapitre par chapitre
- bouton “Demander à ChatGPT” connecté pour de vrai
- import GitHub / déploiement Streamlit Cloud
