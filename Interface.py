# Leitor de Dados
import sys
from PySide2.QtWidgets import (
    QAbstractItemView,
    QAction,
    QApplication,
    QComboBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMdiArea,
    QMenuBar,
    QMessageBox,
    QPushButton,
    QStatusBar,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QFont
from motor import estoque_driver

# init_db()
# Primeira Aba
class Atualizar_Quantidades(QWidget):
    def __init__(self):  # Inicialização da Janela
        QWidget.__init__(self)
        self.driver = estoque_driver()

        # Label:
        self.label_nome = QLabel()
        self.label_nome.setText("Nome:")
        self.label_code = QLabel()
        self.label_code.setText("Código:")
        self.label_quantidade = QLabel()
        self.label_quantidade.setText("Quantidade:")
        self.label_preco_compra = QLabel()
        self.label_preco_compra.setText("Preço de Compra:")
        self.label_preco_venda = QLabel()
        self.label_preco_venda.setText("Preço de Venda:")
        self.label_descricao = QLabel()
        self.label_descricao.setText("Descrição:")

        # Entradas:
        self.entry_nome = QLineEdit()
        self.entry_code = QLineEdit("Código de Identificação da Peça")
        self.entry_quantidade = QLineEdit()
        self.entry_preco_compra = QLineEdit()
        self.entry_preco_venda = QLineEdit()

        # Entrada de Texto:
        self.textEntry_descricao = QTextEdit()
        self.textEntry_descricao.setPlainText("Comente o que foi feito")

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
        nome = self.entry_nome.text()
        quantidade = int(self.entry_quantidade.text())
        preco_compra = float(self.entry_preco_compra.text())
        preco_venda = float(self.entry_preco_venda.text())
        dicta = {
            "code": code,
            "description": descricao,
            "name": nome,
            "qty": quantidade,
            "buy_price": preco_compra,
            "sell_price": preco_venda,
        }
        print(dicta)
        self.driver.add_new(dicta)

        # # Tela de Pop Up
        # self.popup = QMessageBox(QMessageBox.Question, "Dados", "Tudo Certo?")
        # self.popup.setInformativeText(Info)
        # Salvar = self.popup.addButton(QMessageBox.Ok)
        # self.popup.addButton("Voltar", QMessageBox.ButtonRole.RejectRole)
        # self.popup.exec()
        # if self.popup.clickedButton() == Salvar:  # Salva as Informações
        #     f = open((caminho + self.nome + " " + self.dia + ".txt"), "a+")
        #     f.write(Info)
        #     f.close()

        #     conn_c = sqlite3.connect(caminho + "Clientes.db")
        #     cursor_c = conn_c.cursor()
        #     t = (self.nome, self.numero, self.dia)
        #     cursor_c.execute(
        #         """ INSERT INTO cliente (nome, número, data)
        #                     VALUES (?,?,?) """,
        #         t,
        #     )
        #     conn_c.commit()
        #     cursor_c.close()

        #     # Restaura para os Valores Originais
        #     self.e_nome_completo = QLineEdit("Nome Completo")
        #     self.e_cpf = QLineEdit()
        #     self.e_numero = QLineEdit("Apenas os Números!")
        #     self.e_placa = QLineEdit("")
        #     self.e_km = QLineEdit("Apenas os Números!")
        #     self.e_placa = QLineEdit("")
        #     self.e_valor = QLineEdit("Total Pago e Devido")
        #     self.t_servico.setPlainText("Comente o que foi feito")
        #     status.setText("Salvo em: " + caminho + self.nome + " " + self.dia + ".txt")


# Segunda Aba
class Buscador_de_Pecas(QWidget):
    def __init__(self):
        # Inicialização da Janela

        QWidget.__init__(self)
        self.driver = estoque_driver()
        Font = QFont()
        Font.setBold(True)  # deixar o label Negrito

        # Widgets:
        self.label_busca = QLabel()
        self.label_busca.setText("Nome ou Código da Peça:")
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
        self.tabela_pecas.setRowCount(0)
        self.pecas = 0
        peca_buscada = self.entry_busca.text()
        print(peca_buscada)
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
        status.setText("Feito")

    @Slot()
    def info(self):
        code = self.tabela_pecas.item(self.tabela_pecas.currentRow(), 0)
        id = self.driver.get_id(code.text())
        data = self.driver.show_info(id)
        texto = "Nome: {0},\nDescrição: {1}".format(data["nome"], data["descricao"])
        self.popup = QMessageBox(QMessageBox.Information, "Busca", "Informações:")
        self.popup.setInformativeText(texto)
        self.popup.addButton(QMessageBox.Ok)
        self.popup.exec()
        status.setText("Feito")


class Janelas(QMdiArea):
    def __init__(self):  # Inicialização da Janela
        QMdiArea.__init__(self)
        window1 = self.addSubWindow(Atualizar_Quantidades())
        window2 = self.addSubWindow(Buscador_de_Pecas())
        window1.setWindowTitle("Estoque")
        window2.setWindowTitle("Busque por Peças")
        self.setViewMode(QMdiArea.TabbedView)
        self.setActiveSubWindow(window2)


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
        status = QLabel()
        status.setText("Pronto")
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
    window.resize(500, 600)
    window.show()
    sys.exit(app.exec_())
