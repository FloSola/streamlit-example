# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 14:49:23 2023

@author: sitte
"""

import streamlit as st
import pandas as pd

Liga_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGA/predictions_liga_G', sep = ',', index_col = 0)
Liga_G = Liga_G['prediction_label']
Liga_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGA/predictions_liga_D', sep = ',', index_col = 0)
Liga_D = Liga_D['prediction_label']
Liga_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGA/predictions_liga_M', sep = ',', index_col = 0)
Liga_M = Liga_M['prediction_label']
Liga_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGA/predictions_liga_A', sep = ',', index_col = 0)
Liga_A = Liga_A['prediction_label']

Ligue_1_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_1/predictions_ligue_1_G', sep = ',', index_col = 0)
Ligue_1_G = Ligue_1_G['prediction_label']
Ligue_1_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_1/predictions_ligue_1_D', sep = ',', index_col = 0)
Ligue_1_D = Ligue_1_D['prediction_label']
Ligue_1_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_1/predictions_ligue_1_M', sep = ',', index_col = 0)
Ligue_1_M = Ligue_1_M['prediction_label']
Ligue_1_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_1/predictions_ligue_1_A', sep = ',', index_col = 0)
Ligue_1_A = Ligue_1_A['prediction_label']

Ligue_2_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_2/predictions_ligue_2_G', sep = ',', index_col = 0)
Ligue_2_G = Ligue_2_G['prediction_label']
Ligue_2_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_2/predictions_ligue_2_D', sep = ',', index_col = 0)
Ligue_2_D = Ligue_2_D['prediction_label']
Ligue_2_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_2/predictions_ligue_2_M', sep = ',', index_col = 0)
Ligue_2_M = Ligue_2_M['prediction_label']
Ligue_2_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_LIGUE_2/predictions_ligue_2_A', sep = ',', index_col = 0)
Ligue_2_A = Ligue_2_A['prediction_label']

Premiere_league_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_PREMIER_LEAGUE/predictions_Premier_league_G', sep = ',', index_col = 0)
Premiere_league_G = Premiere_league_G['prediction_label']
Premiere_league_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_PREMIER_LEAGUE/predictions_Premier_league_D', sep = ',', index_col = 0)
Premiere_league_D = Premiere_league_D['prediction_label']
Premiere_league_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_PREMIER_LEAGUE/predictions_Premier_league_M', sep = ',', index_col = 0)
Premiere_league_M = Premiere_league_M['prediction_label']
Premiere_league_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_PREMIER_LEAGUE/predictions_Premier_league_A', sep = ',', index_col = 0)
Premiere_league_A = Premiere_league_A['prediction_label']

SerieA_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_SERIE_A/predictions_SerieA_G', sep = ',', index_col = 0)
SerieA_G = SerieA_G['prediction_label']
SerieA_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_SERIE_A/predictions_SerieA_D', sep = ',', index_col = 0)
SerieA_D = SerieA_D['prediction_label']
SerieA_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_SERIE_A/predictions_SerieA_M', sep = ',', index_col = 0)
SerieA_M = SerieA_M['prediction_label']
SerieA_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_SERIE_A/predictions_SerieA_A', sep = ',', index_col = 0)
SerieA_A = SerieA_A['prediction_label']

predictions_G = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_POSTE/predictions_G', sep = ',', index_col = 0)
predictions_D = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_POSTE/predictions_D', sep = ',', index_col = 0)
predictions_M = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_POSTE/predictions_M', sep = ',', index_col = 0)
predictions_A = pd.read_csv('../APP/data/DataFrames/PREDICTIONS_POSTE/predictions_A', sep = ',', index_col = 0)


def Formation():
    df_G = None
    df_D = None
    df_M = None
    df_A = None
    formation_options = ['4-4-2','4-2-4', '3-4-3','3-5-2','5-4-1']

    league_options = ['Ligue 1', 'Ligue 2', 'Premiere League', 'Serie A', 'Liga']

    formation_option = st.selectbox('Choisissez une formation', formation_options)
    
    # Création de la checkbox pour les options de ligue
    league_option = st.multiselect('Choisissez les ligues', league_options)
    
    # Utilisation des conditions if pour sélectionner les meilleures valeurs à partir des dataframes
    if st.button('Afficher les résultats'):
        if formation_option == '4-4-2':
            df_G_titu = predictions_G[predictions_G['Championnat'].isin(league_option)].head(1)
            predictions_G.drop(df_G_titu.index, inplace=True)
            df_D_titu = predictions_D[predictions_D['Championnat'].isin(league_option)].head(4)
            predictions_D.drop(df_D_titu.index, inplace=True)
            df_M_titu = predictions_M[predictions_M['Championnat'].isin(league_option)].head(4)
            predictions_M.drop(df_M_titu.index, inplace=True)
            df_A_titu = predictions_A[predictions_A['Championnat'].isin(league_option)].head(2)
            predictions_A.drop(df_A_titu.index, inplace=True)
            st.write('Meilleur Gardien :')
            st.write(df_G_titu)
            st.write('Meilleurs Défenseurs :')
            st.write(df_D_titu)
            st.write('Meilleurs Milieux :')
            st.write(df_M_titu)
            st.write('Meilleurs Attaquants :')
            st.write(df_A_titu)
            df_G_remplacants = predictions_G[predictions_G['Championnat'].isin(league_option)].head(3)
            df_D_remplacants = predictions_D[predictions_D['Championnat'].isin(league_option)].head(6)
            df_M_remplacants = predictions_M[predictions_M['Championnat'].isin(league_option)].head(6)
            df_A_remplacants = predictions_A[predictions_A['Championnat'].isin(league_option)].head(4)
            st.write('Les meilleurs Gardiens remplaçants sont :')
            st.write(df_G_remplacants)
            st.write('Les meilleurs Défenseurs remplaçants sont :')
            st.write(df_D_remplacants)
            st.write('Les meilleurs Milieux remplaçants sont :')
            st.write(df_M_remplacants)
            st.write('Les meilleurs Attaquants remplaçants :')
            st.write(df_A_remplacants)
        
        elif formation_option == '3-4-3':
            df_G_titu = predictions_G[predictions_G['Championnat'].isin(league_option)].head(1)
            predictions_G.drop(df_G_titu.index, inplace=True)
            df_D_titu = predictions_D[predictions_D['Championnat'].isin(league_option)].head(3)
            predictions_D.drop(df_D_titu.index, inplace=True)
            df_M_titu = predictions_M[predictions_M['Championnat'].isin(league_option)].head(4)
            predictions_M.drop(df_M_titu.index, inplace=True)
            df_A_titu = predictions_A[predictions_A['Championnat'].isin(league_option)].head(3)
            predictions_A.drop(df_A_titu.index, inplace=True)
            st.write('Meilleur Gardien :')
            st.write(df_G_titu)
            st.write('Meilleurs Défenseurs :')
            st.write(df_D_titu)
            st.write('Meilleurs Milieux :')
            st.write(df_M_titu)
            st.write('Meilleurs Attaquants :')
            st.write(df_A_titu)
            df_G_remplacants = predictions_G[predictions_G['Championnat'].isin(league_option)].head(3)
            df_D_remplacants = predictions_D[predictions_D['Championnat'].isin(league_option)].head(5)
            df_M_remplacants = predictions_M[predictions_M['Championnat'].isin(league_option)].head(6)
            df_A_remplacants = predictions_A[predictions_A['Championnat'].isin(league_option)].head(5)
            st.write('Les meilleurs Gardiens remplaçants sont :')
            st.write(df_G_remplacants)
            st.write('Les meilleurs Défenseurs remplaçants sont :')
            st.write(df_D_remplacants)
            st.write('Les meilleurs Milieux remplaçants sont :')
            st.write(df_M_remplacants)
            st.write('Les meilleurs Attaquants remplaçants :')
            st.write(df_A_remplacants)
              
        elif formation_option == '5-4-1':
                df_G_titu = predictions_G[predictions_G['Championnat'].isin(league_option)].head(1)
                predictions_G.drop(df_G_titu.index, inplace=True)
                df_D_titu = predictions_D[predictions_D['Championnat'].isin(league_option)].head(5)
                predictions_D.drop(df_D_titu.index, inplace=True)
                df_M_titu = predictions_M[predictions_M['Championnat'].isin(league_option)].head(4)
                predictions_M.drop(df_M_titu.index, inplace=True)
                df_A_titu = predictions_A[predictions_A['Championnat'].isin(league_option)].head(1) 
                predictions_A.drop(df_A_titu.index, inplace=True)
                st.write('Meilleur Gardien :')
                st.write(df_G_titu)
                st.write('Meilleurs Défenseurs :')
                st.write(df_D_titu)
                st.write('Meilleurs Milieux :')
                st.write(df_M_titu)
                st.write('Meilleurs Attaquants :')
                st.write(df_A_titu)
                df_G_remplacants = predictions_G[predictions_G['Championnat'].isin(league_option)].head(3)
                df_D_remplacants = predictions_D[predictions_D['Championnat'].isin(league_option)].head(7)
                df_M_remplacants = predictions_M[predictions_M['Championnat'].isin(league_option)].head(6)
                df_A_remplacants = predictions_A[predictions_A['Championnat'].isin(league_option)].head(3)
                st.write('Les meilleurs Gardiens remplaçants sont :')
                st.write(df_G_remplacants)
                st.write('Les meilleurs Défenseurs remplaçants sont :')
                st.write(df_D_remplacants)
                st.write('Les meilleurs Milieux remplaçants sont :')
                st.write(df_M_remplacants)
                st.write('Les meilleurs Attaquants remplaçants :')
                st.write(df_A_remplacants)
           
        elif formation_option == '4-2-4':
            df_G_titu = predictions_G[predictions_G['Championnat'].isin(league_option)].head(1)
            predictions_G.drop(df_G_titu.index, inplace=True)
            df_D_titu = predictions_D[predictions_D['Championnat'].isin(league_option)].head(4)
            predictions_D.drop(df_D_titu.index, inplace=True)
            df_M_titu = predictions_M[predictions_M['Championnat'].isin(league_option)].head(2)
            predictions_M.drop(df_M_titu.index, inplace=True)
            df_A_titu = predictions_A[predictions_A['Championnat'].isin(league_option)].head(4)
            predictions_A.drop(df_A_titu.index, inplace=True)
            st.write('Meilleur Gardien :')
            st.write(df_G_titu)
            st.write('Meilleurs Défenseurs :')
            st.write(df_D_titu)
            st.write('Meilleurs Milieux :')
            st.write(df_M_titu)
            st.write('Meilleurs Attaquants :')
            st.write(df_A_titu)
            df_G_remplacants = predictions_G[predictions_G['Championnat'].isin(league_option)].head(3)
            df_D_remplacants = predictions_D[predictions_D['Championnat'].isin(league_option)].head(6)
            df_M_remplacants = predictions_M[predictions_M['Championnat'].isin(league_option)].head(4)
            df_A_remplacants = predictions_A[predictions_A['Championnat'].isin(league_option)].head(6)
            st.write('Les meilleurs Gardiens remplaçants sont :')
            st.write(df_G_remplacants)
            st.write('Les meilleurs Défenseurs remplaçants sont :')
            st.write(df_D_remplacants)
            st.write('Les meilleurs Milieux remplaçants sont :')
            st.write(df_M_remplacants)
            st.write('Les meilleurs Attaquants remplaçants :')
            st.write(df_A_remplacants)
            
        elif formation_option == '3-5-2':
            df_G_titu = predictions_G[predictions_G['Championnat'].isin(league_option)].head(1)
            predictions_G.drop(df_G_titu.index, inplace=True)
            df_D_titu = predictions_D[predictions_D['Championnat'].isin(league_option)].head(3)
            predictions_D.drop(df_D_titu.index, inplace=True)
            df_M_titu = predictions_M[predictions_M['Championnat'].isin(league_option)].head(5)
            predictions_M.drop(df_M_titu.index, inplace=True)
            df_A_titu = predictions_A[predictions_A['Championnat'].isin(league_option)].head(2)
            predictions_A.drop(df_A_titu.index, inplace=True)
            st.write('Meilleur Gardien :')
            st.write(df_G_titu)
            st.write('Meilleurs Défenseurs :')
            st.write(df_D_titu)
            st.write('Meilleurs Milieux :')
            st.write(df_M_titu)
            st.write('Meilleurs Attaquants :')
            st.write(df_A_titu)
            df_G_remplacants = predictions_G[predictions_G['Championnat'].isin(league_option)].head(3)
            df_D_remplacants = predictions_D[predictions_D['Championnat'].isin(league_option)].head(5)
            df_M_remplacants = predictions_M[predictions_M['Championnat'].isin(league_option)].head(7)
            df_A_remplacants = predictions_A[predictions_A['Championnat'].isin(league_option)].head(4)
            st.write('Les meilleurs Gardiens remplaçants sont :')
            st.write(df_G_remplacants)
            st.write('Les meilleurs Défenseurs remplaçants sont :')
            st.write(df_D_remplacants)
            st.write('Les meilleurs Milieux remplaçants sont :')
            st.write(df_M_remplacants)
            st.write('Les meilleurs Attaquants remplaçants :')
            st.write(df_A_remplacants)