# -*- coding: utf-8 -*-
from PySide2.QtWidgets import (
    QAbstractItemView,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)
from PySide2.QtCore import Slot, Qt
from motor import estoque_driver
from atualize_pecas import Atualizar_Pecas
from main import Janelas

# from atualize_pecas import *

# Segunda Aba
class Buscador_de_Pecas(QWidget):
    def __init__(self):

        QWidget.__init__(self)
        self.driver = estoque_driver()

        # Widgets:
        self.label_busca = QLabel("Nome ou Código da Peça:")
        self.entry_busca = QLineEdit()

        self.button_busca = QPushButton("&Buscar")
        self.button_busca.clicked.connect(self.buscar)
        self.button_busca.setShortcut("Ctrl+B")

        self.pecas = 0
        self.tabela_pecas = QTableWidget()
        self.tabela_pecas.setColumnCount(4)
        self.tabela_pecas.setHorizontalHeaderLabels(
            ["Código", "Quantidade", "Preço de Compra (R$)", "Preço de Venda (R$)"]
        )
        self.tabela_pecas.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_pecas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_pecas.itemDoubleClicked.connect(self.info)

        # Leiaute:
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_busca, 0, 0, 1, 2, Qt.AlignCenter)
        self.layout.addWidget(self.entry_busca, 1, 0)
        self.layout.addWidget(self.button_busca, 1, 1)
        self.layout.addWidget(self.tabela_pecas, 2, 0, 1, 2)
        self.setLayout(self.layout)

    @Slot()
    def buscar(self):
        self.tabela_pecas.clearContents()
        self.pecas = 0
        peca_buscada = self.entry_busca.text()
        data = self.driver.search(peca_buscada)
        for peca in data:
            code = QTableWidgetItem(peca["code"])
            qty = QTableWidgetItem(str(peca["quantidade"]))
            buy_price = QTableWidgetItem(str(peca["preco_compra"]))
            sell_price = QTableWidgetItem(str(peca["preco_venda"]))
            code.setTextAlignment(Qt.AlignCenter)
            qty.setTextAlignment(Qt.AlignCenter)
            buy_price.setTextAlignment(Qt.AlignCenter)
            sell_price.setTextAlignment(Qt.AlignCenter)
            self.tabela_pecas.insertRow(self.pecas)
            self.tabela_pecas.setItem(self.pecas, 0, code)
            self.tabela_pecas.setItem(self.pecas, 1, qty)
            self.tabela_pecas.setItem(self.pecas, 2, buy_price)
            self.tabela_pecas.setItem(self.pecas, 3, sell_price)
            self.pecas += 1

    @Slot()
    def info(self):
        row = self.tabela_pecas.currentRow()
        col = self.tabela_pecas.currentColumn()
        code = self.tabela_pecas.item(row, 0)
        id = self.driver.get_id(code.text())
        if col == 0:
            data = self.driver.show_info(id)
            texto = "Nome: {0}\nDescrição: {1}".format(data["nome"], data["descricao"])
            popup_info = QMessageBox(QMessageBox.Information, "Busca", "Informações:")
            popup_info.setInformativeText(texto)
            popup_info.addButton(QMessageBox.Ok)
            popup_info.exec()
        else:
            atualizar_quantidade = Atualizar_Pecas(id)
            atualizar_quantidade.setWindowTitle("Atualizar")
            #atualizar_quantidade.setFixedSize(270, 245)
            atualizar_quantidade.exec()
