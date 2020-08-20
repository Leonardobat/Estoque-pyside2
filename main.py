# -*- coding: utf-8 -*-
import sys
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QMdiArea,
    QMainWindow,
    QMenuBar,
    QAction,
    QStatusBar,
    QMessageBox,
    QApplication,
    QLabel,
    QTabWidget,
)
from novas_pecas import Novas_Pecas
from busca_pecas import Buscador_de_Pecas

class Janelas(QMdiArea):
    def __init__(self):  # Inicialização da Janela
        QMdiArea.__init__(self)
        window1 = self.addSubWindow(Buscador_de_Pecas())
        window2 = self.addSubWindow(Novas_Pecas())
        window1.setWindowTitle("Busque por Peças")
        window2.setWindowTitle("Novas Peças")
        self.setViewMode(QMdiArea.TabbedView)
        self.setActiveSubWindow(window1)
        self.setTabsClosable(False)

class Principal(QMainWindow):
    def __init__(self, widget):
        QMainWindow.__init__(self)
        self.setWindowTitle("Tião Automecânica")
        self.setCentralWidget(widget)
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
    widget = Janelas()
    window = Principal(widget)
    #window.resize(900, 600)
    window.showMaximized()
    sys.exit(app.exec_())
