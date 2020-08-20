# Leitor de Dados
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide2.QtCore import Slot, Qt, Signal
from PySide2.QtGui import QFont
from motor import estoque_driver

# init_db()
# Primeira Aba
class Novas_Pecas(QWidget):
    status_signal = Signal(str)
    update_signal = Signal()

    def __init__(self):  # Inicialização da Janela
        QWidget.__init__(self)
        self.driver = estoque_driver()

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
        self.entry_preco_venda = QDoubleSpinBox()
        self.entry_preco_venda.setMaximum(9999)
        self.entry_preco_venda.setPrefix("R$ ")

        # Entrada de Texto:
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
            peca["name"], peca["code"], peca["qty"]
        )
        infotext += "Valor de Compra: {}\nValor de Venda: {}\nDescrição: {}\n".format(
            peca["buy_price"], peca["sell_price"], peca["description"]
        )
        self.popup.setInformativeText(infotext)
        Salvar = self.popup.addButton(QMessageBox.Ok)
        self.popup.addButton("Voltar", QMessageBox.ButtonRole.RejectRole)
        self.popup.exec()
        if self.popup.clickedButton() == Salvar:  # Salva as Informações
            if self.entry_code.isReadOnly():
                if preco_compra != 0 and preco_venda == 0:
                    self.driver.buy_update(peca)
                elif preco_compra == 0 and preco_venda != 0:
                    self.driver.sell_update(peca)
                else:
                    raise KeyError
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
        self.entry_quantidade.setValue(0)
        self.entry_preco_compra.setValue(0)
        self.entry_preco_venda.setValue(0)
        self.entry_nome.setText(data["nome"])
        self.entry_code.setText(data["code"])
        self.textEntry_descricao.setText(data["descricao"])
        self.entry_nome.setReadOnly(True)
        self.entry_code.setEnabled(False)
        self.textEntry_descricao.setReadOnly(True)

    @Slot()
    def restore_mode(self):
        self.label_nome.setText("Nome da Nova Peça:")
        self.entry_nome.setReadOnly(False)
        self.entry_code.setEnabled(True)
        self.textEntry_descricao.setReadOnly(False)
        self.entry_nome.setText("")
        self.entry_code.setText("")
        self.textEntry_descricao.setText("")
        self.entry_quantidade.setValue(0)
        self.entry_preco_compra.setValue(0)
        self.entry_preco_venda.setValue(0)
