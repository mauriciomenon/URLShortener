# Mauricio Menon (+AI) 02102024
import sys, os
import pyshorteners
import pyshorteners.shorteners
import pyshorteners.shorteners.tinyurl
import qrcode
from PIL import Image, ImageDraw, ImageFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMenu, QMessageBox, QCheckBox
from PyQt6.QtGui import QPixmap, QClipboard, QImage
from PyQt6.QtCore import Qt, QTimer, QDateTime, QSize
import io
import platform

class URLShortenerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.last_generated_qr = None
        
    def show_about_dialog(self):
        about_msg = QMessageBox(self)
        about_msg.setWindowTitle("About")
        about_msg.setText("URL Shortener\nPyQt6+PyInstaller\nAutor: Maurício Menon (+AI)\nVersão: 1.4\n03-10-2024")
        about_msg.setGeometry(50, 50, 150, 100)
        about_msg.exec()   
        
    def update_datetime(self):
        try:
            current_datetime = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")
            self.datetime_label.setText(current_datetime)
        except Exception as e:
            print(f"Erro atualizando data/hora: {e}") 
        
    def initUI(self):
        # Configurar o tema específico do Windows, cores suavizadas para estilo Windows 10
        self.setStyleSheet("""
            QWidget {
                background-color: #e6e6e6;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            QPushButton {
                background-color: #0078d7;
                color: #ffffff;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #bfbfbf;
                padding: 4px;
                border-radius: 4px;
                font-size: 10pt;
                color: #000000;
            }
            QLabel {
                font-size: 10pt;
                color: #000000;
            }
            QCheckBox {
                font-size: 10pt;
                color: #000000;
            }
            QHeaderView::section {
                background-color: #0078d7;
                color: #ffffff;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                gridline-color: #c0c0c0;
                font-size: 10pt;
            }
        """)

        self.setWindowTitle('URL Shortener')
        self.resize(1100, 800)

        # Layout principal
        main_layout = QHBoxLayout()

        # Definindo tamanho fixo para os botões
        button_size = QSize(100, 40)

        # Layout das três linhas de entrada e saída (URL Original, URL Encurtada, URL Alternativa)
        urls_layout = QVBoxLayout()
        urls_layout.setSpacing(10)

        # Largura fixa para campos de entrada
        input_width = 600

        # Campo de entrada para URL original
        url_input_layout = QHBoxLayout()
        url_input_label = QLabel("URL Original:")
        url_input_label.setFixedWidth(150)
        
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Entre a URL a ser encurtada")
        self.url_input.setMinimumHeight(30)
        self.url_input.setFixedWidth(input_width)
        self.url_input.returnPressed.connect(self.shorten_url)
        
        shorten_button = QPushButton("Encurtar", self)
        shorten_button.setFixedSize(button_size)
        shorten_button.clicked.connect(self.shorten_url)
        url_input_layout.addWidget(url_input_label)
        url_input_layout.addWidget(self.url_input)
        url_input_layout.addWidget(shorten_button)
        url_input_layout.addStretch()

        # Campo de entrada para texto do QR Code
        qr_text_layout = QHBoxLayout()
        qr_text_label = QLabel("Texto do QR Code:")
        qr_text_label.setFixedWidth(150)
        self.qr_text_input = QLineEdit(self)
        self.qr_text_input.setPlaceholderText("Texto abaixo do QR Code")
        self.qr_text_input.setText("TJSP - Link Teams")
        self.qr_text_input.setFixedWidth(input_width)
        self.qr_text_input.setMinimumHeight(30)
        qr_text_checkbox = QCheckBox("Mostrar no QR", self)
        qr_text_checkbox.setChecked(True)
        qr_text_layout.addWidget(qr_text_label)
        qr_text_layout.addWidget(self.qr_text_input)
        qr_text_layout.addWidget(qr_text_checkbox)
        qr_text_layout.addStretch()

        # Conectar o checkbox à visibilidade do texto
        qr_text_checkbox.stateChanged.connect(lambda state: self.update_qr_text_visibility(state))

        # Campo de saída para URL encurtada principal
        short_url_layout = QHBoxLayout()
        short_url_label = QLabel("URL Encurtada:")
        short_url_label.setFixedWidth(150)
        self.short_url_output = QLineEdit(self)
        self.short_url_output.setReadOnly(True)
        self.short_url_output.setMinimumHeight(30)
        self.short_url_output.setFixedWidth(input_width)
        copy_button = QPushButton("Copiar", self)
        copy_button.setFixedSize(button_size)
        copy_button.clicked.connect(self.copy_to_clipboard)
        short_url_layout.addWidget(short_url_label)
        short_url_layout.addWidget(self.short_url_output)
        short_url_layout.addWidget(copy_button)
        short_url_layout.addStretch()

        # Campo de saída para URL encurtada alternativa
        alt_short_url_layout = QHBoxLayout()
        alt_short_url_label = QLabel("URL Encurtada Alternativa:")
        alt_short_url_label.setFixedWidth(150)
        self.alt_short_url_output = QLineEdit(self)
        self.alt_short_url_output.setReadOnly(True)
        self.alt_short_url_output.setMinimumHeight(30)
        self.alt_short_url_output.setFixedWidth(input_width)
        copy_alt_button = QPushButton("Copiar", self)
        copy_alt_button.setFixedSize(button_size)
        copy_alt_button.clicked.connect(self.copy_alt_to_clipboard)
        alt_short_url_layout.addWidget(alt_short_url_label)
        alt_short_url_layout.addWidget(self.alt_short_url_output)
        alt_short_url_layout.addWidget(copy_alt_button)
        alt_short_url_layout.addStretch()

        # Adicionar todas as linhas de URL ao layout vertical
        urls_layout.addLayout(url_input_layout)
        urls_layout.addLayout(qr_text_layout)
        urls_layout.addLayout(short_url_layout)
        urls_layout.addLayout(alt_short_url_layout)

        # Layout para QR Code e botão copiar QR Code (lado direito das caixas de texto)
        qr_code_layout = QVBoxLayout()
        self.qr_code_label = QLabel(self)
        self.qr_code_label.setFixedSize(155, 155)
        self.qr_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        qr_code_layout.addWidget(self.qr_code_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        copy_qr_button = QPushButton("Copiar QR Code", self)
        copy_qr_button.setMinimumHeight(40)
        copy_qr_button.setMaximumWidth(self.qr_code_label.width())
        copy_qr_button.clicked.connect(self.copy_qr_code_to_clipboard)
        qr_code_layout.addWidget(copy_qr_button, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Adicionar os layouts de URLs e QR Code ao layout principal
        main_layout.addLayout(urls_layout)
        main_layout.addLayout(qr_code_layout)

        # Layout inferior (parte debaixo) para o histórico
        history_layout = QVBoxLayout()
        self.history_table = QTableWidget(self)
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["URL Original", "URL Encurtada", "URL Alternativa", "QR Code", "Timestamp"])

        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.setColumnWidth(0, 400)
        self.history_table.setColumnWidth(1, 225)
        self.history_table.setColumnWidth(2, 225)
        self.history_table.setColumnWidth(3, 60)
        self.history_table.setColumnWidth(4, 100)
        self.history_table.setMinimumHeight(350)
        #self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Configuração do menu de contexto para a tabela de histórico
        self.history_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.history_table.customContextMenuRequested.connect(self.show_context_menu_history)

        # Adicionar histórico ao layout inferior
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

            qr_image = self.generate_qr_code(long_url)
            qr_pixmap = self.pil_image_to_qpixmap(qr_image)

            # Atualizar o QR code principal
            self.qr_code_label.setPixmap(qr_pixmap)

            self.url_input.clear()

            timestamp = QDateTime.currentDateTime().toString("dd-MM-yyyy HH:mm:ss")

            # Adicionar ao histórico
            self.history_table.insertRow(0)
            self.history_table.setItem(0, 0, QTableWidgetItem(long_url))
            self.history_table.setItem(0, 1, QTableWidgetItem(short_url))
            self.history_table.setItem(0, 2, QTableWidgetItem(alt_short_url))
            self.history_table.setItem(0, 4, QTableWidgetItem(timestamp))

            # Usar o mesmo QR code no histórico sem redimensionamento
            qr_label = QLabel()
            qr_label.setPixmap(qr_pixmap)
            self.history_table.setCellWidget(0, 3, qr_label)

    def update_qr_text_visibility(self, state):
        self.qr_text_input.setEnabled(state == Qt.CheckState.Checked)

    def show_temporary_message(self, message, timeout=2000):
        self.temp_message = QLabel(message, self)
        self.temp_message.setStyleSheet("background-color: #d3d3d3; border: 1px solid black;")  # Tom de cinza
        self.temp_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_message.setFixedSize(200, 50)
        self.temp_message.move((self.width() - self.temp_message.width()) // 2, (self.height() - self.temp_message.height()) // 2)
        self.temp_message.show()
        
        QTimer.singleShot(timeout, self.temp_message.close)

    def show_context_menu_history(self, position):
        menu = QMenu()
        copy_original_action = menu.addAction("Copiar URL Original")
        copy_short_action = menu.addAction("Copiar URL Encurtada")
        copy_alt_action = menu.addAction("Copiar URL Alternativa")
        copy_qr_action = menu.addAction("Copiar QR Code")
        action = menu.exec(self.history_table.mapToGlobal(position))
        selected_items = self.history_table.selectedItems()

        if action == copy_original_action and selected_items:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_items[0].text())
        elif action == copy_short_action and selected_items:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_items[1].text())
        elif action == copy_alt_action and selected_items:
            clipboard = QApplication.clipboard()
            clipboard.setText(selected_items[2].text())
        elif action == copy_qr_action:
            row = self.history_table.currentRow()
            if row >= 0:
                qr_label = self.history_table.cellWidget(row, 3)
                if qr_label and isinstance(qr_label, QLabel):
                    pixmap = qr_label.pixmap()
                    if pixmap and not pixmap.isNull():
                        clipboard = QApplication.clipboard()
                        clipboard.setPixmap(pixmap)

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

    def copy_qr_code_to_clipboard(self):
        if self.last_generated_qr:
            clipboard = QApplication.clipboard()
            qr_pixmap = self.pil_image_to_qpixmap(self.last_generated_qr)
            clipboard.setPixmap(qr_pixmap)

    def generate_qr_code(self, url):
        # Gerar o QR Code com um tamanho fixo
        qr = qrcode.QRCode(
            version=1,  # Tamanho fixo (versão 1)
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,  # Tamanho dos "pixels" do QR Code
            border=4,     # Margem do QR Code
        )
        qr.add_data(url)
        qr.make(fit=True)

        # Gerar a imagem do QR Code e redimensionar para um tamanho fixo (250x250 pixels)
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        fixed_size = (250, 250)
        img = img.resize(fixed_size, Image.ANTIALIAS)

        # Criar uma nova imagem para adicionar o texto abaixo do QR Code
        new_height = img.size[1] + 50
        new_img = Image.new("RGB", (img.size[0], new_height), (255, 255, 255))
        new_img.paste(img, (0, 0))

        draw = ImageDraw.Draw(new_img)
        qr_text = self.qr_text_input.text() if self.qr_text_input.isEnabled() else ""

        if qr_text:
            # Ajustar o tamanho da fonte dependendo do sistema operacional
            if platform.system() == "Windows":
                font_size = 16  # Tamanho ajustado para Windows
            else:
                font_size = 16  # Tamanho ajustado para macOS

            try:
                # Primeira tentativa: carregar Arial pelo nome genérico
                font = ImageFont.truetype("arial.ttf", font_size)
            except IOError:
                try:
                    # Segunda tentativa: caminho específico do macOS
                    font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
                except IOError:
                    try:
                        # Terceira tentativa: caminho específico do Windows
                        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", font_size)
                    except IOError:
                        # Fallback final: usar a fonte padrão do Pillow
                        font = ImageFont.load_default()

            # Centralizar o texto na parte inferior do QR Code
            bbox = draw.textbbox((0, 0), qr_text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            position = ((new_img.size[0] - text_width) // 2, img.size[1] + 10)
            draw.text(position, qr_text, fill=(0, 0, 0), font=font)

        # Armazenar o QR Code gerado para uso posterior
        self.last_generated_qr = new_img
        return new_img
    
    def pil_image_to_qpixmap(self, pil_image):
        bytes_io = io.BytesIO()
        pil_image.save(bytes_io, 'PNG', quality=100)  # Aumentada a qualidade
        bytes_io.seek(0)        
        return QPixmap.fromImage(QImage.fromData(bytes_io.getvalue(), 'PNG'))


def main():
    app = QApplication(sys.argv)
    window = URLShortenerApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()