from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
	QApplication,
	QComboBox,
	QHBoxLayout,
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

themeType = "default"
themeList = ["Default","Red","Blue","Pink"]

class GithubTabloItem(QAbstractButton):
	colors = {
		"default":(
		QColor("#161b22"),
		QColor("#0e4429"),
		QColor("#006d32"),
		QColor("#26a641"),
		QColor("#39d353")),
		"red":(
		QColor("#161b22"),
		QColor("#440e0e"),
		QColor("#6d0000"),
		QColor("#a62626"),
		QColor("#d33939")),
		"blue":(
		QColor("#161b22"),
		QColor("#0e4444"),
		QColor("#006d6d"),
		QColor("#26a4a6"),
		QColor("#39d0d3")),
		"pink":(
		QColor("#161b22"),
		QColor("#440e3f"),
		QColor("#6d0060"),
		QColor("#a62699"),
		QColor("#d339ce"))
	}

	def __init__(self, parent):
		global current_color
		QAbstractButton.__init__(self)
		self.parent = parent
		self.setMinimumSize(13, 13)
		self.setCursor(Qt.PointingHandCursor)
		self.color = current_color

	def paintEvent(self, event):
		global control
		self.color = self.color % 5
		painter = QPainter()
		painter.begin(self)
		painter.setPen(QPen(Qt.black, 1))
		painter.setBrush(self.colors[themeType][self.color])
		painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
		painter.end()
		control = 0

	def mouseReleaseEvent(self, event):
		print(event.buttons())
		global control, current_color, flag
		if event.button() == Qt.LeftButton:
			self.color += 1
			self.color = self.color % 5
			current_color = self.color
			self.update()
			self.parent.current_color_info.emit(current_color +1)
			control = 0
		else:
			self.color -= 1
			self.color = self.color % 5
			current_color = self.color
			self.update()
			self.parent.current_color_info.emit(current_color + 1)
			control = 0

	def enterEvent(self, event):
		global current_color, flag
		if flag:
			self.color = current_color
			self.update()
	
	def set_color(self, color):
		self.color = self.color % 5
		self.color = color
		print(color)
		self.update()

class GithubTablo(QWidget):
	def __init__(self, parent, cols, rows):
		super().__init__(parent)
		self.layout = QGridLayout()
		self.layout.setContentsMargins(0,0,0,0)
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
		self.mainLayout = QVBoxLayout()
		self.setLayout(self.mainLayout)

		self.githubtablo = GithubTablo(self, global_x, global_y)
		self.mainLayout.addWidget(self.githubtablo)
		self.layout = QHBoxLayout()
		self.layout.setAlignment(Qt.AlignLeft)
		
		self.mainLayout.addLayout(self.layout)

		palet = self.palette()
		palet.setColor(self.backgroundRole(), QColor(13, 17, 23))
		self.setPalette(palet)
		self.current_color_label = QLabel()
		self.current_color_label.setText("1")
		self.current_color_label.setFont(QFont("ariel", 10))
		self.current_color_label.setStyleSheet("color: rgb(255,255,255);")
		self.current_color_info.emit(current_color +1)
		self.current_color_info.connect(
			lambda data: self.current_color_label.setText(str(data))
		)

		#box showing the currently used color
		self.current_color_box = GithubTablo(self,1,1)
		self.current_color_box.setStyleSheet("background-color: rgb(255,255,255);")

		#print currnet_color_box color
		self.current_color_info.connect(lambda data: self.current_color_box.layout.itemAt(0).widget().set_color(data-1))
		self.current_color_box.setDisabled(True)
		#self.current_color_info.connect(lambda x : self.current_color_box.layout.widget().color)




		self.themeText = QLabel("Choose Color Theme:")
		self.themeText.setFont(QFont("ariel", 8))
		self.themeText.setStyleSheet("color: rgb(255,255,255);")

		self.themeComboBox = QComboBox()
		self.themeComboBox.setStyleSheet("""
		QComboBox{
		background-color:rgb(26, 34, 46);
		color:rgb(255, 255, 255);
		border:hidden;}
		QComboBox QAbstractItemView {
		background-color:rgb(26, 34, 46);
		color:rgb(255, 255, 255);
		}
		""")
		self.themeComboBox.activated.connect(self.changeTheme)
		self.themeComboBox.setFixedWidth(int(self.width()*0.3))
		self.themeComboBox.addItems(themeList)


		keyboard.add_hotkey("p", self.print_colors)
		keyboard.add_hotkey("c", self.clear_colors)



		self.layout.addWidget(self.current_color_box)
		self.layout.addWidget(self.current_color_label)
		self.layout.addSpacing(int(self.width()*0.7))
		self.layout.addWidget(self.themeText)
		self.layout.addWidget(self.themeComboBox)
		

	def changeTheme(self):
		global themeType
		themeType = self.themeComboBox.currentText().lower()
		self.current_color_info.emit(current_color+1)
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
					g.append(self.githubtablo.layout.itemAtPosition(x, y).widget().color)
			g = np.matrix(g).reshape(global_y, global_x).T.tolist()
			control += 1
			print(*g, sep="\12")

	def clear_colors(self):
		for y in range(global_y):
			for x in range(global_x):
				self.githubtablo.layout.itemAtPosition(x, y).widget().color = 0
				self.githubtablo.layout.itemAtPosition(x, y).widget().update()


if __name__ == "__main__":
	app = QApplication([])
	mw = MainWindow()
	mw.show()
	app.exec_()
