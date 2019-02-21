from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore


widget = QtWidgets.QWidget()
checkbox = QtWidgets.QCheckBox("Check me", parent = widget)
bar = QtWidgets.QTabWidget(parent = widget)
bar.resize(220,220)
button = QtWidgets.QPushButton("Push Me", parent = widget)
button.move(30,40)
widget.resize(300,400)
widget.show()
widget.raise_()