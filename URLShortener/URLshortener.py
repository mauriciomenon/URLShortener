# Mauricio Menon (+AI) 22072024
import sys
import pyshorteners
import pyshorteners.shorteners
import pyshorteners.shorteners.tinyurl 
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QDateTime

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.resize(800, 600)  # Aumentar o tamanho da janela
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Layout para entrada e resultado
        input_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        
        # Campo de entrada para URL original
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entre a URL a ser encurtada")
        self.url_input.setMinimumHeight(40)  # Aumentar a altura da entrada de URL
        self.url_input.setStyleSheet("background-color: #ffffff;")  # Fundo branco
        self.url_input.returnPressed.connect(self.shorten_url)  # Conectar a tecla Enter à função shorten_url
        input_label = QLabel("URL Original:")
        input_label.setFixedWidth(100)
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.url_input)
        
        # Botão para encurtar URL
        shorten_button = QPushButton("Encurtar", self)
        shorten_button.clicked.connect(self.shorten_url)
        shorten_button.setMinimumHeight(40)  # Ajustar a altura do botão
        input_layout.addWidget(shorten_button)
        
        # Campo de saída para URL encurtado
        self.short_url_output = QLineEdit(self)
        self.short_url_output.setReadOnly(True)
        self.short_url_output.setMinimumHeight(40)  # Aumentar a altura da saída de URL
        self.short_url_output.setStyleSheet("background-color: #ffffff;")  # Fundo branco
        result_label = QLabel("URL Encurtada:")
        result_label.setFixedWidth(100)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.short_url_output)
        
        # Botão para copiar URL encurtado
        copy_button = QPushButton("Copiar", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setMinimumHeight(40)  # Ajustar a altura do botão
        result_layout.addWidget(copy_button)
        
        # Tabela para histórico
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(2)
        self.history_table.setHorizontalHeaderLabels(["URL Original", "URL Encurtada"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 400)  # Ajustar largura das colunas
        self.history_table.setColumnWidth(1, 400)
        self.history_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #f0f0f0; }")  # Fundo cinza claro no cabeçalho
        
        # Adicionar layouts ao layout principal
        layout.addLayout(input_layout)
        layout.addLayout(result_layout)
        layout.addWidget(QLabel("Histórico:"))
        layout.addWidget(self.history_table)
        
        # Configurar layout principal
        self.setLayout(layout)
        
        # Menu de contexto para copiar texto
        self.url_input.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.url_input.customContextMenuRequested.connect(self.show_context_menu)
        
        self.short_url_output.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.short_url_output.customContextMenuRequested.connect(self.show_context_menu)
        
        self.history_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_context_menu_history)
        
        # Adicionar menu About e data/hora
        footer_layout = QHBoxLayout()
        about_button = QPushButton("About", self)
        about_button.clicked.connect(self.show_about_dialog)
        about_button.setMinimumHeight(20)  # Reduzir o tamanho do botão About
        footer_layout.addWidget(about_button)
        
        self.datetime_label = QLabel(self)
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(self.datetime_label)
        
        layout.addLayout(footer_layout)
        
        # Atualizar data e hora a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        
    def shorten_url(self):
        long_url = self.url_input.text()
        self.show_temporary_message("Encurtando...")
        short_url = self.get_short_url(long_url)
        self.short_url_output.setText(short_url)
        
        # Copiar automaticamente para a área de transferência
        self.copy_to_clipboard()
        
        # Atualizar histórico
        row_position = self.history_table.rowCount()
        self.history_table.insertRow(row_position)
        self.history_table.setItem(row_position, 0, QTableWidgetItem(long_url))
        self.history_table.setItem(row_position, 1, QTableWidgetItem(short_url))
        
    def get_short_url(self, long_url):
        try:
            type_tiny = pyshorteners.Shortener(timeout=10)
            short_url = type_tiny.tinyurl.short(long_url)
            return short_url
        except Exception as e:
            return f"Error: {e}"
        
    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.short_url_output.text())
        
    def show_context_menu(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Copiar")
        paste_action = menu.addAction("Colar")
        action = menu.exec(self.url_input.mapToGlobal(position))
        if action == copy_action:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.url_input.text() if self.focusWidget() == self.url_input else self.short_url_output.text())
        elif action == paste_action:
            clipboard = QApplication.clipboard()
            self.url_input.setText(clipboard.text())
            
    def show_context_menu_history(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Copiar")
        action = menu.exec(self.history_table.mapToGlobal(position))
        if action == copy_action:
            selected_items = self.history_table.selectedItems()
            if selected_items:
                clipboard = QApplication.clipboard()
                clipboard.setText(selected_items[0].text())
                
    def show_temporary_message(self, message, timeout=2000):
        self.temp_message = QLabel(message, self)
        self.temp_message.setStyleSheet("background-color: #d3d3d3; border: 1px solid black;")  # Tom de cinza
        self.temp_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_message.setFixedSize(200, 50)
        self.temp_message.move((self.width() - self.temp_message.width()) // 2, (self.height() - self.temp_message.height()) // 2)
        self.temp_message.show()
        
        QTimer.singleShot(timeout, self.temp_message.close)
        
    def show_about_dialog(self):
        about_msg = QMessageBox(self)
        about_msg.setWindowTitle("About")
        about_msg.setText("URL Shortener\nPyQt6+PyInstaller\nAutor: Maurício Menon (+AI)\nVersão: 1.7")
        about_msg.setGeometry(50, 50, 150, 100)  # Ainda menor e exibida ao lado esquerdo
        about_msg.exec()
        
    def update_datetime(self):
        try:
            current_datetime = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")
            self.datetime_label.setText(current_datetime)
        except Exception as e:
            print(f"Erro atualizando data/hora: {e}")

def main():
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
