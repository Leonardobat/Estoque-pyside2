# Leitor de Dados
from PySide2.QtWidgets import (
    QComboBox,
    QDialog,
    QGridLayout, # ESCOLHER
    QHBoxLayout,
    QVBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QWidget,
    QSpinBox,
    QDoubleSpinBox,
)
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QFont
from motor import estoque_driver

# init_db()
# Primeira Aba
class Novas_Pecas(QWidget):
    def __init__(self):  # Inicialização da Janela
        QWidget.__init__(self)
        self.driver = estoque_driver()

        # Label:
        self.label_nome = QLabel("Nome:")
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

        # Leiaute:
        self.layout = QVBoxLayout()
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
        self.layout.addWidget(self.button_salvar)
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
        nova_peca = {
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
            nova_peca["name"], nova_peca["code"], nova_peca["qty"]
        )
        infotext += "Valor de Compra: {}\nValor de Venda: {}\nDescrição: {}\n".format(
            nova_peca["buy_price"], nova_peca["sell_price"], nova_peca["description"]
        )
        self.popup.setInformativeText(infotext)
        Salvar = self.popup.addButton(QMessageBox.Ok)
        self.popup.addButton("Voltar", QMessageBox.ButtonRole.RejectRole)
        self.popup.exec()
        if self.popup.clickedButton() == Salvar:  # Salva as Informações
            self.driver.add_new(nova_peca)

            # Restaura para os Valores Originais
            self.entry_nome.setText("")
            self.entry_code.setText("")
            self.textEntry_descricao.setText("")
            self.entry_quantidade.setValue(0)
            self.entry_preco_compra.setValue(0)
            self.entry_preco_venda.setValue(0)
            #status.setText("Salvo") # It's on main file