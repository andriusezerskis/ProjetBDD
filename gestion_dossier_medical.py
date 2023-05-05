
from controller import Controller
from view import MainView

if __name__ == "__main__":
    controller = Controller()
    view = MainView(controller)

    while True:
        view.main_menu()
