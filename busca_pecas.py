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
from PySide2.QtCore import Slot, Qt, Signal
from PySide2.QtGui import QBrush, QColor
from motor import estoque_driver
from novas_pecas import Novas_Pecas


# Segunda Aba
class Buscador_de_Pecas(QWidget):
    selected_cell_info = Signal(dict)
    status_signal = Signal(str)

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
        self.tabela_pecas.setColumnCount(5)
        self.tabela_pecas.setHorizontalHeaderLabels([
            "Código",
            "Nome",
            "Quantidade",
            "Preço de Compra (R$)",
            "Preço de Venda (R$)",
        ])
        self.tabela_pecas.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents)
        self.tabela_pecas.horizontalHeader().setStretchLastSection(True)
        self.tabela_pecas.resizeColumnsToContents()
        self.tabela_pecas.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_pecas.itemDoubleClicked.connect(self.info)
        self.yellow_brush = QBrush(QColor(255, 255, 0, 191))
        self.red_brush = QBrush(QColor(255, 0, 0, 191))

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
        self.tabela_pecas.setRowCount(0)
        self.pecas = 0
        peca_buscada = self.entry_busca.text().upper()
        data = self.driver.search(peca_buscada)
        for peca in data:
            code = QTableWidgetItem(peca["code"])
            name = QTableWidgetItem(peca["nome"])
            qty = QTableWidgetItem(str(peca["quantidade"]))
            buy_price = QTableWidgetItem(str(peca["preco_compra"]))
            sell_price = QTableWidgetItem(str(peca["preco_venda"]))
            code.setTextAlignment(Qt.AlignCenter)
            name.setTextAlignment(Qt.AlignCenter)
            qty.setTextAlignment(Qt.AlignCenter)
            buy_price.setTextAlignment(Qt.AlignCenter)
            sell_price.setTextAlignment(Qt.AlignCenter)
            if peca["quantidade"] < 5 and peca["preco_compra"] < 100:
                qty.setBackground(self.yellow_brush)
                code.setBackground(self.yellow_brush)
                name.setBackground(self.yellow_brush)
                buy_price.setBackground(self.yellow_brush)
                sell_price.setBackground(self.yellow_brush)
            elif peca["quantidade"] == 0:
                qty.setBackground(self.red_brush)
                code.setBackground(self.red_brush)
                name.setBackground(self.red_brush)
                buy_price.setBackground(self.red_brush)
                sell_price.setBackground(self.red_brush)
            self.tabela_pecas.insertRow(self.pecas)
            self.tabela_pecas.setItem(self.pecas, 0, code)
            self.tabela_pecas.setItem(self.pecas, 1, name)
            self.tabela_pecas.setItem(self.pecas, 2, qty)
            self.tabela_pecas.setItem(self.pecas, 3, buy_price)
            self.tabela_pecas.setItem(self.pecas, 4, sell_price)
            self.pecas += 1

    @Slot()
    def info(self):
        row = self.tabela_pecas.currentRow()
        col = self.tabela_pecas.currentColumn()
        code = self.tabela_pecas.item(row, 0)
        id = self.driver.get_id(code.text())
        if col == 0 or col == 1:
            data = self.driver.show_info(id)
            texto = "Nome: {}\nDescrição: {}\nVendas (7 d): {}\nCompras (7 d): {}".format(
                data["nome"], data["descricao"], data["sell_delta"],
                data["buy_delta"])
            popup_info = QMessageBox(QMessageBox.Information, "Busca",
                                     "Informações:")
            popup_info.setInformativeText(texto)
            popup_info.addButton(QMessageBox.Ok)
            popup_info.exec()
            self.status_signal.emit("Feito")
        else:
            self.selected_cell_info.emit(id)
