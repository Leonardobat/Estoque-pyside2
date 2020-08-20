# -*- coding: utf-8 -*-
import sys
from PySide2.QtCore import Slot, Signal
from PySide2.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QAction,
    QStatusBar,
    QMessageBox,
    QApplication,
    QLabel,
    QGridLayout,
    QWidget,
)
from novas_pecas import Novas_Pecas
from busca_pecas import Buscador_de_Pecas

class Principal(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tião Automecânica")
        self.widget = QWidget()
        w1, w2 = Novas_Pecas(), Buscador_de_Pecas()
        w1.setMaximumWidth(350)
        self.layout = QGridLayout()
        self.layout.addWidget(w1, 0, 0, 1, 1)
        self.layout.addWidget(w2, 0, 2, 1, 2)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        self.sobre = QAction("Sobre", self)
        self.sobre.setShortcut("F1")
        self.menu.addAction(self.sobre)
        self.sobre.triggered.connect(self.info)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        global status
        status = QLabel("Pronto")
        self.status.addWidget(status)

    @Slot()
    def info(self):
        self.popup = QMessageBox(QMessageBox.Information, "Sobre", "Informações")
        self.popup.setInformativeText(
            """Suite de Apoio \nVersão 0.3
        \nFeito com S2 por Zero \nMIT License"""
        )
        self.popup.addButton(QMessageBox.Ok)
        self.popup.exec()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Principal()
    window.showMaximized()
    sys.exit(app.exec_())
