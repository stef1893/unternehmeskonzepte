import sys
import random
import os
import PySide6
import subprocess

dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide6 import QtCore, QtWidgets, QtGui

from functions import *

class Hauptfenster(QtWidgets.QWidget):
    def __init__(self, parent=None, typ:str="", path:str=""):
        super(Hauptfenster, self,).__init__()
        self.setStyleSheet(open('stylesheet.css').read())
        self.typ = typ
        self.path = path


class Start(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(open('stylesheet.css').read())

        self.bt_cam = QtWidgets.QPushButton("Kamera")
        self.bt_pic = QtWidgets.QPushButton("Bild")
        self.bt_pdf = QtWidgets.QPushButton("PDF")

        self.layout = QtWidgets.QVBoxLayout(self)
        #self.layout.addWidget(self.text)
        self.layout.addWidget(self.bt_cam)
        self.layout.addWidget(self.bt_pic)
        self.layout.addWidget(self.bt_pdf)

        self.bt_cam.clicked.connect(self.cam)
        self.bt_pic.clicked.connect(self.pic)
        self.bt_pdf.clicked.connect(self.pdf)

    @QtCore.Slot()
    def cam(self):
        self.text.setText(random.choice(self.hello))

    def pic(self):
        index_1 = 0
        index_2 = 0
        index_3 = 0
        self.textviews_names = []
        self.textviews_values = []
        self.controls = []

        dialog = QtWidgets.QFileDialog(self)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()

        self.dialog2 = Hauptfenster(self, "pic", fileNames[0])

        licha, parameter = get_Charge_by_img(fileNames[0])


        self.textviews_names.append(QtWidgets.QLineEdit())
        self.textviews_values.append(QtWidgets.QLineEdit())
        for x in parameter:
            self.textviews_names.append(QtWidgets.QLineEdit())
            self.textviews_values.append(QtWidgets.QLineEdit())

        for y in self.textviews_names:
            if index_1 == 0:
                y.setText("Licha")
                index_1 = index_1 + 1
            else:
                y.setText(parameter[index_1-1].name)
                index_1 = index_1 + 1

        for v in self.textviews_values:
            if index_2 == 0:
                v.setText(licha)
                index_2 = index_2 + 1
            else:
                v.setText(parameter[index_2-1].messwert)
                index_2 = index_2 + 1

        self.layout_form = QtWidgets.QFormLayout()
        for z in self.textviews_names:
            self.layout_form.addRow(z, self.textviews_values[index_3])
            index_3 = index_3 + 1

        self.bt_addLine = QtWidgets.QPushButton('Zeile hinzufügen', self)
        self.bt_addLine.clicked.connect(self.add_line)
        self.bt_deleteLine = QtWidgets.QPushButton('Zeile entfernen', self)
        self.bt_deleteLine.clicked.connect(self.delete_line)
        self.bt_send = QtWidgets.QPushButton('Senden', self)
        self.bt_send.clicked.connect(self.send)

        self.final_layout = QtWidgets.QVBoxLayout(self.dialog2)
        self.final_layout.addLayout(self.layout_form)
        self.final_layout.addWidget(self.bt_addLine)
        self.final_layout.addWidget(self.bt_deleteLine)
        self.final_layout.addWidget(self.bt_send)

        self.dialog2.resize(800,600)
        self.dialog2.show()

    def pdf(self):
        index_1 = 0
        index_2 = 0
        index_3 = 0
        self.textviews_names = []
        self.textviews_values = []
        self.controls = []

        dialog = QtWidgets.QFileDialog(self)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()

        self.dialog2 = Hauptfenster(self, "pdf", fileNames[0])

        licha, parameter = get_charge_by_pdf(fileNames[0])


        self.textviews_names.append(QtWidgets.QLineEdit())
        self.textviews_values.append(QtWidgets.QLineEdit())
        for x in parameter:
            self.textviews_names.append(QtWidgets.QLineEdit())
            self.textviews_values.append(QtWidgets.QLineEdit())

        for y in self.textviews_names:
            if index_1 == 0:
                y.setText("Licha")
                index_1 = index_1 + 1
            else:
                y.setText(parameter[index_1-1].name)
                index_1 = index_1 + 1

        for v in self.textviews_values:
            if index_2 == 0:
                v.setText(licha)
                index_2 = index_2 + 1
            else:
                v.setText(parameter[index_2-1].messwert)
                index_2 = index_2 + 1

        self.layout_form = QtWidgets.QFormLayout()
        for z in self.textviews_names:
            self.layout_form.addRow(z, self.textviews_values[index_3])
            index_3 = index_3 + 1

        self.bt_addLine = QtWidgets.QPushButton('Zeile hinzufügen', self)
        self.bt_addLine.clicked.connect(self.add_line)
        self.bt_deleteLine = QtWidgets.QPushButton('Zeile entfernen', self)
        self.bt_deleteLine.clicked.connect(self.delete_line)
        self.bt_send = QtWidgets.QPushButton('Senden', self)
        self.bt_send.clicked.connect(self.send)

        self.final_layout = QtWidgets.QVBoxLayout(self.dialog2)
        self.final_layout.addLayout(self.layout_form)
        self.final_layout.addWidget(self.bt_addLine)
        self.final_layout.addWidget(self.bt_deleteLine)
        self.final_layout.addWidget(self.bt_send)

        self.dialog2.resize(800,600)
        self.dialog2.show()

    def add_line(self):
        edit = [QtWidgets.QLineEdit(), QtWidgets.QLineEdit()]
        self.controls.append(edit)
        self.layout_form.addRow(edit[0], edit[1])

    def delete_line(self):
        if len(self.controls) > 0:
            edit = self.controls.pop()
            self.layout_form.removeRow(edit[0])

    def send(self):
        parameter: Parameter = []
        index_1 = 0
        index_2 = 0
        licha = ""

        for x in self.textviews_names:
            if index_1 == 0:
                licha = self.textviews_values[index_1].text()
                index_1 = index_1 +1
            else:
                parameter.append(Parameter(x.text(), self.textviews_values[index_1].text()))
                index_1 = index_1 + 1

        if len(self.controls) > 0:
            for y in self.controls:
                parameter.append(Parameter(y[0].text(), y[1].text()))

        message = get_message(licha, parameter)
        print(message)

        connectMqtt(message)
        #publish(client, message)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Start()
    widget.resize(300,400)
    widget.show()

    sys.exit(app.exec_())