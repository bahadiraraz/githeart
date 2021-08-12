from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QAbstractButton
from PyQt5.QtGui import QColor, QPainter, QPen
import keyboard


current_color = 0
class GithubTabloItem(QAbstractButton):
    """
    Github Tablo tarzı Widget'ın elemanı

    clicked sinyali başka bir şey için kullanılabilir,
    renk değiştirmek için mouseReleaseEvent kullanılıyor
    """

    renkler = (
        QColor(22, 27, 34),
        QColor(155, 233, 168),
        QColor(64, 196, 99),
        QColor(48, 161, 78),
        QColor(33, 110, 57),
    )
    
    def __init__(self):
        super().__init__()
        self.setMinimumSize(11,11)
        self.setStyleSheet("border: 0px;")
        self.setStyleSheet("border-color: black;")
        self.setCursor(Qt.PointingHandCursor)
        self.renk = 0

    def mouseReleaseEvent(self, event):
        self.renk += 1
        if self.renk > len(self.renkler) - 1:
            self.renk = 0

        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
     
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(self.renkler[self.renk])
        painter.drawRect(0, 0, self.width()-1, self.height()-1)

        painter.end()

    def keyPressEvent(self, event):
        global current_color
        if event.key() == Qt.Key_1:
            print(current_color)
            current_color = 0
          
        elif event.key() == Qt.Key_2:
            print(current_color)
            current_color = 1
         
        elif event.key() == Qt.Key_3:
            print(current_color)
            current_color = 2
        
        elif event.key() == Qt.Key_4:
            print(current_color)
            current_color = 3
           
        elif event.key() == Qt.Key_5:
            print(current_color)
            current_color = 4
  
            
        self.update()
    
    def mousePressEvent(self, event):
        global current_color
        current_color = (self.renk +1) % 4
        self.update()

    def enterEvent(self, event):
   
        global current_color
        print(current_color)
        self.renk = current_color



    
        
    

class GithubTablo(QWidget):
    """
    Github Tablo tarzı Widget

    parent  ->  Parent widget
    cols    ->  Sütun sayısı (int)
    rows    ->  Satır sayısı (int)
    """
    def __init__(self, parent, cols, rows):
        super().__init__(parent)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setSpacing(3)
        for y in range(rows):
            for x in range(cols):
                self.layout.addWidget(GithubTabloItem(), x, y, alignment=Qt.AlignCenter)



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

   

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.githubtablo = GithubTablo(self, 7, 50)
        self.layout.addWidget(self.githubtablo)


        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(13, 17, 23))
        self.setPalette(p)
        
        self.setWindowTitle("Github Tablo")



if __name__ == "__main__":
    app = QApplication([])

    mw = MainWindow()
    mw.show()

    app.exec_()


