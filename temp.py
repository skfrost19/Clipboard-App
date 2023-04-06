import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLineEdit, QMenuBar

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create a QLineEdit for the search bar
        search_edit = QLineEdit()
        
        # add the search bar to the menu bar
        menu_bar = QMenuBar()
        search_action = QAction('Search', self)
        search_action.setCheckable(True)
        search_action.setChecked(False) 
        search_action.triggered.connect(lambda: self.toggle_search_bar(search_action, search_edit))
        menu_bar.addAction(search_action)
        self.setMenuBar(menu_bar)
        

        # set the window properties
        self.setWindowTitle('Search Bar Example')
        self.setGeometry(100, 100, 300, 200)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
