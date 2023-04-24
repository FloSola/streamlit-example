# Core Pkg
import streamlit as st

# Custom modules
from Présentation import Présentation
from Dataviz import Dataviz 
from Modelisation import Modelisation
from Formation import Formation

def main():

    # List of pages
    liste_menu = ["Présentation", "Dataviz", "Modélisation", "Formation"]

    # Sidebar
    menu = st.sidebar.radio("Menu", liste_menu)
    
    # Page navigation
    if menu == liste_menu[0]:
        Présentation()
    else:
        #Projet_MPG()             
        if menu == liste_menu[1]:
            Dataviz()
        else:
            if menu == liste_menu[2]:
                Modelisation()
            else:
                Formation()
    

if __name__ == '__main__':
    main()