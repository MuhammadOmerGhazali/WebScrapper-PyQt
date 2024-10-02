from PyQt5.QtWidgets import *

def main():
    app = QApplication([])
    window = QWidget()
    
    label = QLabel()
    label.setText("This is yo mama")
    
    
    
    window.show()
    app.exec_()    
    
    
    
    
if __name__ == '__main__':
    main()