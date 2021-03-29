# -*- coding: utf-8 -*-
from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QGridLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QBrush, QColor
from DB import EstoqueDB


# Primeira Aba
class NovasPeças(QWidget):
    update_signal = Signal()
    status_signal = Signal(str)

    def __init__(self):  # Inicialização da Janela
        QWidget.__init__(self)
        self.driver = EstoqueDB()

        # Label:
        self.label_nome = QLabel("Nome da Nova Peça:")
        self.label_code = QLabel("Código:")
        self.label_quantidade = QLabel("Quantidade:")
        self.label_preco_compra = QLabel("Preço de Compra:")
        self.label_preco_venda = QLabel("Preço de Venda:")
        self.label_descricao = QLabel("Descrição:")

        # Entradas:
        self.entry_nome = QLineEdit()
        self.entry_code = QLineEdit()
        self.entry_quantidade = QSpinBox()
        self.entry_preco_compra = QDoubleSpinBox()
        self.entry_preco_compra.setMaximum(9999)
        self.entry_preco_compra.setPrefix("R$ ")
        self.entry_preco_compra.setValue(1)
        self.entry_preco_venda = QDoubleSpinBox()
        self.entry_preco_venda.setMaximum(9999)
        self.entry_preco_venda.setPrefix("R$ ")
        self.textEntry_descricao = QTextEdit()

        # Botão:
        self.button_salvar = QPushButton("&Salvar")
        self.button_salvar.setShortcut("Ctrl+S")
        self.button_salvar.clicked.connect(self.salvar)
        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.setShortcut("Ctrl+Z")
        self.button_voltar.clicked.connect(self.restore_mode)

        # Leiaute:
        self.layout = QVBoxLayout()
        self.layout_buttons = QHBoxLayout()
        self.layout.addWidget(self.label_nome)
        self.layout.addWidget(self.entry_nome)
        self.layout.addWidget(self.label_code)
        self.layout.addWidget(self.entry_code)
        self.layout.addWidget(self.label_quantidade)
        self.layout.addWidget(self.entry_quantidade)
        self.layout.addWidget(self.label_preco_compra)
        self.layout.addWidget(self.entry_preco_compra)
        self.layout.addWidget(self.label_preco_venda)
        self.layout.addWidget(self.entry_preco_venda)
        self.layout.addWidget(self.label_descricao)
        self.layout.addWidget(self.textEntry_descricao)
        self.layout_buttons.addWidget(self.button_voltar)
        self.layout_buttons.addWidget(self.button_salvar)
        self.layout.addLayout(self.layout_buttons)
        self.setLayout(self.layout)

    @Slot()
    def salvar(self):
        # Salva a peça
        code = self.entry_code.text()
        descricao = self.textEntry_descricao.toPlainText()
        nome = self.entry_nome.text().upper()
        quantidade = self.entry_quantidade.value()
        preco_compra = self.entry_preco_compra.value()
        preco_venda = self.entry_preco_venda.value()
        peca = {
            "code": code,
            "name": nome,
            "qty": quantidade,
            "buy_price": preco_compra,
            "sell_price": preco_venda,
            "description": descricao,
        }
        # Tela de Pop Up
        self.popup = QMessageBox(QMessageBox.Question, "Dados", "Tudo Certo?")
        infotext = "Nome: {}\nCódigo: {}\nQuantidade: {}\n".format(
            peca["name"], peca["code"], peca["qty"])
        infotext += "Valor de Compra: {}\nValor de Venda: {}\nDescrição: {}\n".format(
            peca["buy_price"], peca["sell_price"], peca["description"])
        self.popup.setInformativeText(infotext)
        Salvar = self.popup.addButton(QMessageBox.Ok)
        self.popup.addButton("Voltar", QMessageBox.ButtonRole.RejectRole)
        self.popup.exec()
        if self.popup.clickedButton() == Salvar:  # Salva as Informações
            if self.entry_nome.isReadOnly():
                self.driver.buy_update(peca)
            else:
                self.driver.add_new(peca)
            self.restore_mode()
            self.update_signal.emit()
            self.status_signal.emit("Salvo")

    @Slot()
    def mode_atualizar(self, id: int):
        data = self.driver.show(id)
        self.label_nome.setText("Nome da Peça:")
        self.entry_quantidade.setValue(0)
        self.entry_preco_compra.setValue(0)
        self.entry_nome.setText(data["nome"])
        self.entry_code.setText(data["code"])
        self.entry_preco_venda.setValue(data["preco_venda"])
        self.textEntry_descricao.setText(data["descricao"])
        self.entry_nome.setReadOnly(True)
        self.entry_code.setReadOnly(True)
        self.entry_preco_venda.setReadOnly(True)
        self.textEntry_descricao.setReadOnly(True)

    @Slot()
    def restore_mode(self):
        self.label_nome.setText("Nome da Nova Peça:")
        self.entry_nome.setReadOnly(False)
        self.entry_code.setReadOnly(False)
        self.entry_preco_venda.setReadOnly(False)
        self.textEntry_descricao.setReadOnly(False)
        self.entry_nome.clear()
        self.entry_code.clear()
        self.textEntry_descricao.clear()
        self.entry_quantidade.setValue(0)
        self.entry_preco_compra.setValue(0)
        self.entry_preco_venda.setValue(0)


# Segunda Aba
class BuscadorDePeças(QWidget):
    selected_cell_info = Signal(dict)
    status_signal = Signal(str)

    def __init__(self):

        QWidget.__init__(self)
        self.driver = EstoqueDB()

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
