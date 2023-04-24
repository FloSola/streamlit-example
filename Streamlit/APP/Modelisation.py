#!/usr/bin/env python
# coding: utf-8



def Modelisation():
    import streamlit as st
    import pandas as pd
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    
    import seaborn as sns
    sns.set_theme()
    sns.set_palette("vlag")
    
    import numpy as np
    
    import matplotlib.pyplot as plt
    #get_ipython().run_line_magic('matplotlib', 'inline')
    
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import OneHotEncoder
    from sklearn.metrics import mean_squared_error, mean_absolute_error


       
    total = pd.read_csv('../APP/data/DataFrames/total', sep = ',', index_col = 0 )
    total_stats = pd.read_csv('../APP/data/DataFrames/total_stats', sep = ',', index_col = 0 )
    total_j = pd.read_csv('../APP/data/DataFrames/total_j', sep = ',', index_col = 0)
    G = pd.read_csv('../APP/data/DataFrames/G',sep = ',', index_col = 0)
    G_j = pd.read_csv('../APP/data/DataFrames/G_j', sep = ',', index_col = 0)
    D = pd.read_csv('../APP/data/DataFrames/D',sep = ',', index_col = 0)
    D_j = pd.read_csv('../APP/data/DataFrames/D_j', sep = ',', index_col = 0)
    M = pd.read_csv('../APP/data/DataFrames/M',sep = ',', index_col = 0)
    M_j = pd.read_csv('../APP/data/DataFrames/M_j', sep = ',', index_col = 0)
    A = pd.read_csv('../APP/data/DataFrames/A',sep = ',', index_col = 0)
    A_j = pd.read_csv('../APP/data/DataFrames/A_j', sep = ',', index_col = 0)
   
    #if st.checkbox("Showing the data") :
    line_to_plot = st.slider("sélectionner le nombre de lignes à afficher", min_value=3, max_value=total.shape[0])
    st.dataframe(total.head(line_to_plot))
   
    
   
    #Lorsqu'un joueur n'a pas joué lors d'un match, sa note est de zéro, il faut donc traiter cette donnée en la remplacant par la moyenne du joueur (la 'Note')
    total_j_mean = total_j.replace(to_replace = 0.0,
                      value = np.nan)
    
    total_j_mean = total_j_mean.apply(lambda x: x.fillna(value=total_j['Note']))
    
    G_j_mean = G_j.replace(to_replace = 0.0,
                      value = np.nan)
    
    G_j_mean = G_j_mean.apply(lambda x: x.fillna(value=G_j['Note']))
    
    
    D_j_mean = D_j.replace(to_replace = 0.0,
                      value = np.nan)
    D_j_mean = D_j_mean.apply(lambda x: x.fillna(value=D_j['Note']))
    
    
    M_j_mean = M_j.replace(to_replace = 0.0,
                      value = np.nan)
    M_j_mean = M_j_mean.apply(lambda x: x.fillna(value=M_j['Note']))
    
    
    A_j_mean = A_j.replace(to_replace = 0.0,
                      value = np.nan)
    A_j_mean = A_j_mean.apply(lambda x: x.fillna(value=A_j['Note']))
    
    
    #Au lieu de la moyenne, n peut également remplacer les NaN par la note du précédent match.
    total_j_last = total_j.replace(to_replace = 0.0,
                      value = np.nan)
    
    total_j_last = total_j_last.fillna(method="ffill", axis=1)
    
    G_j_last = G_j.replace(to_replace = 0.0,
                      value = np.nan)
    
    G_j_last = G_j_last.fillna(method="ffill", axis=1)
    
    
    D_j_last = D_j.replace(to_replace = 0.0,
                      value = np.nan)
    D_j_last = D_j_last.fillna(method="ffill", axis=1)
    
    
    M_j_last = M_j.replace(to_replace = 0.0,
                      value = np.nan)
    M_j_last = M_j_last.fillna(method="ffill", axis=1)
    
    
    A_j_last = A_j.replace(to_replace = 0.0,
                      value = np.nan)
    A_j_last = A_j_last.fillna(method="ffill", axis=1)
    
    st.title("Application de Pycaret sur les DataFrames")
    page_names = ['DataFrame complet','DataFrame journées','DataFrame statistiques']
    page = st.radio('Choix du DataFrame', page_names, horizontal = True)
    
    if page == 'DataFrame complet':
        st.subheader('complet')
        from PIL import Image
        BEST_MODEL_TOTAL = Image.open("BEST_MODEL_TOTAL.jpg")
        st.image(BEST_MODEL_TOTAL, caption="Meilleur modèle appliqué sur le DataFrame complet")
        PLOT_ERROR_TOTAL = Image.open("PLOT_ERROR_TOTAL.jpg")
        st.image(PLOT_ERROR_TOTAL, caption="Prediction Error")
        FEATURE_IMPORTANCE_TOTAL = Image.open("FEATURE_IMPORTANCE_TOTAL.jpg")
        st.image(FEATURE_IMPORTANCE_TOTAL, caption="Feature Importance")
        PCA_DU_DF_TOTAL_GRAPH = Image.open("PCA DU DF TOTAL GRAPH.png")
        st.image(PCA_DU_DF_TOTAL_GRAPH, caption="")   
        PCA_DU_DF_TOTAL_PIE_PLOT = Image.open("PCA DU DF TOTAL PIE CHART.png")
        st.image(PCA_DU_DF_TOTAL_PIE_PLOT, caption="")   
    else : 
        if page == 'DataFrame journées':
            st.subheader('journées') 
            from PIL import Image
            BEST_MODEL_JOURNEES = Image.open("BEST_MODEL_JOURNEES.jpg")
            st.image(BEST_MODEL_JOURNEES, caption="Meilleur modèle appliqué sur le DataFrame journées")
            PLOT_ERROR_JOURNEES = Image.open("PLOT_ERROR_JOURNEES.jpg")
            st.image(PLOT_ERROR_JOURNEES, caption="Prediction Error")
            FEATURE_IMPORTANCE_JOURNEES = Image.open("FEATURE_IMPORTANCE_JOURNEES.jpg")
            st.image(FEATURE_IMPORTANCE_JOURNEES, caption="Feature Importance")
            PCA_DU_DF_NOTES_GRAPH = Image.open("PCA DU DF NOTES GRAPH.png")
            st.image(PCA_DU_DF_NOTES_GRAPH, caption="")   
            PCA_DU_DF_NOTES_PIE_PLOT = Image.open("PCA DU DF NOTES PIE CHART.png")
            st.image(PCA_DU_DF_NOTES_PIE_PLOT, caption="")   
        else : 
            if page == 'DataFrame statistiques':
                st.subheader('statistiques')
                from PIL import Image
                BEST_MODEL_STATS = Image.open("BEST_MODEL_STATS.jpg")
                st.image(BEST_MODEL_STATS, caption="Meilleur modèle appliqué sur le DataFrame journées")
                PLOT_ERROR_STATS = Image.open("PLOT_ERROR_STATS.jpg")
                st.image(PLOT_ERROR_STATS, caption="Prediction Error")
                FEATURE_IMPORTANCE_STATS = Image.open("FEATURE_IMPORTANCE_STAT.jpg")
                st.image(FEATURE_IMPORTANCE_STATS, caption="Feature Importance")
                PCA_DU_DF_STATS_GRAPH = Image.open("PCA DU DF STATS GRAPH.png")
                st.image(PCA_DU_DF_STATS_GRAPH, caption="")   
                PCA_DU_DF_STATS_PIE_PLOT = Image.open("PCA DU DF STATS PIE CHART.png")
                st.image(PCA_DU_DF_STATS_PIE_PLOT, caption="")
    

    
    
    
    
    
    #from pycaret.regression import create_model, compare_models, setup

    #exp_mean = setup(data = total_j_mean, target = 'j19', session_id = 123)    
    #st.dataframe(exp_mean)
    
    #best_model_mean = exp_mean.compare_models()
    #print(best_model_mean)
    
    
    #exp_mean.plot_model(best_model_mean, plot = 'error')
    #exp_mean.plot_model(best_model_mean, plot = 'feature')
    #exp_mean.predict_model(best_model_mean).head(10)    