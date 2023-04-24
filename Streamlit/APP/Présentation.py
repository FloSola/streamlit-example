# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 15:24:58 2023

@author: sitte
"""
import streamlit as st
def Présentation():
    st.title("Mon Pytit Gazon")
    
    st.header("Mon petit Gazon, Qu'est-ce que c'est?")
    
    st.video(data="https://www.youtube.com/watch?v=NGZPCgEEEV4")
    
    
    st.header("Objectif du projet")
    st.markdown("L'objectif de ce projet est d'analyser les données pour en extraire un maximum "
                "d'informations afin de composer la meilleure équipe possible et gagner la ligue    "
                "dans laquelle nous concourrons")
    
    
    from PIL import Image
    img = Image.open("COMPO.jpg")
    st.image(img, caption="Composition MPG")
    
    st.header("Méthodologie")
    
    st.subheader("Exploration des données et traitement des données")
    from PIL import Image
    img = Image.open("DATASET.jpg")
    st.image(img, caption="Extrait de la source du dataset")
    st.markdown("Nous avons utilisé deux sources de données : l'une provenant du site ""[MPG Stats](https://www.mpgstats.fr/), l'autre provenant des classements des différents championnats disponible sur de nombreux sites internet comme [L'Equipe](https://www.lequipe.fr/Football/ligue-1/page-classement-equipes/general). Nous avons ensuite compilé l'ensemble des données pour créer un seul dataset. Nous avons réalisé les traitements suivants : suppression des joueurs ayant une moyenne égale à 0, remplacement des NaN, suppression des colonnes inutiles")  
    
    
    st.subheader("Visualisation des données") 
    st.markdown("Après avoir préparé le dataset, nous avons réalisé de nombreuses datavisualisations afin de synthétiser le volume important de données et d'en extraire l'essentiel des informtaions contenues.")
                
                
                
    st.subheader("Modélisation")
    st.markdown("Pour répondre à l'objectif initial de ce projet, nous sommes passé par une phase de modélisation dans l'objectif de trouver un modèle statistique qui nous permette de faire une prédiction des notes pour les journées à venir et composer l'équipe la plus performante")