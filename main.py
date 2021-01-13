print("main")
from window_controller import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w1 = mainWindowController()  # = QtWidgets.QMainWindow()
    w1.show()  # MainWindow.show()
    app.exec_()
