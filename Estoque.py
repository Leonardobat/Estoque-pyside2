# -*- coding: utf-8 -*-
import sys
from PySide6.QtCore import Slot, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMainWindow,
    QMenuBar,
    QStatusBar,
    QMessageBox,
    QApplication,
    QLabel,
    QGridLayout,
    QWidget,
    QFrame,
    QSizePolicy,
)
from DB import init_db
from Gui import NovasPeças, BuscadorDePeças


class Principal(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.inicializar_db()
        self.setWindowTitle("Tião Automecânica - Vendas")
        self.widget = QWidget()

        # Janelas
        w1, w2 = NovasPeças(), BuscadorDePeças()
        w2_size_policy = QSizePolicy(QSizePolicy.Preferred,
                                     QSizePolicy.Preferred)
        w2_size_policy.setHorizontalStretch(2)
        w2.setSizePolicy(w2_size_policy)
        w1.update_signal.connect(w2.buscar)
        w2.selected_cell_info.connect(w1.mode_atualizar)
        w1.status_signal.connect(self.atualizar_status)
        w2.status_signal.connect(self.atualizar_status)

        # Leiaute
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(1)
        self.layout = QGridLayout()
        self.layout.addWidget(w1, 0, 0, 1, 1)
        self.layout.addWidget(self.line, 0, 1, 1, 1)
        self.layout.addWidget(w2, 0, 2, 1, 2)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Menu
        self.menu = QMenuBar()
        self.setMenuBar(self.menu)
        self.sobre = QAction("Sobre", self)
        self.sobre.setShortcut("F1")
        self.menu.addAction(self.sobre)
        self.sobre.triggered.connect(self.info)

        # Status
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status_label = QLabel("Pronto")
        self.status.addWidget(self.status_label)

    @Slot()
    def info(self):
        self.popup = QMessageBox(QMessageBox.Information, "Sobre",
                                 "Informações")
        self.popup.setInformativeText("""Suite de Apoio \nVersão 0.4
        \nFeito com S2 por Zero \nMIT License""")
        self.popup.addButton(QMessageBox.Ok)
        self.popup.exec()

    @Slot()
    def atualizar_status(self, msg: str):
        self.status_label.setText(msg)

    @staticmethod
    def inicializar_db():
        try:
            init_db()
        except ValueError:
            popup = QMessageBox(QMessageBox.Critical, "Erro", "Erro")
            popup.setInformativeText(
                "Arquivo de configuração não foi encontrado")
            popup.addButton(QMessageBox.Ok)
            popup.exec()
            exit(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Principal()
    window.showMaximized()
    sys.exit(app.exec_())
