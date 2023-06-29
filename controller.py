from view import View
from model import API

class Controller:
    def __init__(self, API):
        self.view = View()
        self.API = API
    
    def inicio(self):
        opcao = self.view.inicio()

        while opcao != 2:
            if opcao == 1:
                API.get_consulta();
            opcao = self.view.menu()

if __name__ == "__main__":
    API = API()
    main = Controller(API)
    main.inicio()