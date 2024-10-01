# Mauricio Menon (+AI) 30092024
import sys
import pyshorteners
import pyshorteners.shorteners
import pyshorteners.shorteners.tinyurl
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox
from PyQt6.QtGui import QPixmap, QClipboard
from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.resize(1100, 750)  # Ajuste na altura da janela para acomodar a tabela de histórico maior

        # Layout principal
        main_layout = QHBoxLayout()  # Usando layout horizontal principal para acomodar as linhas e o QR Code

        # Definindo tamanho fixo para os botões
        button_size = QSize(100, 40)

        # Layout das três linhas de entrada e saída (URL Original, URL Encurtada, URL Alternativa)
        urls_layout = QVBoxLayout()

        # Campo de entrada para URL original
        url_input_layout = QHBoxLayout()
        url_input_label = QLabel("URL Original:")
        url_input_label.setFixedWidth(150)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entre a URL a ser encurtada")
        self.url_input.setMinimumHeight(30)
        self.url_input.setFixedWidth(600)  #  a largura da caixa de entrada
        self.url_input.setStyleSheet("background-color: #ffffff; color: #000000;")
        self.url_input.returnPressed.connect(self.shorten_url)
        shorten_button = QPushButton("Encurtar", self)
        shorten_button.setFixedSize(button_size)
        shorten_button.clicked.connect(self.shorten_url)
        url_input_layout.addWidget(url_input_label)
        url_input_layout.addWidget(self.url_input)
        url_input_layout.addWidget(shorten_button)

        # Campo de saída para URL encurtada principal
        short_url_layout = QHBoxLayout()
        short_url_label = QLabel("URL Encurtada:")
        short_url_label.setFixedWidth(150)
        self.short_url_output = QLineEdit(self)
        self.short_url_output.setReadOnly(True)
        self.short_url_output.setMinimumHeight(30)
        self.short_url_output.setFixedWidth(600)  # largura da caixa de saída principal 
        self.short_url_output.setStyleSheet("background-color: #ffffff; color: #000000;")
        copy_button = QPushButton("Copiar", self)
        copy_button.setFixedSize(button_size)
        copy_button.clicked.connect(self.copy_to_clipboard)
        short_url_layout.addWidget(short_url_label)
        short_url_layout.addWidget(self.short_url_output)
        short_url_layout.addWidget(copy_button)

        # Campo de saída para URL encurtada alternativa
        alt_short_url_layout = QHBoxLayout()
        alt_short_url_label = QLabel("URL Encurtada Alternativa:")
        alt_short_url_label.setFixedWidth(150)
        self.alt_short_url_output = QLineEdit(self)
        self.alt_short_url_output.setReadOnly(True)
        self.alt_short_url_output.setMinimumHeight(30)
        self.alt_short_url_output.setFixedWidth(600)  # Reduzindo a largura da caixa de saída alternativa em aproximadamente 20%
        self.alt_short_url_output.setStyleSheet("background-color: #ffffff; color: #000000;")
        copy_alt_button = QPushButton("Copiar", self)
        copy_alt_button.setFixedSize(button_size)
        copy_alt_button.clicked.connect(self.copy_alt_to_clipboard)
        alt_short_url_layout.addWidget(alt_short_url_label)
        alt_short_url_layout.addWidget(self.alt_short_url_output)
        alt_short_url_layout.addWidget(copy_alt_button)

        # Adicionar todas as linhas de URL ao layout vertical
        urls_layout.addLayout(url_input_layout)
        urls_layout.addLayout(short_url_layout)
        urls_layout.addLayout(alt_short_url_layout)

        # Layout para o QR Code e botão copiar QR Code, alinhado à direita das três linhas
        qr_code_layout = QVBoxLayout()
        self.qr_code_label = QLabel(self)
        self.qr_code_label.setFixedSize(155, 155)  # Tamanho ajustado do QR Code
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Adicionar QR Code ao layout e alinhá-lo na altura das duas primeiras linhas
        qr_code_layout.addStretch()  # Espaço flexível antes do QR Code para ajustá-lo verticalmente
        qr_code_layout.addWidget(self.qr_code_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        #qr_code_layout.addStretch()  # Adicionar mais espaço antes do botão "Copiar QR Code"

        # Botão para copiar QR Code deve estar perfeitamente alinhado abaixo do QR Code
        copy_qr_button = QPushButton("Copiar QR Code", self)
        copy_qr_button.setMinimumHeight(40)
        copy_qr_button.setMaximumWidth(self.qr_code_label.width())  # Fazer o botão ter a mesma largura do QR Code
        copy_qr_button.clicked.connect(self.copy_qr_code_to_clipboard)
        qr_code_layout.addWidget(copy_qr_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Adicionar espaço flexível abaixo do botão para manter alinhamento
        qr_code_layout.addStretch()

        # Adicionar os layouts de URL e QR Code ao layout principal
        main_layout.addLayout(urls_layout)
        main_layout.addLayout(qr_code_layout)

        # Layout para histórico
        history_layout = QVBoxLayout()
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(4)
        self.history_table.setHorizontalHeaderLabels(["URL Original", "URL Encurtada", "URL Alternativa", "QR Code"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 350)
        self.history_table.setColumnWidth(1, 250)
        self.history_table.setColumnWidth(2, 250)
        self.history_table.setColumnWidth(3, 200)
        self.history_table.setMinimumHeight(350)  # Aumentar ainda mais a altura mínima da tabela
        self.history_table.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #f0f0f0; }")

        # Adicionar histórico ao layout principal
        history_layout.addWidget(QLabel("Histórico:"))
        history_layout.addWidget(self.history_table)

        # Configurar layout principal para ser vertical, contendo tanto as URLs/QR Code quanto o histórico
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.addLayout(main_layout)
        main_vertical_layout.addLayout(history_layout)

        # Adicionar menu About e data/hora
        footer_layout = QHBoxLayout()
        about_button = QPushButton("About", self)
        about_button.setFixedSize(button_size)
        about_button.clicked.connect(self.show_about_dialog)
        footer_layout.addWidget(about_button)

        self.datetime_label = QLabel(self)
        self.datetime_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        footer_layout.addWidget(self.datetime_label)

        main_vertical_layout.addLayout(footer_layout)

        # Configurar o layout principal da janela
        self.setLayout(main_vertical_layout)

        # Atualizar data e hora a cada segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)

    def shorten_url(self):
        long_url = self.url_input.text()
        print(f"URL Digitada: {long_url}")

        self.show_temporary_message("Encurtando...")
        short_url = self.get_short_url(long_url)
        alt_short_url = self.get_alt_short_url(long_url)

        if "Error" not in short_url:
            self.short_url_output.setText(short_url)
            self.short_url_output.repaint()
            print(f"URL Encurtada: {short_url}")

            self.alt_short_url_output.setText(alt_short_url)
            self.alt_short_url_output.repaint()
            print(f"URL Encurtada Alternativa: {alt_short_url}")

            self.copy_to_clipboard()

            qr_image_path = self.generate_qr_code(long_url)
            self.url_input.clear()

            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            self.history_table.setItem(row_position, 0, QTableWidgetItem(long_url))
            self.history_table.setItem(row_position, 1, QTableWidgetItem(short_url))
            self.history_table.setItem(row_position, 2, QTableWidgetItem(alt_short_url))

            qr_pixmap = QPixmap(qr_image_path).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
            qr_label = QLabel()
            qr_label.setPixmap(qr_pixmap)
            self.history_table.setCellWidget(row_position, 3, qr_label)

    def get_short_url(self, long_url):
        try:
            type_tiny = pyshorteners.Shortener(timeout=10)
            short_url = type_tiny.tinyurl.short(long_url)
            return short_url
        except Exception as e:
            return f"Error: {e}"

    def get_alt_short_url(self, long_url):
        try:
            type_isgd = pyshorteners.Shortener().isgd
            alt_short_url = type_isgd.short(long_url)
            return alt_short_url
        except Exception as e:
            return f"Error: {e}"

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.short_url_output.text())
        print(f"Copiado para área de transferência: {self.short_url_output.text()}")

    def copy_alt_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.alt_short_url_output.text())
        print(f"Copiado para área de transferência (alternativo): {self.alt_short_url_output.text()}")

    # Restante do código permanece igual...


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
            font = ImageFont.truetype("arial.ttf", 22)  # Aumentar o tamanho da fonte
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
        about_msg.setText("URL Shortener\nPyQt6+PyInstaller\nAutor: Maurício Menon (+AI)\nVersão: 1.9")
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
