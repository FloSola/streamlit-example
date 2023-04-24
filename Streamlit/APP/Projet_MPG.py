#!/usr/bin/env python
# coding: utf-8


def Projet_MPG():
    import pandas as pd
    pd.set_option('display.max_columns', None)
    pd.set_option("display.max_rows", None)
    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
    from bokeh.plotting import figure, show, output_notebook
    from bokeh.models import ColumnDataSource, FactorRange
    from bokeh.transform import factor_cmap
    from bokeh.models import TabPanel, Tabs
    from bokeh.models.tools import HoverTool
    output_notebook()
    sns.set_theme()
    
    import streamlit as st
    
    l1 = pd.read_csv('../APP/data/MPG-L1.csv', sep = ';')
    l2 = pd.read_csv('../APP/data/MPG-L2.csv', sep = ';')
    seriea  = pd.read_csv('../APP/data/MPG-SERIEA.csv', sep = ';')
    pl = pd.read_csv('../APP/data/MPG-PL.csv', sep = ';')
    liga = pd.read_csv('../APP/data/MPG-LIGA.csv', sep = ';')
    classements = pd.read_csv('../APP/data/CLASSEMENTS.csv',sep =';') 
    
#On ajoute le championnat dans lequel chaque joueur joue pour pouvoir l'identifier plus tard.
    l1['Championnat'] = 'Ligue 1'
    l2['Championnat'] = 'Ligue 2'
    seriea['Championnat'] = 'Serie A'
    pl['Championnat'] = 'Premiere League'
    liga['Championnat'] = 'Liga'
    
#On regroupe les différents championnats dans un seul DataFrame.
#Puis on regroupe le dataframe 'Classement' avec les autres, en fusionnant par la colonne 'Club'.
    all_players = pd.concat([l1,l2,seriea,pl,liga], axis = 0)
    total = pd.merge(all_players, classements, on='Club')
    total.set_index(all_players.index,inplace=True)
    total.head()

#Traitement des NaN. Tout les NaN correspondent en réalité a des zeros, hormis l'enchère moyenne, qui est remplacée par la Cote.
#Exemple : Les Gardiens et certains joueurs de champs ne mettent pas de buts : NaN remplacé par zero.
#Exemple 2 : Certains attaquants ne font pas de tacles ou d'interceptions défensives : NaN remplacé par zero.
    total = total[(total['Note']>0)]
    
    
    fillna_zero = ['Min/But', 'Min/But 1 an', 'Min note/but', 'Cleansheet', 'But/Peno',
                   'But/Coup-franc', 'But/surface', 'Pass decis.', 'Occas° créée', 'Corner gagné', 
                   'Ballons', 'Interceptions', 'Tacles', 'Fautes', '%Passes','%Duel',
                   'But évité', 'Action stoppée','%Win+12J', '%Win+16J', '%Win+20J']
                
    
    total[fillna_zero] = total[fillna_zero].fillna(0)
    
    total['Enchère moy'] = total['Enchère moy'].fillna(total['Cote'])

    total = total.drop('Dispo@MPGLaurent?', axis = 1)
    total = total.dropna(subset = ['Cote','Enchère moy'], how = 'all', axis = 0)

    total.isna().sum()


#Une nouvelle variable qui soustrait la Cote décidé par MPG à l'enchère moyenne des utilisateurs.
#Cela permet d'analyser d'éventuels écarts par poste, championnats etc.
    total['Var E/C'] = total.apply(lambda x : x['Enchère moy']-x['Cote'], axis = 1)



#On regroupe les joueurs par rapport au classement de leur équipe dans leurs championnats respectifs.
    conditionlist = [
        (total['Classement'] >= 15) ,
        (total['Classement'] >= 10) & (total['Classement'] <15),
        (total['Classement'] >= 5) & (total['Classement'] <10),
        (total['Classement'] <= 5)]
    choicelist = ['4 - 15-20', '3 - 10-15', '2 - 5-10', '1 - 1-5']
    total['Classement_range'] = np.select(conditionlist, choicelist, default='Not Specified')



#On regroupe les joueurs par rapport à leur note dans 5 catégories.
    conditionlist = [(total['Note'] >= 8) ,
                     (total['Note'] >= 6) & (total['Note'] <8),
                     (total['Note'] >= 4) & (total['Note'] <6),
                     (total['Note'] >= 2) & (total['Note'] <4),
                     (total['Note'] <= 0)]
    choicelist = ['5 - 8 et plus', '4 - entre 6 et 8', '3 - entre 4 et 6', '2 - entre 2 et 4', '1 - moins de 2']
    total['Note_range'] = np.select(conditionlist, choicelist, default='Not Specified')


#On compartimente les joueurs par rapport à leur Enchère Moy dans 5 catégories.
    conditionlist2 = [(total['Enchère moy'] >= 80) ,
                      (total['Enchère moy'] >= 60) & (total['Enchère moy'] <80),
                      (total['Enchère moy'] >= 40) & (total['Enchère moy'] <60),
                      (total['Enchère moy'] >= 20) & (total['Enchère moy'] <40),
                      (total['Enchère moy'] <= 20)]
    choicelist2 = ['5 - 80 et plus', '4 - entre 60 et 80', '3 - entre 40 et 60', '2 - entre 20 et 40', '1 - moins de 20']
    total['Enchère_moy_range'] = np.select(conditionlist2, choicelist2, default='Not Specified')


#On sous-divise le DataFrame 'total' par position sur le terrain
#G regroupe uniquement les gardiens
#D regroupe les défenseurs centraux et latéraux.
#M regroupe les milieux défensifs et offensifs.
#A regroupe les attaquants.
    
    G = total[(total['Poste'] == 'G')]
          
    D = total[(total['Poste'] == 'DC') | (total['Poste'] == 'DL')]
    
    M = total[(total['Poste'] == 'MD') | (total['Poste'] == 'MO')]
    
    A = total[(total['Poste'] == 'A')]


#On évacue les stats par journées pour rendre les DataFrame plus lisibles.
#Toutefois elle pourront servir plus tard, donc on les stocks dans des DataFrame à part, avec la Note du joueur et sa note roulante sur 1 an.

    journées = ['j1','j2','j3','j4','j5','j6','j7','j8','j9','j10','j11','j12','j13',
                'j14','j15','j16','j17','j18','j19','j20','j21','j22','j23','j24',
                'j25','j26','j27','j28','j29','j30','j31','j32','j33','j34','j35','j36','j37','j38']
    
    note_and_journées = ['Note', 'Note 1 an','j1','j2','j3','j4','j5','j6','j7','j8','j9','j10','j11','j12','j13',
                'j14','j15','j16','j17','j18','j19','j20','j21','j22','j23','j24',
                'j25','j26','j27','j28','j29','j30','j31','j32','j33','j34','j35','j36','j37','j38']
    
    total_j = total[note_and_journées]
    G_j = G[note_and_journées]
    D_j = D[note_and_journées]
    M_j = M[note_and_journées]
    A_j = A[note_and_journées]
    
    total_df = total
    G_df = G
    D_df = D
    M_df = M
    A_df = A
    
    total = total_df.drop(journées, axis = 1)
    G = G.drop(journées, axis = 1)
    D = D.drop(journées, axis = 1)
    M = M.drop(journées, axis = 1)
    A = A.drop(journées, axis = 1)
    
   
#Lorsqu'un joueur n'a pas joué lors d'un match, sa note est de zéro, il faut donc traiter cette donnée en la remplacant par la moyenne du joueur (la 'Note')

    total_j = total_j.replace(to_replace = 0.0,
                      value = np.nan)
    total_j = total_j.apply(lambda x: x.fillna(value=total_j['Note']))
    
    
    total = total.replace(to_replace = 0.0,
                      value = np.nan)
    total = total.apply(lambda x: x.fillna(value=total['Note']))
    
    
    total_df = total_df.replace(to_replace = 0.0,
                      value = np.nan)
    total_df = total_df.apply(lambda x: x.fillna(value=total['Note']))
    
    
    G_j = G_j.replace(to_replace = 0.0,
                      value = np.nan)
    
    G_j = G_j.apply(lambda x: x.fillna(value=G_j['Note']))
    
    
    D_j = D_j.replace(to_replace = 0.0,
                      value = np.nan)
    D_j = D_j.apply(lambda x: x.fillna(value=D_j['Note']))
    
    
    M_j = M_j.replace(to_replace = 0.0,
                      value = np.nan)
    M_j = M_j.apply(lambda x: x.fillna(value=M_j['Note']))
    
    
    A_j = A_j.replace(to_replace = 0.0,
                      value = np.nan)
    A_j = A_j.apply(lambda x: x.fillna(value=A_j['Note']))

#Suppression des variables qui n'impacte pas les joueurs de cette zone du terrain.
#Exemple : Les Tacles, %Duel, Fautes, Occasion créée ne sont pas pris en compte dans la note d'un gardien.

    G =G.drop(['Min/But', 'Min note/but', '%Passes', 'Ballons', 'Interceptions', 'Tacles', '%Duel', 'Fautes', 
           'Pass decis.', 'Occas° créée', 'Min/But 1 an', 'But/surface', 'But/Coup-franc','But/Peno', 
           'Corner gagné'], axis = 1)

    D = D.drop(['But évité', 'Action stoppée'], axis = 1)
    M = M.drop(['But évité', 'Action stoppée'], axis = 1)
    A = A.drop(['But évité', 'Action stoppée'], axis = 1)
    

#Regroupement des données par Postes, en fonction de la Note et des buts inscrits    
    note_poste = total.groupby("Poste")["Note"].mean()
    but_poste = total.groupby("Poste")["But"].sum().reset_index()
    
    
#On observe que les utilisateurs sont prêts a dépenser beaucoup plus pour les attaquants,
#On en déduis que ceux-ci sont plus décisifs dans le jeu, ou pour obtenir une bonne note vs l'adversaire    
    fig, ax=plt.subplots(figsize=(15,10))
    ax.set_title("BoxPlot de l'Enchère Moyenne, par Poste, par Championnat", fontsize = 12)
    sns.boxplot(x = 'Championnat' , y = 'Enchère moy', data = total[total['Cote']>0.5], hue = 'Poste');
    st.pyplot()
     
    
#Suite du précédent Graph, malgré les fortes sommes dépensées pour les attaquants,
#ces derniers ont globalement des notes plus basses quelque soit le championnat.  
    fig, ax=plt.subplots(figsize=(15,10))
    ax.set_title('BoxPlot de la Note, par Poste, par Championnat', fontsize = 12)
    sns.boxplot(x = 'Championnat' , y = 'Note', data = total[total['Cote']>0.5], hue = 'Poste');
    st.pyplot()
     
#Les prochains graphs sont des corrélations entre la notes et les différentes statistiques
#prises en compte lors d'un match, par zone de terrain (Gardiens, Défenseurs, Milieux, Attaquants)
    
    corG = G.corr()
    
    
    corG = corG.loc[['Note']].sort_values(by = 'Note', axis = 1, ascending = False)
    corG10 = corG.iloc[:,1:11] 
    
    fig, ax=plt.subplots(figsize=(15,1))
    sns.heatmap(corG10, annot=True, ax=ax, cmap='YlOrBr')
    ax.set_title('Corrélation des stats des Gardiens', fontsize = 20)
    ax.tick_params(axis='x', rotation=60);
    st.pyplot()
    
    
    corD = D.corr()
    
    corD = corD.loc[['Note']].sort_values(by = 'Note', axis = 1, ascending = False)
    corD10 = corD.iloc[:,1:11] 
    
    fig, ax=plt.subplots(figsize=(15,1))
    sns.heatmap(corD10, annot=True, ax=ax, cmap='YlOrBr')
    ax.set_title('Corrélation des stats des Défenseurs', fontsize = 20)
    ax.tick_params(axis='x', rotation=60);
    st.pyplot()
    
    corM = M.corr()
    
    corM = corM.loc[['Note']].sort_values(by = 'Note', axis = 1, ascending = False)
    corM10 = corM.iloc[:,1:11] 
    
    fig, ax=plt.subplots(figsize=(15,1))
    sns.heatmap(corM10, annot=True, ax=ax, cmap='YlOrBr')
    ax.set_title('Corrélation des stats des Milieux', fontsize = 20)
    ax.tick_params(axis='x', rotation=60);
    st.pyplot()
    
    corA = A.corr()
    
    corA = corA.loc[['Note']].sort_values(by = 'Note', axis = 1, ascending = False)
    corA10 = corA.iloc[:,1:11] 
    
    fig, ax=plt.subplots(figsize=(15,1))
    sns.heatmap(corA10, annot=True, ax=ax, cmap='YlOrBr')
    ax.set_title('Corrélation des stats des Attaquants', fontsize = 20)
    ax.tick_params(axis='x', rotation=60);
    st.pyplot()
    
    
#Graph indiquant que plus une équipe est bien classé, plus la note moyenne d'un joueur est élevée.
    total_test = total.merge(right = classements, on = 'Club', how = 'left')
    
    
    sns.relplot(y='Note', x='Classement_y', kind='line', data=total_test[total_test['Note']>0]);
    st.pyplot()
    
 
#Graph en corrélation avec le précédent, plus une équipe a de victoires, plus la note de ses joueurs est élevé.   
    resultat_note_range = total.groupby("Note_range")["G.","N.","P."].mean().reset_index()
    resultat_note_range
        
    st.set_option('deprecation.showPyplotGlobalUse', False)
    resultat_note_range.plot.bar(x = 'Note_range', y=["G.","N.","P."], stacked=True, rot=0, alpha=1);
    st.pyplot()
    
    
#Graph montrant que les joueurs ayant une enchère plus élevé ont une note moins dispersé, et avec peu d'écart les un des autres.
    
    
    Enchère_moy_range_note = total.groupby("Enchère_moy_range")["Note"].median().reset_index()
    Enchère_moy_range_note
    
    
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(x='Enchère_moy_range', y='Note', data=total, ax =ax,
               order = ['1 - moins de 20','2 - entre 20 et 40', '3 - entre 40 et 60', '4 - entre 60 et 80', '5 - 80 et plus'])
    st.pyplot()
    
    
#On regroupe la note moyenne par Championnat-> Club -> Poste.
#Cela peut servir a identifier les points forts/faibles des clubs sur des postes ciblés par exemple.
    
    moy_poste_champ = total.groupby( by = [ 'Championnat','Club','Poste']).mean()
    
    moy_poste_champ = moy_poste_champ.reset_index()
    
    moy_poste_champ_l1 = moy_poste_champ[moy_poste_champ['Championnat'] == 'Ligue 1']
    
    moy_poste_champ_pl = moy_poste_champ[moy_poste_champ['Championnat'] == 'Premiere League']
    
    moy_poste_champ_la = moy_poste_champ[moy_poste_champ['Championnat'] == 'Liga']
    
    moy_poste_champ_sa = moy_poste_champ[moy_poste_champ['Championnat'] == 'Serie A']
    
    moy_poste_champ_l2 = moy_poste_champ[moy_poste_champ['Championnat'] == 'Ligue 2']
    
    
#Représentation de la not moyenne de tout les joueurs d'un Club, par championnat.
#Permet de cibler rapidement les clubs dans lesquels aller chercher ses joueurs lors du mercato.   
    
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot( x= 'Club', y ='Note', data = moy_poste_champ_l1, ax = ax)
    ax.set_ylim(4,7)
    ax.set_title('Moyenne des Notes par Club - Ligue 1', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    st.pyplot()
 
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot( x= 'Club', y ='Note', data = moy_poste_champ_l2, ax = ax)
    ax.set_ylim(4,7)
    ax.set_title('Moyenne des Notes par Club - Ligue 2', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot( x= 'Club', y ='Note', data = moy_poste_champ_pl, ax = ax)
    ax.set_ylim(4,7)
    ax.set_title('Moyenne des Notes par Club - Premiere League', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot( x= 'Club', y ='Note', data = moy_poste_champ_sa, ax = ax)
    ax.set_ylim(4,7)
    ax.set_title('Moyenne des Notes par Club - Serie A', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(20,10))
    sns.barplot( x= 'Club', y ='Note', data = moy_poste_champ_la, ax = ax)
    ax.set_ylim(4,7)
    ax.set_title('Moyenne des Notes par Club - Liga', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    

    
    fig, ax = plt.subplots(figsize=(15,8))
    sns.barplot( x= 'Poste', y ='Note', data = moy_poste_champ_l1, ax = ax)
    ax.set_ylim(4,6)
    ax.set_title('Moyenne des Notes par Poste - Ligue 1', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    st.pyplot()
    
    fig, ax = plt.subplots(figsize=(15,8))
    sns.barplot( x= 'Poste', y ='Note', data = moy_poste_champ_l2, ax = ax)
    ax.set_ylim(4,6)
    ax.set_title('Moyenne des Notes par Poste - Ligue 2', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(15,8))
    sns.barplot( x= 'Poste', y ='Note', data = moy_poste_champ_pl, ax = ax)
    ax.set_ylim(4,6)
    ax.set_title('Moyenne des Notes par Poste - Premiere League', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(15,8))
    sns.barplot( x= 'Poste', y ='Note', data = moy_poste_champ_sa, ax = ax)
    ax.set_ylim(4,6)
    ax.set_title('Moyenne des Notes par Poste - Seria', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    fig, ax = plt.subplots(figsize=(15,8))
    sns.barplot( x= 'Poste', y ='Note', data = moy_poste_champ_la, ax = ax)
    ax.set_ylim(4,6)
    ax.set_title('Moyenne des Notes par Poste - Liga', fontsize = 20)
    ax.tick_params(axis='x', rotation=60)
    
    
    total_bokeh = total[['Championnat','Club','Note','Poste']]

    G_l1_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 1')&(total_bokeh['Poste'] == 'G')]
    G_l2_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 2')&(total_bokeh['Poste'] == 'G')]
    G_pl_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Premiere League')&(total_bokeh['Poste'] == 'G')]
    G_sa_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Serie A')&(total_bokeh['Poste'] == 'G')]
    G_la_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Liga')&(total_bokeh['Poste'] == 'G')]
    
    D_l1_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 1')&((total_bokeh['Poste'] == 'DL')|(total_bokeh['Poste'] == 'DC'))]
    D_l2_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 2')&((total_bokeh['Poste'] == 'DL')|(total_bokeh['Poste'] == 'DC'))]
    D_pl_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Premiere League')&((total_bokeh['Poste'] == 'DL')|(total_bokeh['Poste'] == 'DC'))]
    D_sa_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Serie A')&((total_bokeh['Poste'] == 'DL')|(total_bokeh['Poste'] == 'DC'))]
    D_la_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Liga')&((total_bokeh['Poste'] == 'DL')|(total_bokeh['Poste'] == 'DC'))]
    
    M_l1_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 1')&((total_bokeh['Poste'] == 'MD')|(total_bokeh['Poste'] == 'MO'))]
    M_l2_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 2')&((total_bokeh['Poste'] == 'MD')|(total_bokeh['Poste'] == 'MO'))]
    M_pl_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Premiere League')&((total_bokeh['Poste'] == 'MD')|(total_bokeh['Poste'] == 'MO'))]
    M_sa_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Serie A')&((total_bokeh['Poste'] == 'MD')|(total_bokeh['Poste'] == 'MO'))]
    M_la_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Liga')&((total_bokeh['Poste'] == 'MD')|(total_bokeh['Poste'] == 'MO'))]
    
    A_l1_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 1')&(total_bokeh['Poste'] == 'A')]
    A_l2_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Ligue 2')&(total_bokeh['Poste'] == 'A')]
    A_pl_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Premiere League')&(total_bokeh['Poste'] == 'A')]
    A_sa_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Serie A')&(total_bokeh['Poste'] == 'A')]
    A_la_bokeh = total_bokeh[(total_bokeh['Championnat'] == 'Liga')&(total_bokeh['Poste'] == 'A')]
    
    moy_G_l1 = G_l1_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_G_l1 = moy_G_l1.reset_index()
    moy_G_l1['Poste'] = 'Gardiens'
    
    moy_D_l1 = D_l1_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_D_l1 = moy_D_l1.reset_index()
    moy_D_l1['Poste'] = 'Défenseurs'
    
    moy_M_l1 = M_l1_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_M_l1 = moy_M_l1.reset_index()
    moy_M_l1['Poste'] = 'Milieux'
    
    moy_A_l1 = A_l1_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_A_l1 = moy_A_l1.reset_index()
    moy_A_l1['Poste'] = 'Attaquants'
    
    
    moy_G_l2 = G_l2_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_G_l2 = moy_G_l2.reset_index()
    moy_G_l2['Poste'] = 'Gardiens'
    
    moy_D_l2 = D_l2_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_D_l2 = moy_D_l2.reset_index()
    moy_D_l2['Poste'] = 'Défenseurs'
    
    moy_M_l2 = M_l2_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_M_l2 = moy_M_l2.reset_index()
    moy_M_l2['Poste'] = 'Milieux'
    
    moy_A_l2 = A_l2_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_A_l2 = moy_A_l2.reset_index()
    moy_A_l2['Poste'] = 'Attaquants'
    
    
    moy_G_pl = G_pl_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_G_pl = moy_G_pl.reset_index()
    moy_G_pl['Poste'] = 'Gardiens'
    
    moy_D_pl = D_pl_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_D_pl = moy_D_pl.reset_index()
    moy_D_pl['Poste'] = 'Défenseurs'
    
    moy_M_pl = M_pl_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_M_pl = moy_M_pl.reset_index()
    moy_M_pl['Poste'] = 'Milieux'
    
    moy_A_pl = A_pl_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_A_pl = moy_A_pl.reset_index()
    moy_A_pl['Poste'] = 'Attaquants'
    
    
    moy_G_sa = G_sa_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_G_sa = moy_G_sa.reset_index()
    moy_G_sa['Poste'] = 'Gardiens'
    
    moy_D_sa = D_sa_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_D_sa = moy_D_sa.reset_index()
    moy_D_sa['Poste'] = 'Défenseurs'
    
    moy_M_sa = M_sa_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_M_sa = moy_M_sa.reset_index()
    moy_M_sa['Poste'] = 'Milieux'
    
    moy_A_sa = A_sa_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_A_sa = moy_A_sa.reset_index()
    moy_A_sa['Poste'] = 'Attaquants'
    
    
    moy_G_la = G_la_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_G_la = moy_G_la.reset_index()
    moy_G_la['Poste'] = 'Gardiens'
    
    moy_D_la = D_la_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_D_la = moy_D_la.reset_index()
    moy_D_la['Poste'] = 'Défenseurs'
    
    moy_M_la = M_la_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_M_la = moy_M_la.reset_index()
    moy_M_la['Poste'] = 'Milieux'
    
    moy_A_la = A_la_bokeh.groupby( by = [ 'Championnat','Club']).mean()
    moy_A_la = moy_A_la.reset_index()
    moy_A_la['Poste'] = 'Attaquants'
    
    l1_bokeh = pd.concat([moy_G_l1, moy_D_l1, moy_M_l1, moy_A_l1], axis = 0)
    l2_bokeh = pd.concat([moy_G_l2, moy_D_l2, moy_M_l2, moy_A_l2], axis = 0)
    pl_bokeh = pd.concat([moy_G_pl, moy_D_pl, moy_M_pl, moy_A_pl], axis = 0)
    sa_bokeh = pd.concat([moy_G_sa, moy_D_sa, moy_M_sa, moy_A_sa], axis = 0)
    la_bokeh = pd.concat([moy_G_la, moy_D_la, moy_M_la, moy_A_la], axis = 0)


    colors = ['#b55d60', '#5F9E6E', '#8d7866', '#5975A4']
    valeurs = ['Gardiens','Défenseurs','Milieux', 'Attaquants']
    poste_order = {'Gardiens': 0, 'Défenseurs': 1, 'Milieux': 2, 'Attaquants': 3}
    tooltips=[('Club, Poste', '@x'), ('Note', '@top')]
    
    modalite_l1 = l1_bokeh['Club'].unique().tolist()
    modalite_l1 = sorted(modalite_l1)
    valeurs = ['Gardiens','Défenseurs','Milieux', 'Attaquants']
    x = [(i, j) for i in modalite_l1 for j in valeurs]
    
    poste_order = {'Gardiens': 0, 'Défenseurs': 1, 'Milieux': 2, 'Attaquants': 3}
    l1_bokeh['Poste_Order'] = l1_bokeh['Poste'].map(poste_order)
    l1_bokeh = l1_bokeh.sort_values(by=['Club', 'Poste_Order'])
    l1_bokeh = l1_bokeh.drop('Poste_Order', axis=1)
    notes_l1 = l1_bokeh['Note']
    
    l1_bokeh = l1_bokeh.reset_index(drop=True)
    
    source_l1 = ColumnDataSource({
        'x' : x,
        'top' : l1_bokeh['Note']})
    
    factor_range = FactorRange(factors=x)
    p_l1 = figure(x_range=factor_range, width=1200, height=500, tooltips = tooltips)
    p_l1.vbar(x='x', top='top', width=0.8, source=source_l1,
              line_color="white",fill_color=factor_cmap('x', palette=colors, factors=valeurs, start=1, end=2))
    
    
    p_l1.xaxis.major_label_orientation = 'vertical'
    p_l1.xaxis.group_label_orientation = 45
    p_l1.y_range.start = 4.5
    p_l1.y_range.end = 6.8
    show(p_l1)
    
    modalite_l2 = l2_bokeh['Club'].unique().tolist()
    modalite_l2 = sorted(modalite_l2)
    
    x = [(i, j) for i in modalite_l2 for j in valeurs]
    
    l2_bokeh['Poste_Order'] = l2_bokeh['Poste'].map(poste_order)
    l2_bokeh = l2_bokeh.sort_values(by=['Club', 'Poste_Order'])
    l2_bokeh = l2_bokeh.drop('Poste_Order', axis=1)
    l2_bokeh = l2_bokeh.reset_index(drop=True)
    
    source_l2 = ColumnDataSource({
        'x' : x,
        'top' : l2_bokeh['Note']})
    
    factor_range = FactorRange(factors=x)
    p_l2 = figure(x_range=factor_range, width=1200, height=500, tooltips = tooltips)
    p_l2.vbar(x='x', top='top', width=0.8, source=source_l2, line_color="white", 
          fill_color=factor_cmap('x', palette=colors, factors=valeurs, start=1, end=2))
    
    p_l2.xaxis.major_label_orientation = 'vertical'
    p_l2.xaxis.group_label_orientation = 45
    p_l2.y_range.start = 3.9
    p_l2.y_range.end = 6.5
    show(p_l2)
    
    modalite_pl = pl_bokeh['Club'].unique().tolist()
    modalite_pl = sorted(modalite_pl)
    
    x = [(i, j) for i in modalite_pl for j in valeurs]
    
    
    pl_bokeh['Poste_Order'] = pl_bokeh['Poste'].map(poste_order)
    pl_bokeh = pl_bokeh.sort_values(by=['Club', 'Poste_Order'])
    pl_bokeh = pl_bokeh.drop('Poste_Order', axis=1)
    notes_pl = pl_bokeh['Note']
    
    pl_bokeh = pl_bokeh.reset_index(drop=True)
    
    source_pl = ColumnDataSource({
        'x' : x,
        'top' : notes_pl})
    
    factor_range = FactorRange(factors=x)
    p_pl = figure(x_range=factor_range, width=1200, height=500, tooltips = tooltips)
    p_pl.vbar(x='x', top='top', width=0.8, source=source_pl, line_color="white",
          fill_color=factor_cmap('x', palette=colors, factors=valeurs, start=1, end=2))
    
    p_pl.xaxis.major_label_orientation = 'vertical'
    p_pl.xaxis.group_label_orientation = 45
    p_pl.y_range.start = 4.2
    p_pl.y_range.end = 6.4
    show(p_pl)
    
    modalite_sa = sa_bokeh['Club'].unique().tolist()
    modalite_sa = sorted(modalite_sa)
    
    x = [(i, j) for i in modalite_sa for j in valeurs]
    
    
    sa_bokeh['Poste_Order'] = sa_bokeh['Poste'].map(poste_order)
    sa_bokeh = sa_bokeh.sort_values(by=['Club', 'Poste_Order'])
    sa_bokeh = sa_bokeh.drop('Poste_Order', axis=1)
    notes_sa = sa_bokeh['Note']
    
    sa_bokeh = sa_bokeh.reset_index(drop=True)
    
    source_sa = ColumnDataSource({
        'x' : x,
        'top' : notes_sa})
    
    factor_range = FactorRange(factors=x)
    p_sa = figure(x_range=factor_range, width=1200, height=500, tooltips = tooltips)
    p_sa.vbar(x='x', top='top', width=0.8, source=source_sa, line_color="white",
          fill_color=factor_cmap('x', palette=colors, factors=valeurs, start=1, end=2))
    
    p_sa.xaxis.major_label_orientation = 'vertical'
    p_sa.xaxis.group_label_orientation = 45
    p_sa.y_range.start = 4.4
    p_sa.y_range.end = 5.8
    show(p_sa)
    
    modalite_la = la_bokeh['Club'].unique().tolist()
    modalite_la = sorted(modalite_la)
    
    x = [(i, j) for i in modalite_la for j in valeurs]
    
    
    la_bokeh['Poste_Order'] = la_bokeh['Poste'].map(poste_order)
    la_bokeh = la_bokeh.sort_values(by=['Club', 'Poste_Order'])
    la_bokeh = la_bokeh.drop('Poste_Order', axis=1)
    notes_la = la_bokeh['Note']
    
    la_bokeh = la_bokeh.reset_index(drop=True)
    
    source_la = ColumnDataSource({
        'x' : x,
        'top' : notes_la})
    
    factor_range = FactorRange(factors=x)
    p_la = figure(x_range=factor_range, width=1200, height=500, tooltips = tooltips)
    p_la.vbar(x='x', top='top', width=0.8, source=source_la, line_color="white",
          fill_color=factor_cmap('x', palette=colors, factors=valeurs, start=1, end=2))
    
    p_la.xaxis.major_label_orientation = 'vertical'
    p_la.xaxis.group_label_orientation = 45
    p_la.y_range.start = 3.8
    p_la.y_range.end = 6
    show(p_la)
    
    tab_l1 = TabPanel(child=p_l1, title="Ligue 1")
    tab_l2 = TabPanel(child=p_l2, title="Ligue 2")
    tab_pl = TabPanel(child=p_pl, title="Premiere League")
    tab_sa = TabPanel(child=p_sa, title="Seria")
    tab_la = TabPanel(child=p_la, title="Liga")
    bokeh_tab = Tabs(tabs=[tab_l1, tab_l2, tab_pl, tab_sa, tab_la])


    
    
    # In[27]:
    
    
    #total_df.to_csv('../data/DataFrames/total_df')
    #total_j.to_csv('../data/DataFrames/total_j')
    #total.to_csv('../data/DataFrames/total')
    #G_df.to_csv('../data/DataFrames/G_df')
    #G.to_csv('../data/DataFrames/G_stat')
    #G_j.to_csv('../data/DataFrames/G_j')
    #D_df.to_csv('../data/DataFrames/D_df')
    #D.to_csv('../data/DataFrames/D_stat')
    #D_j.to_csv('../data/DataFrames/D_j')
    #M_df.to_csv('../data/DataFrames/M_df')
    #M.to_csv('../data/DataFrames/M_stat')
    #M_j.to_csv('../data/DataFrames/M_j')
    #A_df.to_csv('../data/DataFrames/A_df')
    #A.to_csv('../data/DataFrames/A_stat')
    #A_j.to_csv('../data/DataFrames/A_j')

