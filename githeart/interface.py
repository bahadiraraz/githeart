from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
	QApplication,
	QWidget,
	QVBoxLayout,
	QGridLayout,
	QAbstractButton,
	QLabel,
)
from PyQt5.QtGui import QColor, QPainter, QPen, QFont
import keyboard
import numpy as np

current_color = 0
control = 0
flag = True
global_x = 7
global_y = 53

class GithubTabloItem(QAbstractButton):
	renkler = (
		QColor("#161b22"),
		QColor("#0e4429"),
		QColor("#006d32"),
		QColor("#26a641"),
		QColor("#39d353"),
	)

	def __init__(self, parent):
		global current_color
		QAbstractButton.__init__(self)
		self.parent = parent
		self.setMinimumSize(13, 13)
		self.setCursor(Qt.PointingHandCursor)
		self.renk = current_color

	def paintEvent(self, event):
		global control
		self.renk = self.renk % 5
		painter = QPainter()
		painter.begin(self)
		painter.setPen(QPen(Qt.black, 1))
		painter.setBrush(self.renkler[self.renk])
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		painter.end()
		control = 0

	def mouseReleaseEvent(self, event):
		print(event.buttons())
		global control, current_color, flag
		if event.button() == Qt.LeftButton:
			self.renk += 1
			self.renk = self.renk % 5
			current_color = self.renk
			self.update()
			self.parent.current_color_info.emit(current_color +1)
			control = 0
		else:
			self.renk -= 1
			self.renk = self.renk % 5
			current_color = self.renk
			self.update()
			self.parent.current_color_info.emit(current_color + 1)
			control = 0

	def enterEvent(self, event):
		global current_color, flag
		if flag:
			self.renk = current_color
			self.update()
	
	def set_color(self, color):
		self.renk = self.renk % 5
		self.renk = color
		print(color)
		self.update()

class GithubTablo(QWidget):
	def __init__(self, parent, cols, rows):
		super().__init__(parent)
		self.layout = QGridLayout()
		self.setLayout(self.layout)
		self.layout.setSpacing(1)
		for y in range(rows):
			for x in range(cols):
				self.layout.addWidget(
					GithubTabloItem(parent), x, y, alignment=Qt.AlignCenter
				)


class MainWindow(QWidget, QThread):
	global global_x,global_y
	current_color_info = pyqtSignal(int)
	def __init__(self):
		QThread.__init__(self)
		QWidget.__init__(self)
		self.setWindowTitle("Github Tablo")
		self.layout = QVBoxLayout()
		self.setLayout(self.layout)

		self.githubtablo = GithubTablo(self, global_x, global_y)
		self.layout.addWidget(self.githubtablo)
		palet = self.palette()
		palet.setColor(self.backgroundRole(), QColor(13, 17, 23))
		self.setPalette(palet)
		self.current_color_label = QLabel()
		self.current_color_label.setText("1")
		self.current_color_label.setAlignment(Qt.AlignCenter)
		self.current_color_label.setFont(QFont("ariel", 20))
		self.current_color_label.setStyleSheet("color: rgb(255,255,255);")
		self.current_color_info.emit(current_color +1)
		self.current_color_info.connect(
			lambda data: self.current_color_label.setText(str(data))
		)

		#box showing the currently used color
		self.current_color_box = GithubTablo(self,1,1)
		self.current_color_box.setStyleSheet("background-color: rgb(255,255,255);")
		self.layout.addWidget(self.current_color_box)

		#print currnet_color_box color
		self.current_color_info.connect(lambda data: self.current_color_box.layout.itemAt(0).widget().set_color(data-1))
		self.current_color_box.setDisabled(True)
		#self.current_color_info.connect(lambda x : self.current_color_box.layout.widget().renk)

		self.layout.addWidget(self.current_color_label)
		keyboard.add_hotkey("p", self.print_colors)
		keyboard.add_hotkey("c", self.clear_colors)

	def keyPressEvent(self, event):
		global current_color, flag
		if event.key() == Qt.Key_1:
			current_color = 0
		elif event.key() == Qt.Key_2:
			current_color = 1
		elif event.key() == Qt.Key_3:
			current_color = 2
		elif event.key() == Qt.Key_4:
			current_color = 3
		elif event.key() == Qt.Key_5:
			current_color = 4
		elif event.key() == Qt.Key_E:
			print("escape")
			if flag:
				flag = False
			else:
				flag = True

		self.current_color_info.emit(current_color+1)


	def print_colors(self):
		global control
		if control < 1:
			g = list()
			for y in range(global_y):
				for x in range(global_x):
					g.append(self.githubtablo.layout.itemAtPosition(x, y).widget().renk)
			g = np.matrix(g).reshape(global_y, global_x).T.tolist()
			control += 1
			print(*g, sep="\12")

	def clear_colors(self):
		for y in range(global_y):
			for x in range(global_x):
				self.githubtablo.layout.itemAtPosition(x, y).widget().renk = 0
				self.githubtablo.layout.itemAtPosition(x, y).widget().update()


if __name__ == "__main__":
	app = QApplication([])
	mw = MainWindow()
	mw.show()
	app.exec_()
