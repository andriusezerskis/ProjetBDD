"""
Projet de BDD : réaliser une base de données en SQL.
Date : 26/05/2023
Auteurs : Matias Nieto Navarrete, Andrius Ezerskis, Moïra Vanderslagmolen
Matricules : 502920, 542698, 547486
Section : B-INFO
"""

from MVC.controller import Controller
from MVC.view import MainView

if __name__ == "__main__":
    controller = Controller()
    view = MainView(controller)

    while True:
        view.main_menu()
