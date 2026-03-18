import sys
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import threading
from datetime import datetime
import json
import random
import hashlib
import base64
from collections import defaultdict
from queue import Queue
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import re
from PIL import Image
from io import BytesIO

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit,
    QFileDialog, QSpinBox, QCheckBox, QGroupBox, QGridLayout,
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QSplitter, QTreeWidget, QTreeWidgetItem,
    QMenuBar, QMenu, QStatusBar, QToolBar, QDialog, QDialogButtonBox,
    QFormLayout, QScrollArea, QFrame, QProgressDialog, QStyle,
    QListWidget, QListWidgetItem, QApplication, QSizePolicy
)
from PySide6.QtCore import (
    Qt, QThread, Signal, QTimer, QSettings, QUrl, QSize, QByteArray, QMutex, QPoint
)
from PySide6.QtGui import (
    QIcon, QPixmap, QAction, QFont, QColor, QPalette, QTextCursor,
    QTextDocument, QImage, QBrush, QPainter, QLinearGradient
)

# Style moderne amélioré avec barre de progression visible
MODERN_STYLESHEET = """
QMainWindow { 
    background-color: #1e1e1e; 
    font-family: 'Segoe UI', Arial, sans-serif;
}
QWidget { 
    background-color: #1e1e1e; 
    color: #ffffff; 
}
QGroupBox { 
    border: 2px solid #3d3d3d; 
    border-radius: 8px; 
    margin-top: 1.5ex; 
    font-weight: bold;
    font-size: 13px;
    padding-top: 10px;
}
QGroupBox::title { 
    subcontrol-origin: margin; 
    left: 10px; 
    padding: 0 10px; 
    color: #ffaa00;
    background-color: #1e1e1e;
}
QLineEdit, QTextEdit, QSpinBox, QComboBox, QListWidget, QTreeWidget, QTableWidget {
    border: 2px solid #3d3d3d; 
    border-radius: 5px; 
    padding: 8px; 
    background-color: #2d2d2d;
    selection-background-color: #ffaa00;
    selection-color: #1e1e1e;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #ffaa00;
}
QPushButton {
    background-color: #ffaa00; 
    color: #1e1e1e; 
    border: none; 
    border-radius: 5px; 
    padding: 10px 20px; 
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover { 
    background-color: #ffbb22; 
}
QPushButton:pressed { 
    background-color: #ff9900; 
}
QPushButton:disabled { 
    background-color: #4a4a4a; 
    color: #888888; 
}
/* Barre de progression améliorée */
QProgressBar {
    border: 2px solid #3d3d3d;
    border-radius: 8px;
    text-align: center;
    height: 25px;
    font-weight: bold;
    color: white;
    background-color: #2d2d2d;
}
QProgressBar::chunk {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                               stop: 0 #ffaa00, stop: 1 #ffdd55);
    border-radius: 6px;
    margin: 1px;
}
QProgressBar#detailed_progress {
    height: 30px;
    font-size: 13px;
}
QProgressBar#small_progress {
    height: 20px;
    font-size: 11px;
}
QTableWidget { 
    border: 2px solid #3d3d3d; 
    gridline-color: #3d3d3d;
    alternate-background-color: #2a2a2a;
}
QHeaderView::section { 
    background-color: #3d3d3d; 
    padding: 8px; 
    border: 1px solid #1e1e1e;
    font-weight: bold;
}
QTabWidget::pane { 
    border: 2px solid #3d3d3d; 
    border-radius: 5px;
    top: -1px;
}
QTabBar::tab { 
    background-color: #3d3d3d; 
    padding: 10px 20px; 
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}
QTabBar::tab:selected { 
    background-color: #ffaa00; 
    color: #1e1e1e; 
}
QTabBar::tab:hover:!selected { 
    background-color: #4d4d4d; 
}
QStatusBar { 
    background-color: #3d3d3d; 
    color: #ffffff;
}
QTreeWidget::item:selected, QTableWidget::item:selected {
    background-color: #ffaa00;
    color: #1e1e1e;
}
QScrollBar:vertical {
    border: none;
    background-color: #2d2d2d;
    width: 14px;
    border-radius: 7px;
}
QScrollBar::handle:vertical {
    background-color: #ffaa00;
    border-radius: 7px;
    min-height: 30px;
}
QScrollBar::handle:vertical:hover {
    background-color: #ffbb22;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}
QScrollBar:horizontal {
    border: none;
    background-color: #2d2d2d;
    height: 14px;
    border-radius: 7px;
}
QScrollBar::handle:horizontal {
    background-color: #ffaa00;
    border-radius: 7px;
    min-width: 30px;
}
QScrollBar::handle:horizontal:hover {
    background-color: #ffbb22;
}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
    border: none;
    background: none;
}
QScrollArea {
    border: none;
    background-color: #1e1e1e;
}
QScrollArea > QWidget > QWidget {
    background-color: #1e1e1e;
}
/* Style pour les widgets de progression */
.progress-container {
    background-color: #2d2d2d;
    border-radius: 10px;
    padding: 15px;
    margin: 10px;
}
.progress-label {
    color: #ffaa00;
    font-weight: bold;
    font-size: 14px;
}
.progress-value {
    color: #ffffff;
    font-size: 13px;
}
/* Splitter handle */
QSplitter::handle {
    background-color: #3d3d3d;
    width: 2px;
}
QSplitter::handle:hover {
    background-color: #ffaa00;
}
"""


class EnhancedProgressBar(QWidget):
    """Widget de progression amélioré avec plusieurs barres"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("progress_container")
        self.setStyleSheet("""
            #progress_container {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 10px;
                margin: 5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # Barre de progression principale
        main_progress_layout = QHBoxLayout()
        self.main_label = QLabel("Progression globale:")
        self.main_label.setStyleSheet("color: #ffaa00; font-weight: bold; min-width: 120px;")
        main_progress_layout.addWidget(self.main_label)

        self.main_progress = QProgressBar()
        self.main_progress.setObjectName("detailed_progress")
        self.main_progress.setMinimum(0)
        self.main_progress.setMaximum(100)
        self.main_progress.setValue(0)
        self.main_progress.setFormat("%p% (%v/%m)")
        main_progress_layout.addWidget(self.main_progress)

        self.main_value = QLabel("0/0")
        self.main_value.setStyleSheet("color: #ffffff; min-width: 60px;")
        main_progress_layout.addWidget(self.main_value)

        layout.addLayout(main_progress_layout)

        # Barre de progression secondaire (cachée par défaut)
        self.secondary_container = QWidget()
        secondary_layout = QHBoxLayout(self.secondary_container)
        secondary_layout.setContentsMargins(0, 0, 0, 0)

        self.secondary_label = QLabel("Opération en cours:")
        self.secondary_label.setStyleSheet("color: #888888; min-width: 120px;")
        secondary_layout.addWidget(self.secondary_label)

        self.secondary_progress = QProgressBar()
        self.secondary_progress.setObjectName("small_progress")
        self.secondary_progress.setMinimum(0)
        self.secondary_progress.setMaximum(100)
        self.secondary_progress.setValue(0)
        self.secondary_progress.setFormat("%p%")
        secondary_layout.addWidget(self.secondary_progress)

        self.secondary_value = QLabel("0/0")
        self.secondary_value.setStyleSheet("color: #888888; min-width: 60px;")
        secondary_layout.addWidget(self.secondary_value)

        layout.addWidget(self.secondary_container)
        self.secondary_container.hide()

        # Indicateur de vitesse
        self.speed_label = QLabel("")
        self.speed_label.setStyleSheet("color: #888888; font-size: 11px;")
        self.speed_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.speed_label)

    def set_main_progress(self, value, maximum=None):
        """Met à jour la barre principale"""
        if maximum is not None:
            self.main_progress.setMaximum(maximum)
        self.main_progress.setValue(value)
        self.main_value.setText(f"{value}/{self.main_progress.maximum()}")

    def set_secondary_progress(self, value, maximum, label=""):
        """Met à jour la barre secondaire"""
        self.secondary_container.show()
        if label:
            self.secondary_label.setText(label)
        self.secondary_progress.setMaximum(maximum)
        self.secondary_progress.setValue(value)
        self.secondary_value.setText(f"{value}/{maximum}")

    def hide_secondary(self):
        """Cache la barre secondaire"""
        self.secondary_container.hide()

    def set_speed(self, speed_text):
        """Affiche la vitesse d'opération"""
        self.speed_label.setText(speed_text)


class ImageClassifier:
    """Classe pour classifier automatiquement les images"""

    CATEGORY_KEYWORDS = {
        'logo': ['logo', 'brand', 'marque', 'logotype', 'header-logo', 'footer-logo'],
        'icone': ['icon', 'ico', 'favicon', 'social-icon', 'menu-icon', 'button-icon'],
        'banniere': ['banner', 'header', 'hero', 'cover', 'slide', 'carousel', 'bandeau'],
        'produit': ['product', 'shop', 'catalog', 'item', 'article', 'goods', 'merchandise'],
        'photo': ['photo', 'photography', 'gallery', 'image', 'picture', 'img', 'portfolio'],
        'avatar': ['avatar', 'profile', 'user', 'member', 'team', 'author'],
        'background': ['background', 'bg', 'wallpaper', 'texture', 'pattern', 'backdrop'],
        'bouton': ['button', 'btn', 'cta', 'call-to-action', 'download-btn'],
        'social': ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'social'],
        'drapeau': ['flag', 'lang', 'language', 'country', 'france', 'english'],
        'illustration': ['illustration', 'drawing', 'sketch', 'vector', 'art', 'graphic'],
        'carte': ['map', 'location', 'place', 'gps', 'geo'],
        'qr-code': ['qr', 'qrcode', 'barcode'],
        'spinner': ['spinner', 'loader', 'loading', 'ajax-loader', 'preloader'],
        'separateur': ['separator', 'divider', 'line'],
        'badge': ['badge', 'label', 'tag', 'stamp', 'certified'],
        'certification': ['certif', 'guarantee', 'warranty', 'seal', 'trust'],
        'publicite': ['ad', 'ads', 'advertisement', 'promo', 'banner-ad'],
        'infographie': ['infographic', 'chart', 'graph', 'diagram', 'stats'],
        'emoji': ['emoji', 'smiley', 'emoticon']
    }

    URL_PATTERNS = {
        'logo': [r'logo', r'brand', r'marque'],
        'icone': [r'icon', r'favicon', r'sprite'],
        'avatar': [r'avatar', r'profile', r'user'],
        'banniere': [r'banner', r'header', r'hero'],
        'produit': [r'product', r'shop', r'catalog'],
        'social': [r'social', r'facebook', r'twitter']
    }

    CATEGORY_COLORS = {
        'logo': '#FF6B6B',
        'icone': '#4ECDC4',
        'banniere': '#45B7D1',
        'produit': '#96CEB4',
        'photo': '#FFEAA7',
        'avatar': '#DDA0DD',
        'background': '#B0C4DE',
        'bouton': '#FAA275',
        'social': '#FFB347',
        'drapeau': '#A9A9A9',
        'illustration': '#B5EAD7',
        'carte': '#C7B198',
        'qr-code': '#59656F',
        'spinner': '#9C89B8',
        'separateur': '#B0B0B0',
        'badge': '#FADADD',
        'certification': '#C9E4DE',
        'publicite': '#FAD6A5',
        'infographie': '#B1C1C0',
        'emoji': '#FCE2C1',
        'data-embed': '#B39CD0',
        'image-encodee': '#C5A9DF',
        'vectoriel': '#A7C7E7',
        'png-transparent': '#B0E0E6',
        'miniature': '#D4B8B8',
        'petite-image': '#E3C9C9',
        'grande-image': '#C9A9A9',
        'gif-anime': '#A8D8EA',
        'gif-statique': '#AA96DA',
        'transparent': '#C5E0D8',
        'non-classe': '#CCCCCC'
    }

    @staticmethod
    def classify_image(img_info, downloaded_data=None):
        """Classifie une image en lui attribuant une catégorie"""
        scores = defaultdict(int)

        url_lower = img_info.url.lower()
        filename = os.path.basename(urlparse(img_info.url).path).lower()
        alt_text = img_info.alt.lower() if img_info.alt else ""
        title = img_info.title.lower() if img_info.title else ""

        # Score basé sur les patterns d'URL
        for category, patterns in ImageClassifier.URL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url_lower) or re.search(pattern, filename):
                    scores[category] += 5

        # Score basé sur les mots-clés
        for category, keywords in ImageClassifier.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in url_lower or keyword in filename:
                    scores[category] += 3
                if keyword in alt_text or keyword in title:
                    scores[category] += 4

        # Analyse des dimensions
        if img_info.width and img_info.height:
            try:
                w = int(img_info.width)
                h = int(img_info.height)

                if w < 50 and h < 50:
                    scores['icone'] += 3
                elif w > 800 and h > 600:
                    if 'banner' in url_lower or 'hero' in url_lower:
                        scores['banniere'] += 3
                    else:
                        scores['grande-image'] += 2
                elif 200 <= w <= 800 and 200 <= h <= 800:
                    if 'product' in url_lower:
                        scores['produit'] += 2
            except:
                pass

        # Analyse des données téléchargées
        if downloaded_data:
            try:
                img_pil = Image.open(BytesIO(downloaded_data))
                width, height = img_pil.size

                if img_pil.format == 'GIF':
                    try:
                        img_pil.seek(1)
                        scores['gif-anime'] += 5
                    except:
                        scores['gif-statique'] += 2

                if img_pil.mode == 'RGBA':
                    scores['transparent'] += 2
            except:
                pass

        if img_info.is_data:
            scores['data-embed'] += 3

        if not scores:
            return 'non-classe'

        # Retourner la meilleure catégorie
        best_category = max(scores.items(), key=lambda x: x[1])
        img_info.category = best_category[0]
        img_info.category_score = best_category[1]
        img_info.all_categories = dict(scores)

        return best_category[0]

    @staticmethod
    def get_category_color(category):
        return ImageClassifier.CATEGORY_COLORS.get(category, '#CCCCCC')

    @staticmethod
    def get_all_categories():
        return sorted(ImageClassifier.CATEGORY_COLORS.keys())


class ImageInfo:
    """Classe pour stocker les informations d'une image"""

    def __init__(self, url, source_page, alt="", title="", width="", height=""):
        self.url = url
        self.source_page = source_page
        self.alt = alt
        self.title = title
        self.width = width
        self.height = height
        self.downloaded = False
        self.local_path = ""
        self.file_size = 0
        self.is_data = url.startswith('data:image/')
        self.domain = urlparse(url).netloc if not self.is_data else "data-url"
        self.page_depth = 0
        self.category = "non-classe"
        self.category_score = 0
        self.all_categories = {}
        self.image_data = None
        self.download_error = None

    def to_dict(self):
        return {
            'url': self.url,
            'source_page': self.source_page,
            'alt': self.alt,
            'title': self.title,
            'width': self.width,
            'height': self.height,
            'downloaded': self.downloaded,
            'local_path': self.local_path,
            'file_size': self.file_size,
            'is_data': self.is_data,
            'domain': self.domain,
            'category': self.category,
            'category_score': self.category_score
        }


class ImagePreviewDialog(QDialog):
    """Dialogue amélioré pour l'aperçu des images"""

    def __init__(self, image_data, image_info, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Aperçu - {os.path.basename(image_info.url)}")
        self.setModal(True)
        self.setMinimumSize(1000, 800)
        self.setStyleSheet(MODERN_STYLESHEET)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # En-tête avec catégorie
        header_layout = QHBoxLayout()

        category_label = QLabel(f"Catégorie: {image_info.category}")
        category_label.setStyleSheet(f"""
            background-color: {ImageClassifier.get_category_color(image_info.category)};
            color: #1e1e1e;
            padding: 8px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 14px;
        """)
        header_layout.addWidget(category_label)

        if image_info.category_score > 0:
            score_label = QLabel(f"Score: {image_info.category_score}")
            score_label.setStyleSheet("""
                background-color: #3d3d3d;
                padding: 8px 15px;
                border-radius: 20px;
                font-size: 14px;
            """)
            header_layout.addWidget(score_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Splitter pour l'image et les infos
        splitter = QSplitter(Qt.Horizontal)

        # Zone image avec scroll
        image_widget = QWidget()
        image_layout = QVBoxLayout(image_widget)
        image_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(Qt.AlignCenter)
        scroll_area.setStyleSheet("QScrollArea { border: 2px solid #3d3d3d; border-radius: 5px; }")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(400, 300)

        # Charger et afficher l'image
        pixmap = None
        if isinstance(image_data, QPixmap):
            pixmap = image_data
        elif isinstance(image_data, bytes):
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
        elif isinstance(image_data, str) and image_data.startswith('data:image/'):
            try:
                if ';base64,' in image_data:
                    _, data = image_data.split(';base64,', 1)
                    img_data = base64.b64decode(data)
                    pixmap = QPixmap()
                    pixmap.loadFromData(img_data)
            except:
                pass

        if pixmap and not pixmap.isNull():
            # Redimensionner pour l'affichage
            if pixmap.width() > 800 or pixmap.height() > 600:
                pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            dimensions = f"{pixmap.width()} x {pixmap.height()} pixels"
        else:
            self.image_label.setText("❌ Impossible de charger l'image")
            self.image_label.setStyleSheet("color: #ff4444; font-size: 16px; padding: 50px;")
            dimensions = "Inconnues"

        scroll_area.setWidget(self.image_label)
        image_layout.addWidget(scroll_area)

        splitter.addWidget(image_widget)

        # Panneau d'informations
        info_widget = QWidget()
        info_widget.setMaximumWidth(350)
        info_layout = QVBoxLayout(info_widget)

        # Groupe informations principales
        main_info_group = QGroupBox("Informations principales")
        main_info_layout = QFormLayout(main_info_group)
        main_info_layout.setSpacing(10)

        # URL
        url_label = QLabel(image_info.url[:50] + "..." if len(image_info.url) > 50 else image_info.url)
        url_label.setWordWrap(True)
        url_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        main_info_layout.addRow("URL:", url_label)

        # Dimensions
        main_info_layout.addRow("Dimensions:", QLabel(dimensions))

        # Taille
        if image_info.file_size:
            size_str = f"{image_info.file_size / 1024:.1f} KB"
            if image_info.file_size > 1024 * 1024:
                size_str = f"{image_info.file_size / (1024 * 1024):.2f} MB"
            main_info_layout.addRow("Taille:", QLabel(size_str))

        # Type
        type_str = "Data URL" if image_info.is_data else "URL HTTP"
        main_info_layout.addRow("Type:", QLabel(type_str))

        # Domaine
        main_info_layout.addRow("Domaine:", QLabel(image_info.domain))

        info_layout.addWidget(main_info_group)

        # Groupe source
        source_group = QGroupBox("Source")
        source_layout = QFormLayout(source_group)

        # Page source
        source_label = QLabel(image_info.source_page)
        source_label.setWordWrap(True)
        source_layout.addRow("Page:", source_label)

        # Profondeur
        source_layout.addRow("Profondeur:", QLabel(str(image_info.page_depth)))

        # Alt text
        if image_info.alt:
            source_layout.addRow("Alt:", QLabel(image_info.alt[:100]))

        # Title
        if image_info.title:
            source_layout.addRow("Title:", QLabel(image_info.title[:100]))

        info_layout.addWidget(source_group)

        # Groupe classification
        if image_info.all_categories:
            class_group = QGroupBox("Autres catégories possibles")
            class_layout = QVBoxLayout(class_group)

            for cat, score in sorted(image_info.all_categories.items(),
                                     key=lambda x: x[1], reverse=True)[:10]:
                if cat != image_info.category:
                    cat_label = QLabel(f"• {cat}: {score}")
                    cat_label.setStyleSheet(f"color: {ImageClassifier.get_category_color(cat)};")
                    class_layout.addWidget(cat_label)

            info_layout.addWidget(class_group)

        info_layout.addStretch()

        # Boutons d'action
        action_layout = QHBoxLayout()

        download_btn = QPushButton("⬇️ Télécharger")
        download_btn.clicked.connect(lambda: self.download_image(image_info))
        action_layout.addWidget(download_btn)

        copy_url_btn = QPushButton("📋 Copier URL")
        copy_url_btn.clicked.connect(lambda: QApplication.clipboard().setText(image_info.url))
        action_layout.addWidget(copy_url_btn)

        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        action_layout.addWidget(close_btn)

        info_layout.addLayout(action_layout)

        splitter.addWidget(info_widget)
        splitter.setSizes([650, 350])

        layout.addWidget(splitter)

    def download_image(self, image_info):
        """Télécharge l'image"""
        self.accept()


class LogTextEdit(QTextEdit):
    """QTextEdit personnalisé avec coloration syntaxique"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.max_lines = 1000
        self.lines = []

        # Configuration de la coloration
        self.success_color = QColor("#00ff00")
        self.error_color = QColor("#ff4444")
        self.warning_color = QColor("#ffaa00")
        self.info_color = QColor("#888888")
        self.setReadOnly(True)

    def append_log(self, text, level="INFO"):
        """Ajoute un log avec niveau"""
        timestamp = datetime.now().strftime('%H:%M:%S')

        # Colorer selon le niveau
        if level == "SUCCESS":
            prefix = "✅"
            color = self.success_color
        elif level == "ERROR":
            prefix = "❌"
            color = self.error_color
        elif level == "WARNING":
            prefix = "⚠️"
            color = self.warning_color
        else:
            prefix = "ℹ️"
            color = self.info_color

        formatted_text = f"[{timestamp}] {prefix} {text}"

        # Ajouter à la liste
        self.lines.append(formatted_text)

        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]

        # Mettre à jour l'affichage
        self.setText('\n'.join(self.lines))

        # Scroll automatique vers le bas
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)


class RecursiveCrawler(QThread):
    """Crawler récursif amélioré"""

    progress_update = Signal(int, int)
    log_message = Signal(str, str)
    image_found = Signal(ImageInfo)
    page_found = Signal(str, int)
    crawler_complete = Signal(list)
    error_occurred = Signal(str)
    speed_update = Signal(str)

    def __init__(self, start_url, config):
        super().__init__()
        self.start_url = start_url
        self.config = config
        self.is_running = True
        self.mutex = QMutex()
        self.start_time = None
        self.pages_processed = 0

        self.pages_to_visit = Queue()
        self.pages_to_visit.put((start_url, 0))
        self.visited_pages = set()
        self.all_images = []
        self.image_urls_seen = set()

        self.max_pages = config.get('max_pages', 100)
        self.max_depth = config.get('max_depth', 5)
        self.timeout = config.get('timeout', 60)
        self.delay = config.get('delay', 1)
        self.include_subdomains = config.get('include_subdomains', False)
        self.base_domain = urlparse(start_url).netloc
        self.classify_immediately = config.get('classify_immediately', True)

        # Session HTTP optimisée
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]

    def run(self):
        self.start_time = time.time()
        try:
            pages_analyzed = 0
            self.log_message.emit(f"Début de l'exploration de {self.start_url}", "INFO")

            while not self.pages_to_visit.empty() and self.is_running:
                self.mutex.lock()
                if pages_analyzed >= self.max_pages:
                    self.mutex.unlock()
                    self.log_message.emit(f"Limite de {self.max_pages} pages atteinte", "WARNING")
                    break

                current_url, depth = self.pages_to_visit.get()

                if depth > self.max_depth:
                    self.mutex.unlock()
                    continue

                if current_url in self.visited_pages:
                    self.mutex.unlock()
                    continue

                self.visited_pages.add(current_url)
                pages_analyzed += 1
                self.pages_processed = pages_analyzed
                self.mutex.unlock()

                # Calculer la vitesse
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    speed = pages_analyzed / elapsed
                    self.speed_update.emit(f"Vitesse: {speed:.1f} pages/min")

                self.progress_update.emit(pages_analyzed, self.max_pages)
                self.page_found.emit(current_url, depth)

                self.analyze_page(current_url, depth)
                time.sleep(self.delay)

            self.log_message.emit(f"Exploration terminée: {len(self.all_images)} images trouvées", "SUCCESS")
            self.crawler_complete.emit(self.all_images)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def analyze_page(self, url, depth):
        """Analyse une page web"""
        try:
            headers = {'User-Agent': random.choice(self.user_agents)}
            response = self.session.get(url, timeout=self.timeout, headers=headers)

            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.content, 'html.parser')

            # Trouver toutes les images
            img_tags = soup.find_all('img')
            for img in img_tags:
                img_url = self.extract_image_url(img, url)
                if img_url and img_url not in self.image_urls_seen:
                    if self.is_valid_image(img_url):
                        img_info = ImageInfo(
                            url=img_url,
                            source_page=url,
                            alt=img.get('alt', ''),
                            title=img.get('title', ''),
                            width=img.get('width', ''),
                            height=img.get('height', '')
                        )
                        img_info.page_depth = depth

                        if self.classify_immediately:
                            category = ImageClassifier.classify_image(img_info)
                            img_info.category = category

                        self.mutex.lock()
                        self.all_images.append(img_info)
                        self.image_urls_seen.add(img_url)
                        self.mutex.unlock()

                        self.image_found.emit(img_info)

            # Trouver les liens pour continuer l'exploration
            if depth < self.max_depth:
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    full_url = self.normalize_url(href, url)

                    if full_url and self.should_follow_link(full_url):
                        self.mutex.lock()
                        if full_url not in self.visited_pages:
                            self.pages_to_visit.put((full_url, depth + 1))
                        self.mutex.unlock()

        except Exception as e:
            self.log_message.emit(f"Erreur sur {url}: {str(e)[:50]}", "ERROR")

    def extract_image_url(self, img_tag, base_url):
        """Extrait l'URL d'une image"""
        for attr in ['src', 'data-src', 'data-original', 'data-lazy-src']:
            url = img_tag.get(attr)
            if url:
                return self.normalize_url(url, base_url)

        # Gérer srcset
        srcset = img_tag.get('srcset')
        if srcset:
            parts = srcset.split(',')[0].strip().split(' ')[0]
            return self.normalize_url(parts, base_url)

        return None

    def normalize_url(self, url, base_url):
        """Normalise une URL"""
        if not url or url.startswith('#') or url.startswith('mailto:') or url.startswith('javascript:'):
            return None

        url = url.strip()

        if url.startswith('data:image/'):
            return url

        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = urljoin(base_url, url)
        elif not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)

        # Enlever les ancres
        if '#' in url:
            url = url.split('#')[0]

        return url

    def is_valid_image(self, url):
        """Vérifie si l'URL correspond à une image"""
        if url.startswith('data:image/'):
            return True

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.bmp', '.avif']
        ext = os.path.splitext(urlparse(url).path)[1].lower()
        return ext in image_extensions or not ext

    def should_follow_link(self, url):
        """Détermine si un lien doit être suivi"""
        try:
            parsed = urlparse(url)

            if parsed.scheme not in ['http', 'https']:
                return False

            if self.include_subdomains:
                return parsed.netloc.endswith(self.base_domain) or parsed.netloc == self.base_domain
            else:
                return parsed.netloc == self.base_domain

        except:
            return False

    def stop(self):
        self.is_running = False


class AllCategoriesDownloader(QThread):
    """Thread pour télécharger TOUTES les catégories en même temps"""

    progress_update = Signal(int, int)
    category_progress = Signal(str, int, int)
    log_message = Signal(str, str)
    download_complete = Signal(ImageInfo)
    all_complete = Signal(int, int)  # total_success, total_failed
    speed_update = Signal(str)

    def __init__(self, images, base_folder):
        super().__init__()
        self.images = images
        self.base_folder = base_folder
        self.is_running = True
        self.session = None
        self.mutex = QMutex()
        self.total_success = 0
        self.total_failed = 0
        self.start_time = None
        self.downloaded_bytes = 0

        # Organiser les images par catégorie
        self.images_by_category = defaultdict(list)
        for img in images:
            self.images_by_category[img.category].append(img)

    def run(self):
        self.start_time = time.time()
        try:
            self.session = requests.Session()
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })

            total_images = len(self.images)
            processed = 0

            self.log_message.emit(f"Début du téléchargement de TOUTES les catégories", "SUCCESS")
            self.log_message.emit(f"📂 {len(self.images_by_category)} catégories à traiter", "INFO")

            # Créer le dossier principal
            os.makedirs(self.base_folder, exist_ok=True)

            # Télécharger chaque catégorie
            for category, category_images in self.images_by_category.items():
                if not self.is_running:
                    break

                self.log_message.emit(f"Téléchargement de la catégorie: {category} ({len(category_images)} images)",
                                      "INFO")

                # Créer le dossier de la catégorie
                clean_category = self.clean_folder_name(category)
                category_folder = os.path.join(self.base_folder, clean_category)
                os.makedirs(category_folder, exist_ok=True)

                # Télécharger les images de cette catégorie
                category_success = 0
                category_failed = 0

                for i, img in enumerate(category_images):
                    if not self.is_running:
                        break

                    # Mise à jour progression globale
                    processed += 1
                    self.progress_update.emit(processed, total_images)

                    # Progression de la catégorie
                    self.category_progress.emit(category, i + 1, len(category_images))

                    # Calculer la vitesse
                    elapsed = time.time() - self.start_time
                    if elapsed > 0 and self.downloaded_bytes > 0:
                        speed = self.downloaded_bytes / elapsed / 1024  # KB/s
                        self.speed_update.emit(f"Vitesse: {speed:.1f} KB/s")

                    try:
                        if img.is_data:
                            success = self.download_data_image(img, category_folder)
                        else:
                            success = self.download_http_image(img, category_folder)

                        if success:
                            self.mutex.lock()
                            self.total_success += 1
                            category_success += 1
                            img.downloaded = True
                            self.mutex.unlock()
                            self.download_complete.emit(img)
                        else:
                            self.mutex.lock()
                            self.total_failed += 1
                            category_failed += 1
                            self.mutex.unlock()

                    except Exception as e:
                        self.log_message.emit(f"Erreur: {str(e)[:50]}", "ERROR")
                        self.mutex.lock()
                        self.total_failed += 1
                        category_failed += 1
                        self.mutex.unlock()

                    time.sleep(0.1)  # Petit délai

                self.log_message.emit(
                    f"Catégorie {category} terminée: {category_success}/{len(category_images)} réussis",
                    "SUCCESS" if category_failed == 0 else "WARNING"
                )

            self.log_message.emit(
                f"Téléchargement complet terminé: {self.total_success}/{total_images} images",
                "SUCCESS"
            )
            self.all_complete.emit(self.total_success, self.total_failed)

        except Exception as e:
            self.log_message.emit(f"Erreur globale: {str(e)}", "ERROR")

    def download_data_image(self, img, folder_path):
        """Télécharge une image Data URL"""
        try:
            img_data = self.extract_data_image(img.url)
            if img_data:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]
                filename = f"data_image_{timestamp}.png"
                filepath = os.path.join(folder_path, filename)
                filepath = self.get_unique_filename(filepath)

                with open(filepath, 'wb') as f:
                    f.write(img_data)

                img.local_path = filepath
                img.file_size = len(img_data)

                self.mutex.lock()
                self.downloaded_bytes += img.file_size
                self.mutex.unlock()

                return True
        except:
            pass
        return False

    def download_http_image(self, img, folder_path):
        """Télécharge une image HTTP"""
        try:
            response = self.session.get(
                img.url,
                timeout=30,
                stream=True,
                headers={'User-Agent': 'Mozilla/5.0'}
            )

            if response.status_code == 200:
                content_type = response.headers.get('content-type', '')
                ext = self.get_extension(content_type, img.url)

                # Générer un nom de fichier
                base_name = os.path.basename(img.url.split('?')[0])
                if not base_name or base_name == '':
                    base_name = f"image_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                else:
                    base_name = self.clean_filename(base_name)

                filename = base_name
                if not filename.endswith(ext):
                    filename += ext

                filepath = os.path.join(folder_path, filename)
                filepath = self.get_unique_filename(filepath)

                file_size = 0
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            file_size += len(chunk)

                img.local_path = filepath
                img.file_size = file_size

                self.mutex.lock()
                self.downloaded_bytes += file_size
                self.mutex.unlock()

                return True
        except:
            pass
        return False

    def extract_data_image(self, url):
        """Extrait les données d'une Data URL"""
        try:
            if ';base64,' in url:
                _, data = url.split(';base64,', 1)
                return base64.b64decode(data)
        except:
            pass
        return None

    def get_extension(self, content_type, url):
        """Détermine l'extension du fichier"""
        content_map = {
            'image/jpeg': '.jpg',
            'image/jpg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
            'image/x-icon': '.ico',
            'image/bmp': '.bmp',
            'image/avif': '.avif'
        }

        for ct, ext in content_map.items():
            if ct in content_type.lower():
                return ext

        # Vérifier l'extension dans l'URL
        path = urlparse(url).path
        ext = os.path.splitext(path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico', '.bmp', '.avif']:
            return ext

        return '.jpg'

    def clean_folder_name(self, name):
        """Nettoie un nom de dossier"""
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        name = name.replace(' ', '_')
        name = ''.join(char for char in name if ord(char) >= 32)
        if len(name) > 50:
            name = name[:50]
        return name or "dossier"

    def clean_filename(self, filename):
        """Nettoie un nom de fichier"""
        filename = filename.split('?')[0]
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        filename = ''.join(char for char in filename if ord(char) >= 32)
        if len(filename) > 100:
            name, ext = os.path.splitext(filename)
            filename = name[:95] + ext
        return filename

    def get_unique_filename(self, filepath):
        """Génère un nom de fichier unique"""
        if not os.path.exists(filepath):
            return filepath

        base, ext = os.path.splitext(filepath)
        counter = 1
        while os.path.exists(f"{base}_{counter}{ext}"):
            counter += 1
        return f"{base}_{counter}{ext}"

    def stop(self):
        self.is_running = False


class CategoryCard(QFrame):
    """Widget carte pour afficher une catégorie"""

    download_clicked = Signal(str)

    def __init__(self, category, count, downloaded=0, color="#CCCCCC"):
        super().__init__()
        self.category = category
        self.setFrameStyle(QFrame.Box)
        self.setLineWidth(2)
        self.setStyleSheet(f"""
            CategoryCard {{
                background-color: #2d2d2d;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 10px;
            }}
            CategoryCard:hover {{
                background-color: #3d3d3d;
                border-width: 3px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(5)

        # En-tête avec couleur
        header_layout = QHBoxLayout()

        color_dot = QLabel()
        color_dot.setFixedSize(16, 16)
        color_dot.setStyleSheet(f"background-color: {color}; border-radius: 8px;")
        header_layout.addWidget(color_dot)

        category_label = QLabel(category.upper())
        category_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(category_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Statistiques
        stats_layout = QHBoxLayout()

        count_label = QLabel(f"📊 {count}")
        count_label.setStyleSheet("font-size: 12px; color: #888888;")
        stats_layout.addWidget(count_label)

        if downloaded > 0:
            downloaded_label = QLabel(f"✓ {downloaded}")
            downloaded_label.setStyleSheet("font-size: 12px; color: #00ff00;")
            stats_layout.addWidget(downloaded_label)

        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Barre de progression visuelle
        if count > 0:
            progress_frame = QFrame()
            progress_frame.setFixedHeight(6)
            progress_frame.setStyleSheet("background-color: #3d3d3d; border-radius: 3px;")

            progress_layout = QHBoxLayout(progress_frame)
            progress_layout.setContentsMargins(0, 0, 0, 0)

            self.progress_bar = QFrame()
            self.progress_bar.setFixedHeight(6)
            self.progress_bar.setFixedWidth(0)
            self.progress_bar.setStyleSheet(f"background-color: {color}; border-radius: 3px;")

            progress_layout.addWidget(self.progress_bar)
            progress_layout.addStretch()

            layout.addWidget(progress_frame)

        # Bouton de téléchargement
        download_btn = QPushButton("📥 Télécharger")
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffaa00;
                color: #1e1e1e;
                padding: 8px;
                font-size: 12px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #ffbb22;
            }
        """)
        download_btn.clicked.connect(lambda: self.download_clicked.emit(category))
        layout.addWidget(download_btn)

        self.setFixedSize(220, 160)

    def update_progress(self, current, total):
        """Met à jour la barre de progression"""
        if total > 0:
            width_percent = int((current / total) * 200)  # 200px est la largeur de la carte
            self.progress_bar.setFixedWidth(min(width_percent, 200))


class ScrollableCategoriesWidget(QScrollArea):
    """Widget avec scroll pour afficher toutes les catégories"""

    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Widget conteneur
        self.container = QWidget()
        self.setWidget(self.container)

        # Layout avec grille adaptable
        self.layout = QGridLayout(self.container)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.cards = {}
        self.current_row = 0
        self.current_col = 0
        self.max_cols = 4  # Nombre de cartes par ligne

    def add_category_card(self, category, card):
        """Ajoute une carte de catégorie"""
        self.cards[category] = card
        self.layout.addWidget(card, self.current_row, self.current_col)

        self.current_col += 1
        if self.current_col >= self.max_cols:
            self.current_col = 0
            self.current_row += 1

    def clear_cards(self):
        """Supprime toutes les cartes"""
        for card in self.cards.values():
            card.deleteLater()
        self.cards.clear()
        self.current_row = 0
        self.current_col = 0

    def update_category_progress(self, category, current, total):
        """Met à jour la progression d'une catégorie"""
        if category in self.cards:
            self.cards[category].update_progress(current, total)


class MainWindow(QMainWindow):
    """Fenêtre principale améliorée avec barre de progression visible"""

    def __init__(self):
        super().__init__()
        self.images = []
        self.image_cache = {}
        self.crawler_thread = None
        self.downloader_thread = None
        self.settings = QSettings("ImageExtractor", "Professional")
        self.current_download_folder = ""

        self.init_ui()
        self.load_settings()
        self.setup_connections()

    def init_ui(self):
        self.setWindowTitle("Extracteur d'Images Intelligent - Classification Automatique")
        self.setGeometry(100, 100, 1800, 1000)
        self.setStyleSheet(MODERN_STYLESHEET)

        self.create_menu_bar()
        self.create_toolbar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Barre d'URL moderne
        url_widget = QWidget()
        url_widget.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 5px;
            }
        """)
        url_layout = QHBoxLayout(url_widget)
        url_layout.setContentsMargins(10, 10, 10, 10)

        url_label = QLabel("🌐")
        url_label.setStyleSheet("font-size: 20px;")
        url_layout.addWidget(url_label)

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://exemple.com")
        self.url_edit.setText(self.settings.value("last_url", "https://exemple.com"))
        self.url_edit.setMinimumHeight(40)
        url_layout.addWidget(self.url_edit)

        self.analyze_btn = QPushButton("🔍 Explorer le site")
        self.analyze_btn.setMinimumHeight(40)
        self.analyze_btn.setMinimumWidth(200)
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffaa00;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        url_layout.addWidget(self.analyze_btn)

        main_layout.addWidget(url_widget)

        # Widget de progression amélioré (toujours visible)
        self.progress_widget = EnhancedProgressBar()
        main_layout.addWidget(self.progress_widget)

        # Splitter principal avec ratios équilibrés
        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.setHandleWidth(2)
        main_splitter.setChildrenCollapsible(False)

        # Panneau gauche (Configuration) - 30%
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setSpacing(15)
        left_layout.setContentsMargins(5, 5, 5, 5)

        # Groupe Configuration
        config_group = QGroupBox("⚙️ Configuration")
        config_layout = QGridLayout(config_group)
        config_layout.setVerticalSpacing(15)

        config_layout.addWidget(QLabel("Pages max:"), 0, 0)
        self.max_pages_spin = QSpinBox()
        self.max_pages_spin.setRange(10, 1000)
        self.max_pages_spin.setValue(100)
        self.max_pages_spin.setSuffix(" pages")
        self.max_pages_spin.setMinimumHeight(30)
        config_layout.addWidget(self.max_pages_spin, 0, 1)

        config_layout.addWidget(QLabel("Profondeur:"), 1, 0)
        self.max_depth_spin = QSpinBox()
        self.max_depth_spin.setRange(1, 10)
        self.max_depth_spin.setValue(5)
        self.max_depth_spin.setMinimumHeight(30)
        config_layout.addWidget(self.max_depth_spin, 1, 1)

        config_layout.addWidget(QLabel("Délai:"), 2, 0)
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 5)
        self.delay_spin.setValue(1)
        self.delay_spin.setSuffix(" s")
        self.delay_spin.setMinimumHeight(30)
        config_layout.addWidget(self.delay_spin, 2, 1)

        self.subdomain_check = QCheckBox("Inclure les sous-domaines")
        self.subdomain_check.setChecked(False)
        self.subdomain_check.setMinimumHeight(30)
        config_layout.addWidget(self.subdomain_check, 3, 0, 1, 2)

        self.classify_check = QCheckBox("Classifier pendant l'exploration")
        self.classify_check.setChecked(True)
        self.classify_check.setMinimumHeight(30)
        config_layout.addWidget(self.classify_check, 4, 0, 1, 2)

        left_layout.addWidget(config_group)

        # Groupe Destination
        dest_group = QGroupBox("📁 Destination")
        dest_layout = QHBoxLayout(dest_group)

        self.folder_edit = QLineEdit()
        self.folder_edit.setText(self.settings.value("download_folder", "images_classees"))
        self.folder_edit.setMinimumHeight(35)
        dest_layout.addWidget(self.folder_edit)

        self.browse_btn = QPushButton("📂")
        self.browse_btn.setMaximumWidth(50)
        self.browse_btn.setMinimumHeight(35)
        dest_layout.addWidget(self.browse_btn)

        left_layout.addWidget(dest_group)

        # Groupe Statistiques
        stats_group = QGroupBox("📊 Statistiques")
        stats_layout = QVBoxLayout(stats_group)

        self.stats_text = QTextEdit()
        self.stats_text.setReadOnly(True)
        self.stats_text.setMaximumHeight(150)
        stats_layout.addWidget(self.stats_text)

        left_layout.addWidget(stats_group)

        # Groupe Pages explorées
        pages_group = QGroupBox("📄 Pages explorées")
        pages_layout = QVBoxLayout(pages_group)

        self.pages_list = QListWidget()
        self.pages_list.setMinimumHeight(150)
        pages_layout.addWidget(self.pages_list)

        left_layout.addWidget(pages_group)

        # Groupe Logs
        log_group = QGroupBox("📋 Journal")
        log_layout = QVBoxLayout(log_group)

        self.log_text = LogTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMinimumHeight(200)
        log_layout.addWidget(self.log_text)

        log_controls = QHBoxLayout()

        self.clear_log_btn = QPushButton("🗑️ Effacer")
        self.clear_log_btn.clicked.connect(self.clear_log)
        log_controls.addWidget(self.clear_log_btn)

        log_controls.addStretch()

        self.stop_btn = QPushButton("⏹️ Arrêter")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_operation)
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4444;
                color: white;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        """)
        log_controls.addWidget(self.stop_btn)

        log_layout.addLayout(log_controls)

        left_layout.addWidget(log_group)

        # Panneau droit avec onglets - 70%
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(5, 5, 5, 5)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Onglet Catégories avec SCROLL
        self.categories_tab = self.create_categories_tab()
        self.tabs.addTab(self.categories_tab, "🏷️ Catégories")

        # Onglet Toutes les images
        self.all_tab = self.create_all_images_tab()
        self.tabs.addTab(self.all_tab, "🖼️ Toutes les images")

        # Onglet Résumé
        self.summary_tab = self.create_summary_tab()
        self.tabs.addTab(self.summary_tab, "📈 Résumé")

        right_layout.addWidget(self.tabs)

        # Barre d'outils des actions
        action_bar = QWidget()
        action_bar.setStyleSheet("""
            QWidget {
                background-color: #2d2d2d;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        action_layout = QHBoxLayout(action_bar)
        action_layout.setContentsMargins(10, 5, 10, 5)

        self.download_all_btn = QPushButton("📥 Tout télécharger")
        self.download_all_btn.setMinimumHeight(35)
        self.download_all_btn.clicked.connect(self.download_all)
        action_layout.addWidget(self.download_all_btn)

        self.download_all_categories_btn = QPushButton("📦 Télécharger TOUTES les catégories")
        self.download_all_categories_btn.setMinimumHeight(35)
        self.download_all_categories_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.download_all_categories_btn.clicked.connect(self.download_all_categories)
        action_layout.addWidget(self.download_all_categories_btn)

        self.reclassify_btn = QPushButton("🔄 Reclassifier")
        self.reclassify_btn.setMinimumHeight(35)
        self.reclassify_btn.clicked.connect(self.reclassify_all_images)
        action_layout.addWidget(self.reclassify_btn)

        self.export_btn = QPushButton("📤 Exporter")
        self.export_btn.setMinimumHeight(35)
        self.export_btn.clicked.connect(self.export_image_list)
        action_layout.addWidget(self.export_btn)

        action_layout.addStretch()

        right_layout.addWidget(action_bar)

        # Assemblage du splitter avec ratios équilibrés
        main_splitter.addWidget(left_widget)
        main_splitter.addWidget(right_widget)
        main_splitter.setSizes([500, 1300])  # 30% - 70% approximativement

        main_layout.addWidget(main_splitter, 1)  # stretch factor 1 pour prendre tout l'espace

        # Barre de statut
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Prêt")

        self.update_button_states()

        # Timer pour animation de progression
        self.progress_timer = QTimer()
        self.progress_timer.timeout.connect(self.animate_progress)
        self.animation_value = 0

    def animate_progress(self):
        """Animation pour la barre de progression quand elle est active"""
        if self.crawler_thread or self.downloader_thread:
            self.animation_value = (self.animation_value + 1) % 100
            # Optionnel: ajouter un effet de pulsation

    def create_categories_tab(self):
        """Crée l'onglet des catégories avec SCROLL"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        # En-tête
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)

        title = QLabel("📦 Images par catégorie")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        header_layout.addWidget(title)

        # Compteur
        self.category_count_label = QLabel("")
        self.category_count_label.setStyleSheet("color: #888888;")
        header_layout.addWidget(self.category_count_label)

        header_layout.addStretch()

        # Bouton de rafraîchissement
        refresh_btn = QPushButton("🔄")
        refresh_btn.setMaximumWidth(40)
        refresh_btn.clicked.connect(self.update_categories_display)
        header_layout.addWidget(refresh_btn)

        layout.addWidget(header_widget)

        # Zone de défilement pour les cartes
        self.categories_scroll = ScrollableCategoriesWidget()
        layout.addWidget(self.categories_scroll, 1)  # stretch factor 1 pour prendre tout l'espace

        return tab

    def create_all_images_tab(self):
        """Crée l'onglet de toutes les images"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        # Barre de filtre
        filter_widget = QWidget()
        filter_widget.setStyleSheet("background-color: #2d2d2d; border-radius: 5px; padding: 5px;")
        filter_layout = QHBoxLayout(filter_widget)

        filter_layout.addWidget(QLabel("🔍 Filtrer par catégorie:"))

        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Toutes les catégories")
        self.filter_combo.currentTextChanged.connect(self.filter_by_category)
        self.filter_combo.setMinimumHeight(30)
        self.filter_combo.setMinimumWidth(200)
        filter_layout.addWidget(self.filter_combo)

        filter_layout.addStretch()

        # Compteur d'images
        self.images_count_label = QLabel("")
        self.images_count_label.setStyleSheet("color: #888888;")
        filter_layout.addWidget(self.images_count_label)

        layout.addWidget(filter_widget)

        # Tableau des images
        self.images_table = QTableWidget()
        self.images_table.setColumnCount(9)
        self.images_table.setHorizontalHeaderLabels([
            "Aperçu", "Catégorie", "Type", "Page source", "URL", "Dimensions", "Taille", "Statut", "Actions"
        ])
        self.images_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.images_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.images_table.setAlternatingRowColors(True)
        self.images_table.setSortingEnabled(True)
        self.images_table.verticalHeader().setVisible(False)
        layout.addWidget(self.images_table, 1)  # stretch factor 1

        return tab

    def create_summary_tab(self):
        """Crée l'onglet de résumé"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.5;
                background-color: #2d2d2d;
                border: 2px solid #3d3d3d;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.summary_text)

        return tab

    def create_menu_bar(self):
        """Crée la barre de menu"""
        menubar = self.menuBar()

        # Menu Fichier
        file_menu = menubar.addMenu("Fichier")

        export_action = QAction("Exporter la liste JSON", self)
        export_action.triggered.connect(self.export_image_list)
        file_menu.addAction(export_action)

        export_report_action = QAction("Exporter le rapport", self)
        export_report_action.triggered.connect(self.export_report)
        file_menu.addAction(export_report_action)

        file_menu.addSeparator()
        exit_action = QAction("Quitter", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menu Classification
        class_menu = menubar.addMenu("Classification")

        reclassify_action = QAction("Reclassifier toutes les images", self)
        reclassify_action.triggered.connect(self.reclassify_all_images)
        class_menu.addAction(reclassify_action)

        # Menu Affichage
        view_menu = menubar.addMenu("Affichage")

        toggle_progress_action = QAction("Afficher/Masquer progression", self)
        toggle_progress_action.setCheckable(True)
        toggle_progress_action.setChecked(True)
        toggle_progress_action.triggered.connect(
            lambda checked: self.progress_widget.setVisible(checked)
        )
        view_menu.addAction(toggle_progress_action)

        # Menu Aide
        help_menu = menubar.addMenu("Aide")
        about_action = QAction("À propos", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Crée la barre d'outils"""
        toolbar = QToolBar("Outils")
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        analyze_action = QAction("🔍 Explorer", self)
        analyze_action.triggered.connect(self.start_crawling)
        toolbar.addAction(analyze_action)

        download_action = QAction("📥 Télécharger tout", self)
        download_action.triggered.connect(self.download_all)
        toolbar.addAction(download_action)

        toolbar.addSeparator()

        reclassify_action = QAction("🔄 Reclassifier", self)
        reclassify_action.triggered.connect(self.reclassify_all_images)
        toolbar.addAction(reclassify_action)

        toolbar.addSeparator()

        stop_action = QAction("⏹️ Arrêter", self)
        stop_action.triggered.connect(self.stop_operation)
        toolbar.addAction(stop_action)

    def setup_connections(self):
        """Configure les connexions signaux/slots"""
        self.analyze_btn.clicked.connect(self.start_crawling)
        self.url_edit.returnPressed.connect(self.start_crawling)
        self.browse_btn.clicked.connect(self.browse_folder)

    def start_crawling(self):
        """Démarre l'exploration"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une URL")
            return

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_edit.setText(url)

        self.settings.setValue("last_url", url)

        # Réinitialiser les données
        self.images.clear()
        self.image_cache.clear()
        self.images_table.setRowCount(0)
        self.pages_list.clear()
        self.summary_text.clear()
        self.filter_combo.clear()
        self.filter_combo.addItem("Toutes les catégories")

        # Nettoyer les catégories
        self.categories_scroll.clear_cards()

        config = {
            'max_pages': self.max_pages_spin.value(),
            'max_depth': self.max_depth_spin.value(),
            'delay': self.delay_spin.value(),
            'timeout': 60,
            'include_subdomains': self.subdomain_check.isChecked(),
            'classify_immediately': self.classify_check.isChecked()
        }

        self.log_message(f"Exploration récursive de {url}", "INFO")

        # Initialiser la barre de progression
        self.progress_widget.set_main_progress(0, config['max_pages'])
        self.progress_widget.set_secondary_progress(0, 100, "Exploration en cours...")
        self.progress_widget.set_speed("")

        self.crawler_thread = RecursiveCrawler(url, config)
        self.crawler_thread.progress_update.connect(self.update_progress)
        self.crawler_thread.log_message.connect(self.log_message)
        self.crawler_thread.image_found.connect(self.add_image_to_table)
        self.crawler_thread.page_found.connect(self.add_page_to_list)
        self.crawler_thread.crawler_complete.connect(self.crawling_complete)
        self.crawler_thread.error_occurred.connect(self.show_error)
        self.crawler_thread.speed_update.connect(self.progress_widget.set_speed)
        self.crawler_thread.start()

        self.analyze_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_timer.start(100)  # Animation toutes les 100ms
        self.status_label = self.status_bar.currentMessage()  # Pour compatibilité
        self.status_bar.showMessage("Exploration en cours...")

    def add_page_to_list(self, url, depth):
        """Ajoute une page à la liste"""
        indent = "  " * depth
        self.pages_list.addItem(f"{indent}📄 [{depth}] {url}")
        self.pages_list.scrollToBottom()

    def add_image_to_table(self, img_info):
        """Ajoute une image au tableau"""
        row = self.images_table.rowCount()
        self.images_table.insertRow(row)
        self.images.append(img_info)

        # Mettre à jour le filtre
        if self.filter_combo.findText(img_info.category) == -1:
            self.filter_combo.addItem(img_info.category)

        # Mettre à jour le compteur
        self.images_count_label.setText(f"Total: {len(self.images)} images")

        # Aperçu
        preview_label = QLabel()
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setMinimumSize(50, 50)
        preview_label.setMaximumSize(50, 50)
        preview_label.setStyleSheet("border: 1px solid #3d3d3d; background-color: #2b2b2b; border-radius: 3px;")
        preview_label.setText("🖼️")
        self.images_table.setCellWidget(row, 0, preview_label)

        # Catégorie
        category_item = QTableWidgetItem(img_info.category)
        color = ImageClassifier.get_category_color(img_info.category)
        category_item.setForeground(QBrush(QColor(color)))
        category_item.setFont(QFont("Arial", 9, QFont.Bold))
        category_item.setToolTip(f"Score: {img_info.category_score}")
        self.images_table.setItem(row, 1, category_item)

        # Type
        type_icon = "📦" if img_info.is_data else "🌐"
        type_item = QTableWidgetItem(type_icon)
        type_item.setTextAlignment(Qt.AlignCenter)
        type_item.setToolTip("Data URL" if img_info.is_data else "URL HTTP")
        self.images_table.setItem(row, 2, type_item)

        # Page source
        source = img_info.source_page
        if len(source) > 50:
            source = source[:50] + "..."
        source_item = QTableWidgetItem(source)
        source_item.setToolTip(img_info.source_page)
        self.images_table.setItem(row, 3, source_item)

        # URL
        url_text = img_info.url
        if len(url_text) > 50:
            if img_info.is_data:
                url_text = "Data URL"
            else:
                url_text = url_text[:50] + "..."
        url_item = QTableWidgetItem(url_text)
        url_item.setToolTip(img_info.url)
        self.images_table.setItem(row, 4, url_item)

        # Dimensions
        dims = f"{img_info.width}x{img_info.height}" if img_info.width and img_info.height else "-"
        self.images_table.setItem(row, 5, QTableWidgetItem(dims))

        # Taille
        size_text = f"{img_info.file_size / 1024:.1f} KB" if img_info.file_size else "-"
        self.images_table.setItem(row, 6, QTableWidgetItem(size_text))

        # Statut
        status = "✓" if img_info.downloaded else "○"
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignCenter)
        self.images_table.setItem(row, 7, status_item)

        # Actions
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(2, 2, 2, 2)
        actions_layout.setSpacing(2)

        preview_btn = QPushButton("👁️")
        preview_btn.setMaximumWidth(30)
        preview_btn.setToolTip("Aperçu")
        preview_btn.clicked.connect(lambda checked, r=row: self.show_image_preview(r))
        actions_layout.addWidget(preview_btn)

        download_btn = QPushButton("⬇️")
        download_btn.setMaximumWidth(30)
        download_btn.setToolTip("Télécharger")
        download_btn.clicked.connect(lambda checked, r=row: self.download_single(r))
        actions_layout.addWidget(download_btn)

        self.images_table.setCellWidget(row, 8, actions_widget)

        self.update_statistics()
        self.update_categories_display()

    def update_categories_display(self):
        """Met à jour l'affichage des catégories sous forme de cartes avec SCROLL"""
        self.categories_scroll.clear_cards()

        # Compter les images par catégorie
        categories = defaultdict(lambda: {'total': 0, 'downloaded': 0})
        for img in self.images:
            categories[img.category]['total'] += 1
            if img.downloaded:
                categories[img.category]['downloaded'] += 1

        # Trier par nombre d'images
        sorted_categories = sorted(categories.items(), key=lambda x: x[1]['total'], reverse=True)

        # Mettre à jour le compteur de catégories
        self.category_count_label.setText(f"{len(categories)} catégories")

        # Ajouter les cartes à la zone scrollable
        for category, stats in sorted_categories:
            color = ImageClassifier.get_category_color(category)
            card = CategoryCard(
                category,
                stats['total'],
                stats['downloaded'],
                color
            )
            card.download_clicked.connect(self.download_category)
            self.categories_scroll.add_category_card(category, card)

    def download_category(self, category):
        """Télécharge une catégorie spécifique"""
        category_images = [img for img in self.images if img.category == category]

        if not category_images:
            QMessageBox.information(self, "Info", f"Aucune image dans la catégorie {category}")
            return

        # Demander confirmation
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Télécharger {len(category_images)} images de la catégorie '{category}' ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Créer le dossier de destination
        base_folder = self.folder_edit.text().strip()
        if not base_folder:
            base_folder = "images_classees"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_folder = os.path.join(base_folder, f"categorie_{category}_{timestamp}")

        try:
            os.makedirs(download_folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer le dossier: {str(e)}")
            return

        # Démarrer le téléchargement
        self.start_download(category_images, download_folder, f"Téléchargement {category}")

    def download_all_categories(self):
        """Télécharge TOUTES les catégories dans des dossiers séparés"""
        if not self.images:
            QMessageBox.information(self, "Info", "Aucune image à télécharger")
            return

        total_images = len(self.images)
        categories = len(set(img.category for img in self.images))

        # Demander confirmation
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Télécharger TOUTES les images ({total_images} images dans {categories} catégories) ?\n\n"
            f"Les images seront organisées dans des dossiers par catégorie.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Créer le dossier principal
        base_folder = self.folder_edit.text().strip()
        if not base_folder:
            base_folder = "images_classees"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        main_folder = os.path.join(base_folder, f"toutes_categories_{timestamp}")

        try:
            os.makedirs(main_folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer le dossier: {str(e)}")
            return

        self.log_message(f"Dossier principal créé: {main_folder}", "INFO")
        self.current_download_folder = main_folder

        # Démarrer le téléchargement de toutes les catégories
        self.start_download(self.images, main_folder, "Téléchargement toutes catégories")

    def start_download(self, images, folder, operation_name):
        """Démarre un téléchargement avec progression"""
        self.downloader_thread = AllCategoriesDownloader(images, folder)
        self.downloader_thread.progress_update.connect(self.update_download_progress)
        self.downloader_thread.category_progress.connect(self.update_category_progress)
        self.downloader_thread.download_complete.connect(self.update_image_downloaded)
        self.downloader_thread.log_message.connect(self.log_message)
        self.downloader_thread.all_complete.connect(self.download_complete)
        self.downloader_thread.speed_update.connect(self.progress_widget.set_speed)
        self.downloader_thread.start()

        # Mettre à jour l'interface
        self.progress_widget.set_main_progress(0, len(images))
        self.progress_widget.set_secondary_progress(0, 100, operation_name)

        self.analyze_btn.setEnabled(False)
        self.download_all_btn.setEnabled(False)
        self.download_all_categories_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        self.log_message(f"Début du {operation_name} de {len(images)} images", "SUCCESS")
        self.status_bar.showMessage(f"{operation_name} en cours...")

    def update_category_progress(self, category, current, total):
        """Met à jour la progression d'une catégorie dans l'affichage"""
        self.categories_scroll.update_category_progress(category, current, total)
        self.progress_widget.set_secondary_progress(current, total, f"Catégorie: {category}")

    def show_image_preview(self, row):
        """Affiche l'aperçu d'une image"""
        if row < 0 or row >= len(self.images):
            return

        img_info = self.images[row]

        if img_info.url in self.image_cache:
            dialog = ImagePreviewDialog(self.image_cache[img_info.url], img_info, self)
            dialog.exec()
            return

        try:
            if img_info.is_data:
                if ';base64,' in img_info.url:
                    _, data = img_info.url.split(';base64,', 1)
                    img_data = base64.b64decode(data)
                    self.image_cache[img_info.url] = img_data
                    dialog = ImagePreviewDialog(img_data, img_info, self)
                    dialog.exec()
            else:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(img_info.url, timeout=30, headers=headers)

                if response.status_code == 200:
                    img_data = response.content
                    self.image_cache[img_info.url] = img_data
                    dialog = ImagePreviewDialog(img_data, img_info, self)
                    dialog.exec()
                else:
                    QMessageBox.warning(self, "Erreur", f"HTTP {response.status_code}")

        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur: {str(e)}")

    def reclassify_all_images(self):
        """Reclassifie toutes les images"""
        if not self.images:
            return

        self.log_message("Reclassification de toutes les images...", "INFO")

        for img in self.images:
            old_category = img.category
            new_category = ImageClassifier.classify_image(img)
            if old_category != new_category:
                self.log_message(f"  {old_category} → {new_category}", "INFO")

        # Mettre à jour l'affichage
        self.images_table.setRowCount(0)
        for img in self.images:
            self.add_image_to_table(img)

        self.update_categories_display()
        self.update_statistics()
        self.log_message("Reclassification terminée", "SUCCESS")

    def filter_by_category(self, category):
        """Filtre les images par catégorie"""
        if category == "Toutes les catégories" or not category:
            for row in range(self.images_table.rowCount()):
                self.images_table.setRowHidden(row, False)
        else:
            for row, img in enumerate(self.images):
                self.images_table.setRowHidden(row, img.category != category)

    def download_single(self, row):
        """Télécharge une seule image"""
        if row < len(self.images):
            self.download_images([self.images[row]])

    def download_all(self):
        """Télécharge toutes les images"""
        if not self.images:
            QMessageBox.information(self, "Info", "Aucune image à télécharger")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Télécharger toutes les images ({len(self.images)} images) ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.download_images(self.images)

    def download_images(self, images):
        """Télécharge une liste d'images"""
        folder = self.folder_edit.text().strip()
        if not folder:
            folder = "images_classees"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        download_folder = os.path.join(folder, f"download_{timestamp}")

        try:
            os.makedirs(download_folder, exist_ok=True)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de créer le dossier: {str(e)}")
            return

        self.log_message(f"Dossier de téléchargement: {download_folder}", "INFO")

        # Démarrer le téléchargement
        self.start_download(images, download_folder, "Téléchargement")

    def update_download_progress(self, current, total):
        """Met à jour la barre de progression"""
        self.progress_widget.set_main_progress(current, total)
        self.status_bar.showMessage(f"Téléchargement: {current}/{total}")

    def update_image_downloaded(self, img_info):
        """Met à jour le statut d'une image téléchargée"""
        for row, img in enumerate(self.images):
            if img.url == img_info.url:
                self.images[row] = img_info
                status_item = self.images_table.item(row, 7)
                if status_item:
                    status_item.setText("✓")

                size_item = self.images_table.item(row, 6)
                if size_item and img_info.file_size:
                    size_item.setText(f"{img_info.file_size / 1024:.1f} KB")
                break

        self.update_statistics()
        self.update_categories_display()

    def download_complete(self, success, failed):
        """Fin du téléchargement"""
        self.downloader_thread = None
        self.analyze_btn.setEnabled(True)
        self.download_all_btn.setEnabled(True)
        self.download_all_categories_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_widget.hide_secondary()
        self.progress_timer.stop()

        self.update_button_states()
        self.update_categories_display()
        self.log_message(f"Téléchargement terminé: {success} réussis, {failed} échecs", "SUCCESS")
        self.status_bar.showMessage("Téléchargement terminé")

    def all_categories_complete(self, success, failed):
        """Fin du téléchargement de toutes les catégories"""
        self.download_complete(success, failed)

        total = success + failed

        QMessageBox.information(
            self,
            "Téléchargement terminé",
            f"Téléchargement de toutes les catégories terminé!\n\n"
            f"✓ Réussis: {success}\n"
            f"✗ Échecs: {failed}\n"
            f"📁 Dossier: {self.current_download_folder}"
        )

    def update_statistics(self):
        """Met à jour les statistiques"""
        total = len(self.images)
        data_urls = sum(1 for img in self.images if img.is_data)
        http_urls = total - data_urls
        downloaded = sum(1 for img in self.images if img.downloaded)

        # Compter par catégorie
        categories = defaultdict(int)
        for img in self.images:
            categories[img.category] += 1

        stats = f"""
📊 STATISTIQUES
━━━━━━━━━━━━━━━━━━━━━━━━━━
Total images: {total}
├─ HTTP/HTTPS: {http_urls}
└─ Data URLs: {data_urls}

Téléchargées: {downloaded}

📂 RÉPARTITION PAR CATÉGORIE
"""

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            downloaded_count = sum(1 for img in self.images if img.category == category and img.downloaded)
            percentage = (count / total) * 100 if total > 0 else 0
            stats += f"\n{category}: {count} ({percentage:.1f}%) [✓ {downloaded_count}]"

        self.stats_text.setText(stats)

        # Mettre à jour le résumé
        summary = f"""
RAPPORT D'EXTRACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━
Date: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
URL: {self.url_edit.text()}
Pages explorées: {self.pages_list.count()}
Images trouvées: {total}

DÉTAIL PAR CATÉGORIE:
"""

        for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            summary += f"\n\n{category.upper()} ({count} images):"
            category_images = [img for img in self.images if img.category == category][:5]
            for img in category_images:
                summary += f"\n  • {os.path.basename(img.url)[:50]}"

        self.summary_text.setText(summary)

    def update_progress(self, current, total):
        """Met à jour la progression"""
        self.progress_widget.set_main_progress(current, total)
        self.progress_widget.set_secondary_progress(current, total, "Pages analysées")

    def crawling_complete(self, images):
        """Fin de l'exploration"""
        self.crawler_thread = None
        self.analyze_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_widget.hide_secondary()
        self.progress_timer.stop()

        self.log_message(f"Exploration terminée: {len(images)} images classifiées", "SUCCESS")
        self.update_button_states()
        self.update_categories_display()

        QMessageBox.information(
            self,
            "Exploration terminée",
            f"Exploration terminée!\n\n"
            f"📊 {len(images)} images trouvées\n"
            f"📂 {len(set(img.category for img in images))} catégories\n"
            f"📄 {self.pages_list.count()} pages analysées"
        )

        self.status_bar.showMessage("Exploration terminée")

    def stop_operation(self):
        """Arrête l'opération en cours"""
        if self.crawler_thread and self.crawler_thread.isRunning():
            self.crawler_thread.stop()
            self.crawler_thread.wait()

        if self.downloader_thread and self.downloader_thread.isRunning():
            self.downloader_thread.stop()
            self.downloader_thread.wait()

        self.analyze_btn.setEnabled(True)
        self.download_all_btn.setEnabled(True)
        self.download_all_categories_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_widget.hide_secondary()
        self.progress_timer.stop()

        self.log_message("Opération arrêtée", "WARNING")
        self.status_bar.showMessage("Opération arrêtée")

    def log_message(self, message, level="INFO"):
        """Ajoute un message au journal"""
        self.log_text.append_log(message, level)

    def clear_log(self):
        """Efface le journal"""
        self.log_text.clear()
        self.log_text.lines = []

    def show_error(self, message):
        """Affiche une erreur"""
        QMessageBox.critical(self, "Erreur", message)
        self.log_message(message, "ERROR")
        self.stop_operation()

    def browse_folder(self):
        """Ouvre un dialogue pour choisir un dossier"""
        folder = QFileDialog.getExistingDirectory(self, "Dossier destination", self.folder_edit.text())
        if folder:
            self.folder_edit.setText(folder)
            self.settings.setValue("download_folder", folder)

    def export_image_list(self):
        """Exporte la liste des images au format JSON"""
        if not self.images:
            QMessageBox.information(self, "Info", "Aucune image à exporter")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Exporter", "images_classees.json", "JSON (*.json)")
        if filename:
            data = [img.to_dict() for img in self.images]
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.log_message(f"Liste exportée vers {filename}", "SUCCESS")

    def export_report(self):
        """Exporte un rapport texte"""
        if not self.images:
            QMessageBox.information(self, "Info", "Aucune donnée à exporter")
            return

        filename, _ = QFileDialog.getSaveFileName(self, "Exporter le rapport", "rapport_classification.txt",
                                                  "Texte (*.txt)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"RAPPORT D'EXTRACTION AVEC CLASSIFICATION\n")
                f.write(f"{'=' * 50}\n")
                f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"URL de base: {self.url_edit.text()}\n")
                f.write(f"Pages explorées: {self.pages_list.count()}\n")
                f.write(f"Images trouvées: {len(self.images)}\n\n")

                categories = defaultdict(list)
                for img in self.images:
                    categories[img.category].append(img)

                for category, images in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
                    f.write(f"\n{category.upper()} ({len(images)} images):\n")
                    for img in images[:10]:
                        f.write(f"  - {img.url}\n")
                        f.write(f"    (source: {img.source_page})\n")

            self.log_message(f"Rapport exporté vers {filename}", "SUCCESS")

    def update_button_states(self):
        """Met à jour l'état des boutons"""
        has_images = len(self.images) > 0
        self.download_all_btn.setEnabled(has_images)
        self.download_all_categories_btn.setEnabled(has_images)
        self.export_btn.setEnabled(has_images)
        self.reclassify_btn.setEnabled(has_images)

    def load_settings(self):
        """Charge les paramètres"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def closeEvent(self, event):
        """Gère la fermeture de la fenêtre"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("last_url", self.url_edit.text())
        self.settings.setValue("download_folder", self.folder_edit.text())
        self.stop_operation()
        event.accept()

    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        QMessageBox.about(
            self,
            "À propos",
            """
            <h2>Extracteur d'Images Intelligent</h2>
            <p>Version 4.0.0</p>
            <p>Extraction et classification automatique d'images</p>

            <h3>🌟 Fonctionnalités</h3>
            <ul>
                <li>Exploration récursive de sites web</li>
                <li>Classification intelligente (25+ catégories)</li>
                <li>Téléchargement organisé par catégorie</li>
                <li>Interface avec SCROLL pour toutes les catégories</li>
                <li>Aperçu des images avec métadonnées</li>
                <li>Barre de progression améliorée avec vitesse</li>
            </ul>

            <h3>📊 Catégories détectées</h3>
            <p>Logo, Icône, Bannière, Produit, Photo, Avatar,<br>
            Background, Bouton, Social, Drapeau, Illustration,<br>
            Carte, QR Code, Spinner, Badge, et plus...</p>

            <p>© 2024</p>
            """
        )


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Image Extractor Pro")
    app.setApplicationDisplayName("Extracteur d'Images Intelligent")

    # Configuration pour éviter les erreurs d'encodage
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()