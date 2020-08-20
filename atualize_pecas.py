# -*- coding: utf-8 -*-
from PySide2.QtWidgets import (
    QWidget,
    QDialog,
    QLabel,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QPushButton,
    QButtonGroup,
    QCheckBox,
)
from PySide2.QtCore import Slot, Qt
from motor import estoque_driver

# Segunda Aba
class Atualizar_Pecas(QDialog):
    def __init__(self, id):
        # Inicialização da Janela

        QDialog.__init__(self)
        self.driver = estoque_driver()
        self.pecaid = id

        # Label:
        info = self.driver.show(self.pecaid)
        self.label_nome = QLabel("Nome: {}".format(info["nome"]))
        self.label_code = QLabel("Código: {}".format(info["code"]))
        self.label_quantidade = QLabel("Quantidade:")
        self.label_preco_compra = QLabel("Preço de\nCompra:")
        self.label_preco_venda = QLabel("Preço de\nVenda:")

        # Entradas:
        self.entry_quantidade = QSpinBox()
        self.entry_preco_compra = QDoubleSpinBox()
        self.entry_preco_compra.setMaximum(9999)
        self.entry_preco_compra.setPrefix("R$ ")
        self.entry_preco_venda = QDoubleSpinBox()
        self.entry_preco_venda.setMaximum(9999)
        self.entry_preco_venda.setPrefix("R$ ")
        self.entry_preco_venda.setEnabled(False)

        # Botão:
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_venda = QCheckBox("Venda")
        self.button_compra = QCheckBox("Compra")
        self.button_compra.setChecked(True)
        self.button_compra.toggled.connect(self.modo)
        self.button_group.addButton(self.button_venda)
        self.button_group.addButton(self.button_compra)
        self.button_salvar = QPushButton("&Salvar")
        self.button_salvar.setShortcut("Ctrl+S")
        self.button_salvar.clicked.connect(self.salvar)
        self.button_voltar = QPushButton("Voltar")
        self.button_voltar.setShortcut("Ctrl+Z")
        self.button_voltar.clicked.connect(self.sair)

        # Leiaute:
        self.layout = QGridLayout()
        self.layout.addWidget(self.label_nome, 0, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.label_code, 0, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.button_venda, 1, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.button_compra, 1, 1, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.label_quantidade, 2, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.entry_quantidade, 2, 1, 1, 1)
        self.layout.addWidget(self.label_preco_compra, 3, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.entry_preco_compra, 3, 1, 1, 1)
        self.layout.addWidget(self.label_preco_venda, 4, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.entry_preco_venda, 4, 1, 1, 1)
        self.layout.addWidget(self.button_voltar, 5, 0, 1, 1, Qt.AlignCenter)
        self.layout.addWidget(self.button_salvar, 5, 1, 1, 1, Qt.AlignCenter)
        self.setLayout(self.layout)

    @Slot()
    def salvar(self):
        # Salva a peça
        quantidade = self.entry_quantidade.value()
        if self.button_venda.isChecked():
            preco_venda = self.entry_preco_venda.value()
            peca_atualizada = {
                "id": self.pecaid,
                "delta_qty": (-quantidade),
                "qty": quantidade,
                "sell_price": preco_venda,
            }
            # self.driver.sell_update(peca_atualizada)
        else:
            preco_compra = self.entry_preco_compra.value()
            peca_atualizada = {
                "id": self.pecaid,
                "delta_qty": quantidade,
                "qty": quantidade,
                "buy_price": preco_compra,
            }
            # self.driver.buy_update(peca_atualizada)

        self.entry_quantidade.setValue(0)
        self.entry_preco_compra.setValue(0)
        self.entry_preco_venda.setValue(0)
        self.close()
        print(peca_atualizada)
        # status.setText("Salvo")

    @Slot()
    def sair(self):
        self.close()

    @Slot()
    def modo(self):
        if self.button_venda.isChecked():
            self.entry_preco_compra.setEnabled(False)
            self.entry_preco_venda.setEnabled(True)
        else:
            self.entry_preco_compra.setEnabled(True)
            self.entry_preco_venda.setEnabled(False)
