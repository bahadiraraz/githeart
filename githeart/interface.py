from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QAbstractButton, QLabel
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
import keyboard
import numpy as np

current_color = 0
flag = True

control = 0


class GithubTabloItem(QAbstractButton):
	"""
	Github Tablo tarzı Widget'ın elemanı

	clicked sinyali başka bir şey için kullanılabilir,
	renk değiştirmek için mouseReleaseEvent kullanılıyor
	"""
	renkler = (
		QColor("#161b22"),
		QColor("#0e4429"),
		QColor("#006d32"),
		QColor("#26a641"),
		QColor("#39d353"),
	)

	def __init__(self, parent):
		self.parent = parent
		global current_color
		QAbstractButton.__init__(self)
		self.setMinimumSize(13, 13)
		self.setStyleSheet("border: 0px;")
		self.setStyleSheet("border-color: black;")
		self.setCursor(Qt.PointingHandCursor)
		self.renk = current_color

	def paintEvent(self, event):
		global control
		painter = QPainter()
		painter.begin(self)
		painter.setPen(QPen(Qt.black, 1))
		painter.setBrush(self.renkler[self.renk])
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		painter.end()
		control = 0

	def mouseReleaseEvent(self, event):
		global control
		global current_color
		global flag
		self.renk += 1
		self.renk = self.renk % 5
		current_color = self.renk
		self.update()
		self.parent.current_color_info.emit(current_color)
		control = 0
		

	def enterEvent(self, event):
		global flag
		global current_color
		print(flag)
		if flag:
			self.renk = current_color
			self.update()


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
		self.layout.setSpacing(1)
		for y in range(rows):
			for x in range(cols):
				self.layout.addWidget(GithubTabloItem(parent), x, y, alignment=Qt.AlignCenter)


class MainWindow(QWidget, QThread):
	current_color_info = pyqtSignal(int)

	def __init__(self):
		QThread.__init__(self)
		QWidget.__init__(self)

		self.layout = QVBoxLayout()
		self.setLayout(self.layout)
		self.githubtablo = GithubTablo(self, 7, 50)
		self.layout.addWidget(self.githubtablo)
		p = self.palette()
		p.setColor(self.backgroundRole(), QColor(13, 17, 23))
		self.setPalette(p)

		self.setWindowTitle("Github Tablo")

		def clear_colors():
			for y in range(50):
				for x in range(7):
					self.githubtablo.layout.itemAtPosition(x, y).widget().renk = 0
					self.githubtablo.layout.itemAtPosition(x, y).widget().update()

		self.current_color_label = QLabel()
		self.current_color_label.setText("0")
		self.current_color_label.setAlignment(Qt.AlignCenter)
		self.current_color_label.setFont(QFont("ariel", 20))
		self.current_color_label.setStyleSheet("color: rgb(255,255,255);")
		self.current_color_info.emit(current_color)
		self.current_color_info.connect(lambda data: self.current_color_label.setText(str(data)))
		self.layout.addWidget(self.current_color_label)
		keyboard.add_hotkey('c', clear_colors)
		keyboard.add_hotkey('p', self.print_colors)

	def keyPressEvent(self, event):
		global current_color
		global flag
		if event.key() == Qt.Key_1:
			current_color = 0
			flag = True
		elif event.key() == Qt.Key_2:
			current_color = 1
			flag = True
		elif event.key() == Qt.Key_3:
			current_color = 2
			flag = True
		elif event.key() == Qt.Key_4:
			current_color = 3
			flag = True
		elif event.key() == Qt.Key_5:
			current_color = 4
			flag = True
		elif event.key() == Qt.Key_Escape:
			if flag:
				flag = False
			else:
				flag = True
			print("escape")

		self.current_color_info.emit(current_color)

	def print_colors(self):
		global control
		if control < 1:

			g = []
			for y in range(50):
				for x in range(7):
					g.append(self.githubtablo.layout.itemAtPosition(x, y).widget().renk)

			g = np.matrix(g).reshape(50, 7).T.tolist()
			print(*g, sep="\n")
			print()
			control += 1

if __name__ == "__main__":
	app = QApplication([])
	mw = MainWindow()
	mw.show()
	app.exec_()
