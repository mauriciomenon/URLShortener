# Mauricio Menon (+AI) 22072024
import sys
import pyshorteners
import pyshorteners.shorteners
import pyshorteners.shorteners.tinyurl
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox
from PyQt6.QtGui import QPixmap, QClipboard
from PyQt6.QtCore import Qt, QTimer, QDateTime

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.resize(900, 600)  # Aumentar a largura da janela
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Layout para entrada e resultado
        input_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        
        # Campo de entrada para URL original
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entre a URL a ser encurtada")
        self.url_input.setMinimumHeight(40)  # Aumentar a altura da entrada de URL
        self.url_input.setStyleSheet("background-color: #ffffff; color: #000000;")  # Fundo branco, texto preto
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
        self.short_url_output.setStyleSheet("background-color: #ffffff; color: #000000;")  # Fundo branco, texto preto
        result_label = QLabel("URL Encurtada:")
        result_label.setFixedWidth(100)
        result_layout.addWidget(result_label)
        result_layout.addWidget(self.short_url_output)
        
        # Botão para copiar URL encurtado
        copy_button = QPushButton("Copiar", self)
        copy_button.clicked.connect(self.copy_to_clipboard)
        copy_button.setMinimumHeight(40)  # Ajustar a altura do botão
        result_layout.addWidget(copy_button)

        # Botão para copiar QR Code
        copy_qr_button = QPushButton("Copiar QR Code", self)
        copy_qr_button.clicked.connect(self.copy_qr_code_to_clipboard)
        copy_qr_button.setMinimumHeight(40)
        result_layout.addWidget(copy_qr_button)
        
        # Campo de saída para QR Code
        self.qr_code_label = QLabel(self)
        self.qr_code_label.setFixedSize(150, 150)  # QR Code menor
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.qr_code_label)
        
        # Tabela para histórico
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["URL Original", "URL Encurtada", "QR Code"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 350)  # Ajustar largura das colunas
        self.history_table.setColumnWidth(1, 350)
        self.history_table.setColumnWidth(2, 150)
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
        print(f"URL Digitada: {long_url}")  # Depuração para verificar se a URL foi capturada

        self.show_temporary_message("Encurtando...")
        short_url = self.get_short_url(long_url)
        
        # Verificar se o encurtamento ocorreu sem erros
        if "Error" not in short_url:
            self.short_url_output.setText(short_url)
            self.short_url_output.repaint()  # Forçar atualização da interface
            print(f"URL Encurtada: {short_url}")  # Depuração para verificar se a URL encurtada está correta
        
            # Copiar automaticamente para a área de transferência
            self.copy_to_clipboard()

            # Gerar QR Code com o texto "TJSP" no meio, usando a URL original
            qr_image_path = self.generate_qr_code(long_url)

            # Limpar URL original após encurtar
            self.url_input.clear()
            
            # Atualizar histórico
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(long_url))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(short_url))

            # Adicionar QR Code na tabela
            qr_pixmap = QPixmap(qr_image_path).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
            qr_label = QLabel()
            qr_label.setPixmap(qr_pixmap)
            self.history_table.setCellWidget(row_position, 2, qr_label)

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
        print(f"Copiado para área de transferência: {self.short_url_output.text()}")  # Depuração

    def copy_qr_code_to_clipboard(self):
        clipboard = QApplication.clipboard()
        pixmap = QPixmap("qrcode.png")
        if not pixmap.isNull():
            clipboard.setPixmap(pixmap)
        
    def generate_qr_code(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Gerar a imagem do QR Code
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Criar uma nova imagem maior para acomodar o texto abaixo do QR Code
        new_height = img.size[1] + 30  # Aumentar a altura para adicionar espaço para o texto
        new_img = Image.new("RGB", (img.size[0], new_height), (255, 255, 255))  # Fundo branco
        new_img.paste(img, (0, 0))  # Colar o QR Code na parte superior

        # Adicionar o texto abaixo do QR Code
        draw = ImageDraw.Draw(new_img)
        text = "TJSP - Link para entrar na reunião"
        try:
            # Usar uma fonte TrueType se disponível para melhorar a qualidade
            font = ImageFont.truetype("arial.ttf", 30)  # Aumentar o tamanho da fonte
        except IOError:
            # Caso a fonte TrueType não esteja disponível, usar a fonte padrão
            font = ImageFont.load_default()
        
        bbox = draw.textbbox((0, 0), text, font=font)  # Substituir textsize por textbbox para obter as dimensões
        text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        position = ((new_img.size[0] - text_width) // 2, img.size[1] + 2)  # Centralizado horizontalmente e próximo ao QR Code
        draw.text(position, text, fill=(0, 0, 0), font=font)  # Texto em preto

        # Salvar a imagem do QR Code com alta qualidade
        qr_image_path = "qrcode.png"
        new_img.save(qr_image_path, quality=95)
        
        # Mostrar o QR Code na interface após garantir a inicialização completa do ambiente gráfico
        if QApplication.instance() is not None:
            pixmap = QPixmap(qr_image_path).scaled(150, 200, Qt.AspectRatioMode.KeepAspectRatio)
            self.qr_code_label.setPixmap(pixmap)

        return qr_image_path




        
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
        copy_action = menu.addAction("Copiar URL")
        copy_qr_action = menu.addAction("Copiar QR Code")
        action = menu.exec(self.history_table.mapToGlobal(position))
        selected_items = self.history_table.selectedItems()
        if action == copy_action and selected_items:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_items[0].text())
        elif action == copy_qr_action:
            row = self.history_table.currentRow()
            if row >= 0:
                qr_label = self.history_table.cellWidget(row, 2)
                if qr_label and isinstance(qr_label, QLabel):
                    pixmap = QPixmap("qrcode.png")
                    if not pixmap.isNull():
                        clipboard = QApplication.clipboard()
                        clipboard.setPixmap(pixmap)
                
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
