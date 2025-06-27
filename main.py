import sys
import os
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QScrollArea, QMainWindow,
    QListWidget, QListWidgetItem, QStackedLayout, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QFrame,
    QMessageBox, QInputDialog, QFileDialog, QDialog,
    QProgressBar, QSplashScreen, QGraphicsDropShadowEffect,
    QHeaderView, QSizePolicy, QTextEdit, QSpacerItem,
    QCheckBox, QSlider, QGroupBox, QFormLayout
)
from PyQt5.QtGui import (
    QPixmap, QIcon, QCursor, QFont, QColor, QFontDatabase, 
    QPainter, QLinearGradient, QPalette, QBrush
)
from PyQt5.QtCore import Qt, QTimer, QSize, QPoint, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Configuración de Matplotlib
plt.rcParams['toolbar'] = 'None'

# Colores y Temas Mejorados
COLOR_PRIMARY = "#FF6B35"
COLOR_SECONDARY = "#004E89"
COLOR_DARK = "#1A1A2E"
COLOR_LIGHT_BG = "#F7F9FC"
COLOR_ACCENT = "#FFD23F"
COLOR_SUCCESS = "#06D6A0"
COLOR_WARNING = "#F18701"
COLOR_ERROR = "#EF476F"
COLOR_GREY_TEXT = "#6C757D"
COLOR_BORDER = "#E9ECEF"

THEME_LIGHT = {
    "background": COLOR_LIGHT_BG,
    "text": COLOR_DARK,
    "primary": COLOR_PRIMARY,
    "secondary": COLOR_SECONDARY,
    "accent": COLOR_ACCENT,
    "success": COLOR_SUCCESS,
    "warning": COLOR_WARNING,
    "error": COLOR_ERROR,
    "card_bg": "#FFFFFF",
    "button_bg": COLOR_PRIMARY,
    "button_hover": "#FF8A65",
    "button_pressed": "#E64A19",
    "border": COLOR_BORDER,
    "header_bg": "#F8F9FA",
    "selection_bg": "#FFE0B2",
    "placeholder_text": "#9E9E9E",
    "dark": COLOR_DARK,
    "grey_text": COLOR_GREY_TEXT,
    "gradient_start": "#FF6B35",
    "gradient_end": "#F18701",
    "shadow": "rgba(0, 0, 0, 0.1)",
}

THEME_DARK = {
    "background": "#0F0F23",
    "text": "#E0E0E0",
    "primary": "#00D9FF",
    "secondary": "#7209B7",
    "accent": "#FFD23F",
    "success": "#06D6A0",
    "warning": "#F18701",
    "error": "#EF476F",
    "card_bg": "#16213E",
    "button_bg": "#00D9FF",
    "button_hover": "#33E1FF",
    "button_pressed": "#0099CC",
    "border": "#2A3F5F",
    "header_bg": "#1A1A2E",
    "selection_bg": "#7209B7",
    "placeholder_text": "#BDBDBD",
    "dark": "#0F0F23",
    "grey_text": "#BDBDBD",
    "gradient_start": "#00D9FF",
    "gradient_end": "#7209B7",
    "shadow": "rgba(0, 0, 0, 0.3)",
}

# Constantes
DEFAULT_IMAGE_PATH = "default.png"
DATA_FILE = "productos.json"
USER_DATA_FILE = "user_data.json"

# Variable global para el tema actual
current_theme = THEME_LIGHT

# Crear directorios necesarios
os.makedirs("images", exist_ok=True)
os.makedirs("icons", exist_ok=True)

def load_products():
    """Carga los productos desde un archivo JSON o usa datos predeterminados"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [tuple(p) for p in data]
        except Exception as e:
            print(f"Error cargando productos: {e}")
    
    # Datos de ejemplo
    return [
        ("Beef Ramen", 23.00, "img/beef_ramen.jpg", "Ramen", 12),
        ("Chicken Teriyaki", 18.50, "img/chicken_teriyaki.jpg", "Ramen", 8),
        ("Sushi Roll", 12.00, "img/sushi_roll.jpg", "Other", 20),
        ("Tofu Salad", 15.75, "img/tofu_salad.jpg", "Other", 5),
        ("Tempura Udon", 20.00, "img/tempura_udon.jpg", "Ramen", 6),
        ("Matcha Ice Cream", 7.50, "img/matcha_ice_cream.jpg", "Drink", 13),
        ("Miso Soup", 6.00, "img/miso_soup.jpg", "Ramen", 25),
        ("Green Tea", 4.50, "img/green_tea.jpg", "Drink", 9),
        ("Spicy Ramen", 22.00, "img/spicy_ramen.jpg", "Ramen", 14),
        ("Salmon Sashimi", 19.00, "img/salmon_sashimi.jpg", "Other", 7),
        ("Vegetable Gyoza", 10.00, "img/vegetable_gyoza.jpg", "Other", 10),
        ("Iced Coffee", 5.00, "img/iced_coffee.jpg", "Drink", 11),
        ("Fruit Mochi", 6.50, "img/fruit_mochi.jpg", "Other", 15),
        ("Pork Ramen", 24.00, "img/pork_ramen.jpg", "Ramen", 4),
        ("Bubble Tea", 6.00, "img/bubble_tea.jpeg", "Drink", 18),
        ("Shrimp Tempura", 17.50, "img/shrimp_tempura.jpg", "Other", 6),
        ("Yakisoba", 16.00, "img/yakisoba.jpg", "Ramen", 3),
        ("Coconut Water", 4.75, "img/coconut_water.jpg", "Drink", 20),
        ("Seaweed Salad", 9.00, "img/seaweed_salad.jpg", "Other", 2),
        ("Oolong Tea", 4.00, "img/oolong_tea.jpg", "Drink", 22),
    ]

def load_user_data():
    """Carga los datos del usuario"""
    default_data = {
        "name": "Administrador",
        "email": "admin@foodwizz.com",
        "business_name": "FoodWizz Restaurant",
        "phone": "+507 6007 8900",
        "address": "123 Food Street, Culinary City",
        "theme": "Claro",
        "notifications": True,
        "auto_backup": True,
        "language": "Español",
        "currency": "USD",
        "tax_rate": 7.5,
        "join_date": "2024-01-01",
        "total_sales": 125000,
        "total_orders": 1250,
        "favorite_category": "Ramen"
    }
    
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return default_data

def save_user_data(data):
    """Guarda los datos del usuario"""
    try:
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error guardando datos de usuario: {e}")

def save_products(products_list):
    """Guarda los productos en un archivo JSON"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(products_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        QMessageBox.critical(None, "Error al Guardar", f"No se pudo guardar los datos: {e}")

# Cargar datos iniciales
products = load_products()
user_data = load_user_data()

class ModernShadowEffect(QGraphicsDropShadowEffect):
    """Efecto de sombra"""
    def __init__(self, parent=None, blur_radius=20, offset=QPoint(0, 8), color=None):
        super().__init__(parent)
        if color is None:
            color = QColor(0, 0, 0, 60)
        self.setBlurRadius(blur_radius)
        self.setXOffset(offset.x())
        self.setYOffset(offset.y())
        self.setColor(color)

class AnimatedButton(QPushButton):
    """Botón con animacion"""
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setGraphicsEffect(ModernShadowEffect(self, blur_radius=15, offset=QPoint(0, 4)))
        
    def enterEvent(self, event):
        self.setGraphicsEffect(ModernShadowEffect(self, blur_radius=25, offset=QPoint(0, 8)))
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setGraphicsEffect(ModernShadowEffect(self, blur_radius=15, offset=QPoint(0, 4)))
        super().leaveEvent(event)

class ModernCard(QFrame):
    """Tarjeta con efectos"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setGraphicsEffect(ModernShadowEffect(self, blur_radius=20, offset=QPoint(0, 6)))
        
    def apply_theme(self, theme):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {theme['card_bg']};
                border-radius: 20px;
                border: 1px solid {theme['border']};
            }}
            QFrame:hover {{
                border: 2px solid {theme['primary']};
            }}
        """)

class StatsCard(ModernCard):
    """Tarjeta de estadísticas"""
    def __init__(self, title, value, icon="📊", color=None, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(8)
        
        # Icono y título
        header_layout = QHBoxLayout()
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)
        header_layout.addStretch()
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px; font-weight: 600; color: #6C757D;")
        
        # Valor
        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        
        layout.addLayout(header_layout)
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        self.title_label = title_label
        self.value_label = value_label
        
    def update_value(self, new_value):
        self.value_label.setText(str(new_value))

class ProductCard(ModernCard):
    """Widget de tarjeta de producto"""
    def __init__(self, product):
        super().__init__()
        self.product_data = product
        name, price, image_path, category, stock = product

        self.setFixedSize(220, 320)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)

        # Imagen del producto con marco redondeado
        image_container = QFrame()
        image_container.setFixedSize(190, 160)
        image_container.setStyleSheet("""
            QFrame {
                border-radius: 15px;
                background-color: #F8F9FA;
            }
        """)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(5, 5, 5, 5)
        
        self.image_label = QLabel()
        pixmap = QPixmap(image_path) if os.path.exists(image_path) else QPixmap(DEFAULT_IMAGE_PATH)
        if pixmap.isNull():
            pixmap = QPixmap(180, 150)
            pixmap.fill(QColor("#FEFAE0"))
        self.image_label.setPixmap(pixmap.scaled(180, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.image_label.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image_label)
        
        layout.addWidget(image_container, alignment=Qt.AlignCenter)

        # Información del producto
        info_container = QFrame()
        info_layout = QVBoxLayout(info_container)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(8)

        # Nombre del producto
        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        info_layout.addWidget(self.name_label)

        # Precio y stock
        details_layout = QHBoxLayout()
        self.price_label = QLabel(f"${price:.2f}")
        self.price_label.setAlignment(Qt.AlignLeft)
        details_layout.addWidget(self.price_label)

        self.stock_label = QLabel(f"Stock: {stock}")
        self.stock_label.setAlignment(Qt.AlignRight)
        details_layout.addWidget(self.stock_label)
        info_layout.addLayout(details_layout)

        layout.addWidget(info_container)

        # Botón de añadir mejorado
        self.add_to_cart_btn = AnimatedButton("Añadir al Carrito")
        self.add_to_cart_btn.setFixedHeight(40)
        layout.addWidget(self.add_to_cart_btn)

        self.apply_theme(current_theme)
        self.mouseDoubleClickEvent = self.show_product_details

    def show_product_details(self, event):
        """Muestra detalles del producto"""
        name, price, image_path, category, stock = self.product_data
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Detalles de {name}")
        dialog.setFixedSize(500, 600)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {current_theme['background']};
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Imagen grande
        img_container = ModernCard()
        img_container.setFixedSize(300, 200)
        img_layout = QVBoxLayout(img_container)
        
        img_lbl = QLabel()
        pixmap = QPixmap(image_path) if os.path.exists(image_path) else QPixmap(DEFAULT_IMAGE_PATH)
        if pixmap.isNull():
            pixmap = QPixmap(280, 180)
            pixmap.fill(QColor("#FEFAE0"))
        img_lbl.setPixmap(pixmap.scaled(280, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        img_lbl.setAlignment(Qt.AlignCenter)
        img_layout.addWidget(img_lbl)
        
        layout.addWidget(img_container, alignment=Qt.AlignCenter)

        # Información detallada
        info_card = ModernCard()
        info_layout = QVBoxLayout(info_card)
        info_layout.setContentsMargins(25, 20, 25, 20)
        
        name_lbl = QLabel(f"<h2 style='color: {current_theme['primary']};'>{name}</h2>")
        name_lbl.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(name_lbl)

        details_lbl = QLabel(f"""
            <div style='font-size: 16px; line-height: 1.6;'>
                <p><b>Categoría:</b> <span style='color: {current_theme['secondary']};'>{category}</span></p>
                <p><b>Precio:</b> <span style='color: {current_theme['accent']}; font-size: 18px;'>${price:.2f}</span></p>
                <p><b>Stock Disponible:</b> <span style='color: {current_theme['success']};'>{stock} unidades</span></p>
                <p><b>Descripción:</b> Delicioso {name.lower()} preparado con ingredientes frescos y de la más alta calidad.</p>
            </div>
        """)
        details_lbl.setWordWrap(True)
        details_lbl.setStyleSheet(f"color: {current_theme['text']};")
        info_layout.addWidget(details_lbl)
        
        layout.addWidget(info_card)

        # Botón cerrar
        close_btn = AnimatedButton("Cerrar")
        close_btn.setFixedHeight(45)
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        img_container.apply_theme(current_theme)
        info_card.apply_theme(current_theme)
        dialog.exec_()

    def apply_theme(self, theme):
        """Aplica el tema a la tarjeta"""
        super().apply_theme(theme)
        
        self.name_label.setStyleSheet(f"""
            font-weight: bold; 
            color: {theme['text']}; 
            font-size: 16px;
            padding: 5px;
        """)
        self.price_label.setStyleSheet(f"""
            color: {theme['accent']}; 
            font-weight: 700; 
            font-size: 18px;
        """)
        self.stock_label.setStyleSheet(f"""
            color: {theme['warning']}; 
            font-style: italic; 
            font-size: 13px;
        """)
        self.add_to_cart_btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['gradient_start']}, stop:1 {theme['gradient_end']});
                color: white;
                font-weight: 700;
                border-radius: 20px;
                padding: 10px 15px;
                font-size: 14px;
                border: none;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['button_hover']}, stop:1 {theme['gradient_end']});
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {theme['button_pressed']}, stop:1 {theme['gradient_end']});
            }}
        """)

class OrdersView(QWidget):
    """Vista de órdenes y productos"""
    def __init__(self):
        super().__init__()
        self.current_theme = current_theme
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header mejorado
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("Menú de Productos")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 10px;")
        header_layout.addWidget(title)
        
        description = QLabel("Explora nuestros deliciosos productos y gestiona tus órdenes con facilidad")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 16px; color: #6C757D; margin-bottom: 15px;")
        header_layout.addWidget(description)
        
        layout.addWidget(header_card)
        
        # Controles de búsqueda 
        controls_card = ModernCard()
        controls_layout = QHBoxLayout(controls_card)
        controls_layout.setContentsMargins(25, 20, 25, 20)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar productos por nombre...")
        self.search_input.setFixedHeight(45)
        self.search_input.textChanged.connect(self.update_product_grid)
        controls_layout.addWidget(self.search_input)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["📋 Todas las Categorías", "🍜 Ramen", "🥤 Bebidas", "🍱 Otros"])
        self.category_filter.setFixedHeight(45)
        self.category_filter.currentTextChanged.connect(self.update_product_grid)
        controls_layout.addWidget(self.category_filter)
        
        layout.addWidget(controls_card)

        # Grid de productos
        self.grid = QGridLayout()
        self.grid.setSpacing(25)
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #F0F0F0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #C0C0C0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #A0A0A0;
            }
        """)
        
        content = QWidget()
        content.setLayout(self.grid)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.update_product_grid()
        self.apply_theme(current_theme)
        controls_card.apply_theme(current_theme)
        header_card.apply_theme(current_theme)

    def update_product_grid(self):
        """Actualiza la cuadrícula de productos"""
        # Limpiar grid
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.setParent(None)

        search = self.search_input.text().lower()
        cat = self.category_filter.currentText()
        
        # Categorías con emojis
        category_map = {
            "📋 Todas las Categorías": "Todas las Categorías",
            "🍜 Ramen": "Ramen",
            "🥤 Bebidas": "Drink",
            "🍱 Otros": "Other"
        }
        
        cat = category_map.get(cat, cat)

        row = col = 0
        for product in products:
            name, price, img, category, stock = product
            
            category_match = (cat == "Todas las Categorías" or category == cat)
            search_match = (not search or search in name.lower())

            if category_match and search_match:
                card = ProductCard(product)
                self.grid.addWidget(card, row, col)
                col += 1
                if col >= 4:
                    col = 0
                    row += 1

    def apply_theme(self, theme):
        """Aplica el tema a la vista"""
        self.current_theme = theme
        self.setStyleSheet(f"background-color: {theme['background']};")
        
        # Estilos de controles
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {theme['border']};
                border-radius: 22px;
                padding: 12px 20px;
                font-size: 16px;
                color: {theme['text']};
                background-color: {theme['card_bg']};
            }}
            QLineEdit:focus {{
                border: 2px solid {theme['primary']};
                background-color: {theme['card_bg']};
            }}
        """)
        
        self.category_filter.setStyleSheet(f"""
            QComboBox {{
                border: 2px solid {theme['border']};
                border-radius: 22px;
                padding: 12px 20px;
                font-size: 16px;
                color: {theme['text']};
                background-color: {theme['card_bg']};
                min-width: 200px;
            }}
            QComboBox:hover {{
                border: 2px solid {theme['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 30px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid {theme['text']};
                margin-right: 10px;
            }}
        """)
        
        # Actualizar tarjetas existentes
        for i in range(self.grid.count()):
            widget = self.grid.itemAt(i).widget()
            if isinstance(widget, ProductCard):
                widget.apply_theme(theme)

class InventoryView(QWidget):
    """Vista de inventario"""
    def __init__(self):
        super().__init__()
        self.current_theme = current_theme
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header 
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("📦 Gestión de Inventario")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 10px;")
        header_layout.addWidget(title)
        
        description = QLabel("Administra tu inventario de productos de manera eficiente")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 16px; color: #6C757D;")
        header_layout.addWidget(description)
        
        layout.addWidget(header_card)

        # Búsqueda 
        search_card = ModernCard()
        search_layout = QHBoxLayout(search_card)
        search_layout.setContentsMargins(25, 20, 25, 20)
        
        self.inventory_search = QLineEdit()
        self.inventory_search.setPlaceholderText("🔍 Buscar producto por nombre o categoría...")
        self.inventory_search.setFixedHeight(45)
        self.inventory_search.textChanged.connect(self.update_inventory_table)
        search_layout.addWidget(self.inventory_search)
        
        layout.addWidget(search_card)
        
        # Tabla 
        table_card = ModernCard()
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(25, 25, 25, 25)
        
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(["Imagen", "Producto", "Categoría", "Precio", "Stock"])
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.setColumnWidth(0, 100)
        self.inventory_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setMinimumHeight(400)
        table_layout.addWidget(self.inventory_table)
        
        layout.addWidget(table_card)

        # Botones 
        buttons_card = ModernCard()
        btn_layout = QHBoxLayout(buttons_card)
        btn_layout.setContentsMargins(25, 20, 25, 20)
        
        btn_add = AnimatedButton("➕ Añadir Producto")
        btn_add.clicked.connect(self.add_product)
        btn_edit = AnimatedButton("✏️ Editar Producto")
        btn_edit.clicked.connect(self.edit_product)
        btn_del = AnimatedButton("🗑️ Eliminar Producto")
        btn_del.clicked.connect(self.remove_product)
        
        for btn in [btn_add, btn_edit, btn_del]:
            btn.setFixedHeight(50)
            btn_layout.addWidget(btn)
        
        layout.addWidget(buttons_card)

        self.update_inventory_table()
        self.apply_theme(current_theme)
        header_card.apply_theme(current_theme)
        search_card.apply_theme(current_theme)
        table_card.apply_theme(current_theme)
        buttons_card.apply_theme(current_theme)

    def update_inventory_table(self):
        """Actualiza la tabla de inventario"""
        search_text = self.inventory_search.text().lower()
        filtered_products = [p for p in products if search_text in p[0].lower() or search_text in p[3].lower()]

        self.inventory_table.setRowCount(len(filtered_products))
        for r, (name, price, img_path, category, stock) in enumerate(filtered_products):
            # Imagen
            lbl = QLabel()
            pm = QPixmap(img_path) if os.path.exists(img_path) else QPixmap(DEFAULT_IMAGE_PATH)
            if pm.isNull():
                pm = QPixmap(80, 80)
                pm.fill(QColor("#FEFAE0"))
            lbl.setPixmap(pm.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("padding: 5px;")
            self.inventory_table.setCellWidget(r, 0, lbl)
            
            # Datos
            self.inventory_table.setItem(r, 1, QTableWidgetItem(name))
            self.inventory_table.setItem(r, 2, QTableWidgetItem(category))
            self.inventory_table.setItem(r, 3, QTableWidgetItem(f"${price:.2f}"))
            self.inventory_table.setItem(r, 4, QTableWidgetItem(str(stock)))
        
        self.inventory_table.resizeRowsToContents()

    def add_product(self):
        """Añadir nuevo producto"""
        self._show_product_dialog("Añadir Nuevo Producto")

    def edit_product(self):
        """Editar producto seleccionado"""
        selected_rows = self.inventory_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Editar Producto", "Por favor, selecciona un producto para editar.")
            return

        row = selected_rows[0].row()
        product_name_in_table = self.inventory_table.item(row, 1).text()
        
        original_product = next((p for p in products if p[0] == product_name_in_table), None)
        
        if original_product:
            self._show_product_dialog("Editar Producto", original_product)
        else:
            QMessageBox.critical(self, "Error", "No se pudo encontrar el producto original.")

    def _show_product_dialog(self, title, product_data=None):
        """Muestra diálogo para añadir/editar producto con diseño mejorado"""
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.setFixedSize(600, 500)
        dialog.setStyleSheet(f"""
            QDialog {{
                background-color: {current_theme['background']};
                border-radius: 20px;
            }}
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        # Título del diálogo
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 24px; 
            font-weight: bold; 
            color: {current_theme['primary']};
            margin-bottom: 20px;
        """)
        layout.addWidget(title_label)

        # Formulario en tarjeta
        form_card = ModernCard()
        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(15)

        fields = {}
        input_data = [
            ("Nombre del Producto", "name", "text"),
            ("Categoría", "category", "combo"),
            ("Precio", "price", "text"),
            ("Stock", "stock", "text")
        ]
        
        categories = ["Ramen", "Drink", "Other", "Postres", "Snacks"]

        for label_text, key, input_type in input_data:
            if input_type == "combo":
                combo = QComboBox()
                combo.addItems(categories)
                combo.setFixedHeight(45)
                combo.setStyleSheet(f"""
                    QComboBox {{
                        border: 2px solid {current_theme['border']};
                        border-radius: 10px;
                        padding: 10px 15px;
                        font-size: 14px;
                        color: {current_theme['text']};
                        background-color: {current_theme['card_bg']};
                    }}
                """)
                form_layout.addRow(f"{label_text}:", combo)
                fields[key] = combo
            else:
                le = QLineEdit()
                le.setPlaceholderText(f"Ingrese {label_text.lower()}")
                le.setFixedHeight(45)
                le.setStyleSheet(f"""
                    QLineEdit {{
                        border: 2px solid {current_theme['border']};
                        border-radius: 10px;
                        padding: 10px 15px;
                        font-size: 14px;
                        color: {current_theme['text']};
                        background-color: {current_theme['card_bg']};
                    }}
                    QLineEdit:focus {{
                        border: 2px solid {current_theme['primary']};
                    }}
                """)
                form_layout.addRow(f"{label_text}:", le)
                fields[key] = le

        layout.addWidget(form_card)

        # Rellenar datos si es edición
        if product_data:
            name, price, img_path, category, stock = product_data
            fields["name"].setText(name)
            fields["category"].setCurrentText(category)
            fields["price"].setText(str(price))
            fields["stock"].setText(str(stock))

        # Botones mejorados
        button_card = ModernCard()
        button_layout = QHBoxLayout(button_card)
        button_layout.setContentsMargins(20, 15, 20, 15)
        
        btn_cancel = AnimatedButton("Cancelar")
        btn_cancel.setFixedHeight(50)
        btn_cancel.clicked.connect(dialog.reject)
        
        btn_save = AnimatedButton("Guardar Producto")
        btn_save.setFixedHeight(50)
        btn_save.clicked.connect(lambda: self._save_product_dialog(dialog, fields, product_data))

        button_layout.addWidget(btn_cancel)
        button_layout.addWidget(btn_save)
        layout.addWidget(button_card)

        # Aplicar temas
        form_card.apply_theme(current_theme)
        button_card.apply_theme(current_theme)
        
        # Estilos de botones
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {current_theme['border']};
                color: {current_theme['text']};
                font-weight: 600;
                border-radius: 25px;
                padding: 15px 30px;
                font-size: 16px;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {current_theme['grey_text']};
                color: white;
            }}
        """)
        
        btn_save.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {current_theme['gradient_start']}, stop:1 {current_theme['gradient_end']});
                color: white;
                font-weight: 600;
                border-radius: 25px;
                padding: 15px 30px;
                font-size: 16px;
                border: none;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {current_theme['button_hover']}, stop:1 {current_theme['gradient_end']});
            }}
        """)

        dialog.exec_()

    def _save_product_dialog(self, dialog, fields, original_product_data):
        """Guarda el producto del diálogo"""
        name = fields["name"].text().strip()
        category = fields["category"].currentText().strip()
        price_str = fields["price"].text().strip()
        stock_str = fields["stock"].text().strip()

        # Validación
        if not name or not category or not price_str or not stock_str:
            QMessageBox.warning(dialog, "Datos Incompletos", "Por favor, completa todos los campos.")
            return
        
        try:
            price = float(price_str)
            if price <= 0:
                raise ValueError("El precio debe ser positivo.")
        except ValueError:
            QMessageBox.warning(dialog, "Error de Formato", "El precio debe ser un número válido.")
            return
        
        try:
            stock = int(stock_str)
            if stock < 0:
                raise ValueError("El stock no puede ser negativo.")
        except ValueError:
            QMessageBox.warning(dialog, "Error de Formato", "El stock debe ser un número entero válido.")
            return

        new_product = (name, price, DEFAULT_IMAGE_PATH, category, stock)

        global products
        if original_product_data:
            # Edición
            try:
                original_name = original_product_data[0]
                idx = next(i for i, p in enumerate(products) if p[0] == original_name)
                products[idx] = new_product
                QMessageBox.information(dialog, "Éxito", f"Producto '{name}' actualizado correctamente.")
            except StopIteration:
                QMessageBox.critical(dialog, "Error", "No se pudo encontrar el producto original.")
                return
        else:
            # Nuevo producto
            if any(p[0].lower() == name.lower() for p in products):
                QMessageBox.warning(dialog, "Producto Existente", "Ya existe un producto con este nombre.")
                return
            products.append(new_product)
            QMessageBox.information(dialog, "Éxito", f"Producto '{name}' añadido correctamente.")
        
        save_products(products)
        self.update_inventory_table()
        dialog.accept()

    def remove_product(self):
        """Eliminar producto seleccionado"""
        selected_rows = self.inventory_table.selectedIndexes()
        if not selected_rows:
            QMessageBox.warning(self, "Eliminar Producto", "Por favor, selecciona un producto para eliminar.")
            return

        row = selected_rows[0].row()
        product_name_to_delete = self.inventory_table.item(row, 1).text()

        reply = QMessageBox.question(self, "Confirmar Eliminación",
                                     f"¿Estás seguro de que deseas eliminar '{product_name_to_delete}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            global products
            products = [p for p in products if p[0] != product_name_to_delete]
            save_products(products)
            self.update_inventory_table()
            QMessageBox.information(self, "Eliminación Exitosa", f"Producto '{product_name_to_delete}' eliminado.")

    def apply_theme(self, theme):
        """Aplica el tema a la vista"""
        self.current_theme = theme
        self.setStyleSheet(f"background-color: {theme['background']};")
        
        self.inventory_search.setStyleSheet(f"""
            QLineEdit {{
                border: 2px solid {theme['border']};
                border-radius: 22px;
                padding: 12px 20px;
                font-size: 16px;
                color: {theme['text']};
                background-color: {theme['card_bg']};
            }}
            QLineEdit:focus {{
                border: 2px solid {theme['primary']};
            }}
        """)
        
        self.inventory_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {theme['card_bg']};
                border: none;
                border-radius: 15px;
                gridline-color: {theme['border']};
                color: {theme['text']};
                font-size: 14px;
                selection-background-color: {theme['selection_bg']};
            }}
            QHeaderView::section {{
                background-color: {theme['header_bg']};
                color: {theme['text']};
                padding: 15px;
                border: none;
                border-bottom: 2px solid {theme['border']};
                font-weight: bold;
                font-size: 14px;
            }}
            QTableWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {theme['border']};
            }}
            QTableWidget::item:selected {{
                background-color: {theme['selection_bg']};
                color: {theme['text']};
            }}
        """)

class ReportsView(QWidget):
    """Vista de reportes con gráficos"""
    def __init__(self):
        super().__init__()
        self.current_theme = current_theme
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header mejorado
        header_card = ModernCard()
        header_layout = QVBoxLayout(header_card)
        header_layout.setContentsMargins(30, 25, 30, 25)
        
        title = QLabel("📊 Informes y Análisis")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; margin-bottom: 10px;")
        header_layout.addWidget(title)
        
        description = QLabel("Visualiza el rendimiento de tu negocio con gráficos detallados")
        description.setAlignment(Qt.AlignCenter)
        description.setStyleSheet("font-size: 16px; color: #6C757D;")
        header_layout.addWidget(description)
        
        layout.addWidget(header_card)

        # Tarjetas de estadísticas
        stats_container = QWidget()
        stats_layout = QHBoxLayout(stats_container)
        stats_layout.setSpacing(20)
        
        # Calcular estadísticas
        total_products = len(products)
        total_value = sum(p[1] * p[4] for p in products)  # precio * stock
        low_stock = len([p for p in products if p[4] < 10])
        avg_price = sum(p[1] for p in products) / len(products) if products else 0
        
        stats_cards = [
            StatsCard("Total Productos", total_products, "📦", current_theme['primary']),
            StatsCard("Valor Inventario", f"${total_value:,.0f}", "💰", current_theme['success']),
            StatsCard("Stock Bajo", low_stock, "⚠️", current_theme['warning']),
            StatsCard("Precio Promedio", f"${avg_price:.2f}", "📈", current_theme['secondary'])
        ]
        
        for card in stats_cards:
            card.apply_theme(current_theme)
            stats_layout.addWidget(card)
        
        layout.addWidget(stats_container)

        # Contenedor para gráficos
        charts_card = ModernCard()
        self.charts_layout = QGridLayout(charts_card)
        self.charts_layout.setContentsMargins(30, 30, 30, 30)
        self.charts_layout.setSpacing(30)
        
        layout.addWidget(charts_card)

        # Datos simulados
        self.months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago"]
        self.ganancias = [12000, 18000, 15000, 21000, 19000, 23000, 26000, 28000]
        self.categorias = ['Ramen', 'Bebidas', 'Postres', 'Otros']
        self.ventas_categoria = [55000, 32000, 18000, 15000]
        
        # Crear gráficos
        self.canvas_monthly = self._create_chart_canvas()
        self.canvas_category = self._create_chart_canvas()

        self.charts_layout.addWidget(self.canvas_monthly, 0, 0)
        self.charts_layout.addWidget(self.canvas_category, 0, 1)

        self.draw_plots()
        self.apply_theme(current_theme)
        header_card.apply_theme(current_theme)
        charts_card.apply_theme(current_theme)

    def _create_chart_canvas(self):
        """Crea un canvas para gráficos"""
        fig = Figure(figsize=(6, 5), dpi=100)
        fig.patch.set_facecolor('none')
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(350)
        canvas.setStyleSheet("background-color: transparent;")
        return canvas

    def draw_plots(self):
        """Dibuja los gráficos con estilo"""
        # Configurar colores según el tema
        bg_color = self.current_theme['card_bg']
        text_color = self.current_theme['text']
        primary_color = self.current_theme['primary']
        secondary_color = self.current_theme['secondary']
        
        # Gráfico de barras - Ganancias mensuales
        self.canvas_monthly.figure.clear()
        ax1 = self.canvas_monthly.figure.add_subplot(111)
        ax1.set_facecolor('none')
        
        bars = ax1.bar(self.months, self.ganancias, 
                      color=primary_color, alpha=0.8, 
                      edgecolor=secondary_color, linewidth=1.5)
        
        # Añadir valores en las barras
        for bar, value in zip(bars, self.ganancias):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 500,
                    f'${value/1000:.0f}K', ha='center', va='bottom',
                    color=text_color, fontweight='bold', fontsize=9)
        
        ax1.set_title('📈 Ganancias Mensuales', fontsize=16, fontweight='bold', 
                     color=text_color, pad=20)
        ax1.set_ylabel('Ganancias ($)', color=text_color, fontweight='600')
        ax1.tick_params(axis='x', rotation=45, colors=text_color)
        ax1.tick_params(axis='y', colors=text_color)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['left'].set_color(text_color)
        ax1.spines['bottom'].set_color(text_color)
        ax1.grid(True, alpha=0.3, color=text_color)
        
        self.canvas_monthly.figure.tight_layout()
        self.canvas_monthly.draw()

        # Gráfico de pastel - Ventas por categoría
        self.canvas_category.figure.clear()
        ax2 = self.canvas_category.figure.add_subplot(111)
        ax2.set_facecolor('none')
        
        colors = [primary_color, secondary_color, self.current_theme['accent'], self.current_theme['success']]
        wedges, texts, autotexts = ax2.pie(self.ventas_categoria, labels=self.categorias, 
                                          autopct='%1.1f%%', colors=colors, startangle=140,
                                          textprops={'color': text_color, 'fontweight': 'bold'})
        
        # El texto del porcentaje
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        ax2.set_title('🥧 Ventas por Categoría', fontsize=16, fontweight='bold', 
                     color=text_color, pad=20)
        
        self.canvas_category.figure.tight_layout()
        self.canvas_category.draw()

    def apply_theme(self, theme):
        """Aplica el tema a la vista"""
        self.current_theme = theme
        self.setStyleSheet(f"background-color: {theme['background']};")
        self.draw_plots()

class AccountView(QWidget):
    """Vista de cuenta completamente rediseñada y expandida"""
    def __init__(self, theme_callback):
        super().__init__()
        self.theme_callback = theme_callback
        self.user_data = user_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(25)

        # Header de perfil
        profile_card = ModernCard()
        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(40, 30, 40, 30)
        profile_layout.setSpacing(20)
        
        # Avatar y nombre
        avatar_layout = QHBoxLayout()
        
        # Avatar (círculo con iniciales)
        avatar_container = QFrame()
        avatar_container.setFixedSize(100, 100)
        avatar_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {current_theme['gradient_start']}, stop:1 {current_theme['gradient_end']});
                border-radius: 50px;
                border: 3px solid {current_theme['border']};
            }}
        """)
        
        avatar_label = QLabel(self.user_data['name'][:2].upper())
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet("""
            color: white; 
            font-size: 32px; 
            font-weight: bold;
            background: transparent;
            border: none;
        """)
        
        avatar_layout_inner = QVBoxLayout(avatar_container)
        avatar_layout_inner.addWidget(avatar_label)
        avatar_layout_inner.setContentsMargins(0, 0, 0, 0)
        
        avatar_layout.addWidget(avatar_container)
        
        # Información del usuario
        user_info_layout = QVBoxLayout()
        
        name_label = QLabel(f"👋 Hola, {self.user_data['name']}")
        name_label.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 5px;")
        
        business_label = QLabel(f"🏪 {self.user_data['business_name']}")
        business_label.setStyleSheet("font-size: 18px; color: #6C757D; margin-bottom: 10px;")
        
        join_date = QLabel(f"📅 Miembro desde {self.user_data['join_date']}")
        join_date.setStyleSheet("font-size: 14px; color: #6C757D;")
        
        user_info_layout.addWidget(name_label)
        user_info_layout.addWidget(business_label)
        user_info_layout.addWidget(join_date)
        user_info_layout.addStretch()
        
        avatar_layout.addLayout(user_info_layout)
        avatar_layout.addStretch()
        
        profile_layout.addLayout(avatar_layout)
        layout.addWidget(profile_card)

        # Estadísticas del usuario
        user_stats_container = QWidget()
        user_stats_layout = QHBoxLayout(user_stats_container)
        user_stats_layout.setSpacing(20)
        
        user_stats_cards = [
            StatsCard("Ventas Totales", f"${self.user_data['total_sales']:,}", "💰", current_theme['success']),
            StatsCard("Órdenes", self.user_data['total_orders'], "📋", current_theme['primary']),
            StatsCard("Categoría Favorita", self.user_data['favorite_category'], "❤️", current_theme['accent']),
        ]
        
        for card in user_stats_cards:
            card.apply_theme(current_theme)
            user_stats_layout.addWidget(card)
        
        layout.addWidget(user_stats_container)

        # Scroll area para configuraciones
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(20)

        # Configuraciones organizadas en secciones
        sections = [
            ("🎨 Apariencia", self._create_appearance_section()),
            ("👤 Información Personal", self._create_personal_info_section()),
            ("🏢 Información del Negocio", self._create_business_info_section()),
            ("⚙️ Configuraciones", self._create_settings_section()),
            ("📊 Preferencias", self._create_preferences_section())
        ]
        
        for section_title, section_widget in sections:
            # Título de sección
            section_header = QLabel(section_title)
            section_header.setStyleSheet("""
                font-size: 20px; 
                font-weight: bold; 
                margin-top: 10px; 
                margin-bottom: 10px;
                padding: 10px 0px;
            """)
            scroll_layout.addWidget(section_header)
            scroll_layout.addWidget(section_widget)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        self.apply_theme(current_theme)
        profile_card.apply_theme(current_theme)

    def _create_appearance_section(self):
        """Crea la sección de apariencia"""
        card = ModernCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Selector de tema
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Tema de la aplicación:")
        theme_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["🌞 Claro", "🌙 Oscuro"])
        self.theme_combo.setCurrentText("🌞 Claro" if self.user_data['theme'] == "Claro" else "🌙 Oscuro")
        self.theme_combo.currentIndexChanged.connect(self.apply_theme_change)
        self.theme_combo.setFixedHeight(40)
        
        theme_layout.addWidget(theme_label)
        theme_layout.addStretch()
        theme_layout.addWidget(self.theme_combo)
        
        layout.addLayout(theme_layout)
        return card

    def _create_personal_info_section(self):
        """Crea la sección de información personal"""
        card = ModernCard()
        layout = QFormLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Campos editables
        self.name_edit = QLineEdit(self.user_data['name'])
        self.email_edit = QLineEdit(self.user_data['email'])
        self.phone_edit = QLineEdit(self.user_data['phone'])
        
        fields = [
            ("👤 Nombre completo:", self.name_edit),
            ("📧 Correo electrónico:", self.email_edit),
            ("📱 Teléfono:", self.phone_edit),
        ]
        
        for label_text, field in fields:
            field.setFixedHeight(40)
            field.setStyleSheet(f"""
                QLineEdit {{
                    border: 2px solid {current_theme['border']};
                    border-radius: 10px;
                    padding: 10px 15px;
                    font-size: 14px;
                    color: {current_theme['text']};
                    background-color: {current_theme['card_bg']};
                }}
                QLineEdit:focus {{
                    border: 2px solid {current_theme['primary']};
                }}
            """)
            layout.addRow(label_text, field)
        
        # Botón para guardar cambios
        save_personal_btn = AnimatedButton("💾 Guardar Cambios Personales")
        save_personal_btn.setFixedHeight(45)
        save_personal_btn.clicked.connect(self.save_personal_info)
        layout.addRow("", save_personal_btn)
        
        return card

    def _create_business_info_section(self):
        """Crea la sección de información del negocio"""
        card = ModernCard()
        layout = QFormLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Campos del negocio
        self.business_name_edit = QLineEdit(self.user_data['business_name'])
        self.address_edit = QLineEdit(self.user_data['address'])
        
        fields = [
            ("🏪 Nombre del negocio:", self.business_name_edit),
            ("📍 Dirección:", self.address_edit),
        ]
        
        for label_text, field in fields:
            field.setFixedHeight(40)
            field.setStyleSheet(f"""
                QLineEdit {{
                    border: 2px solid {current_theme['border']};
                    border-radius: 10px;
                    padding: 10px 15px;
                    font-size: 14px;
                    color: {current_theme['text']};
                    background-color: {current_theme['card_bg']};
                }}
                QLineEdit:focus {{
                    border: 2px solid {current_theme['primary']};
                }}
            """)
            layout.addRow(label_text, field)
        
        # Botón para guardar
        save_business_btn = AnimatedButton("🏢 Guardar Info. del Negocio")
        save_business_btn.setFixedHeight(45)
        save_business_btn.clicked.connect(self.save_business_info)
        layout.addRow("", save_business_btn)
        
        return card

    def _create_settings_section(self):
        """Crea la sección de configuraciones"""
        card = ModernCard()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(20)
        
        # Configuraciones con switches
        settings_data = [
            ("🔔 Notificaciones", "notifications", "Recibir notificaciones del sistema"),
            ("💾 Respaldo automático", "auto_backup", "Crear respaldos automáticos de datos"),
        ]
        
        self.settings_checkboxes = {}
        
        for title, key, description in settings_data:
            setting_container = QFrame()
            setting_layout = QVBoxLayout(setting_container)
            setting_layout.setContentsMargins(15, 10, 15, 10)
            setting_layout.setSpacing(5)
            
            # Título y checkbox
            title_layout = QHBoxLayout()
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: 600; font-size: 16px;")
            
            checkbox = QCheckBox()
            checkbox.setChecked(self.user_data.get(key, True))
            checkbox.setStyleSheet(f"""
                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 10px;
                    border: 2px solid {current_theme['border']};
                    background-color: {current_theme['card_bg']};
                }}
                QCheckBox::indicator:checked {{
                    background-color: {current_theme['primary']};
                    border: 2px solid {current_theme['primary']};
                }}
                QCheckBox::indicator:checked::after {{
                    content: "✓";
                    color: white;
                    font-weight: bold;
                }}
            """)
            
            self.settings_checkboxes[key] = checkbox
            
            title_layout.addWidget(title_label)
            title_layout.addStretch()
            title_layout.addWidget(checkbox)
            
            # Descripción
            desc_label = QLabel(description)
            desc_label.setStyleSheet("color: #6C757D; font-size: 13px;")
            desc_label.setWordWrap(True)
            
            setting_layout.addLayout(title_layout)
            setting_layout.addWidget(desc_label)
            
            setting_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {current_theme['header_bg']};
                    border-radius: 10px;
                    border: 1px solid {current_theme['border']};
                }}
            """)
            
            layout.addWidget(setting_container)
        
        # Botón para guardar configuraciones
        save_settings_btn = AnimatedButton("⚙️ Guardar Configuraciones")
        save_settings_btn.setFixedHeight(45)
        save_settings_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_settings_btn)
        
        return card

    def _create_preferences_section(self):
        """Crea la sección de preferencias"""
        card = ModernCard()
        layout = QFormLayout(card)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Idioma
        self.language_combo = QComboBox()
        self.language_combo.addItems(["🇪🇸 Español", "🇺🇸 English", "🇫🇷 Français"])
        self.language_combo.setCurrentText("🇪🇸 Español")
        self.language_combo.setFixedHeight(40)
        
        # Moneda
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["💵 USD", "💶 EUR", "💷 GBP", "🪙 MXN"])
        self.currency_combo.setCurrentText("💵 USD")
        self.currency_combo.setFixedHeight(40)
        
        # Tasa de impuestos
        self.tax_rate_edit = QLineEdit(str(self.user_data.get('tax_rate', 8.5)))
        self.tax_rate_edit.setFixedHeight(40)
        self.tax_rate_edit.setPlaceholderText("Ej: 8.5")
        
        fields = [
            ("🌐 Idioma:", self.language_combo),
            ("💰 Moneda:", self.currency_combo),
            ("📊 Tasa de impuestos (%):", self.tax_rate_edit),
        ]
        
        for label_text, field in fields:
            if isinstance(field, QComboBox):
                field.setStyleSheet(f"""
                    QComboBox {{
                        border: 2px solid {current_theme['border']};
                        border-radius: 10px;
                        padding: 10px 15px;
                        font-size: 14px;
                        color: {current_theme['text']};
                        background-color: {current_theme['card_bg']};
                    }}
                    QComboBox:hover {{
                        border: 2px solid {current_theme['primary']};
                    }}
                """)
            else:
                field.setStyleSheet(f"""
                    QLineEdit {{
                        border: 2px solid {current_theme['border']};
                        border-radius: 10px;
                        padding: 10px 15px;
                        font-size: 14px;
                        color: {current_theme['text']};
                        background-color: {current_theme['card_bg']};
                    }}
                    QLineEdit:focus {{
                        border: 2px solid {current_theme['primary']};
                    }}
                """)
            layout.addRow(label_text, field)
        
        # Botón para guardar preferencias
        save_prefs_btn = AnimatedButton("📋 Guardar Preferencias")
        save_prefs_btn.setFixedHeight(45)
        save_prefs_btn.clicked.connect(self.save_preferences)
        layout.addRow("", save_prefs_btn)
        
        return card

    def save_personal_info(self):
        """Guarda la información personal"""
        self.user_data['name'] = self.name_edit.text()
        self.user_data['email'] = self.email_edit.text()
        self.user_data['phone'] = self.phone_edit.text()
        save_user_data(self.user_data)
        QMessageBox.information(self, "Éxito", "Información personal guardada correctamente.")

    def save_business_info(self):
        """Guarda la información del negocio"""
        self.user_data['business_name'] = self.business_name_edit.text()
        self.user_data['address'] = self.address_edit.text()
        save_user_data(self.user_data)
        QMessageBox.information(self, "Éxito", "Información del negocio guardada correctamente.")

    def save_settings(self):
        """Guarda las configuraciones"""
        for key, checkbox in self.settings_checkboxes.items():
            self.user_data[key] = checkbox.isChecked()
        save_user_data(self.user_data)
        QMessageBox.information(self, "Éxito", "Configuraciones guardadas correctamente.")

    def save_preferences(self):
        """Guarda las preferencias"""
        self.user_data['language'] = self.language_combo.currentText()
        self.user_data['currency'] = self.currency_combo.currentText()
        try:
            self.user_data['tax_rate'] = float(self.tax_rate_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Error", "La tasa de impuestos debe ser un número válido.")
            return
        save_user_data(self.user_data)
        QMessageBox.information(self, "Éxito", "Preferencias guardadas correctamente.")

    def apply_theme_change(self):
        """Aplica el cambio de tema"""
        selected_theme = self.theme_combo.currentText()
        theme_name = "Claro" if "Claro" in selected_theme else "Oscuro"
        self.user_data['theme'] = theme_name
        save_user_data(self.user_data)
        if self.theme_callback:
            self.theme_callback(theme_name)

    def apply_theme(self, theme):
        """Aplica el tema a la vista"""
        self.setStyleSheet(f"background-color: {theme['background']};")

class LoadingThread(QThread):
    """Hilo para simular carga"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal()

    def run(self):
        steps = [
            "Inicializando FoodWizz...",
            "Cargando productos...",
            "Configurando interfaz...",
            "Aplicando temas...",
            "Preparando gráficos...",
            "Finalizando carga..."
        ]
        
        for i, step in enumerate(steps):
            self.status_updated.emit(step)
            for j in range(17):  # 17 * 6 = 102, aproximadamente 100
                progress = min(100, (i * 17) + j)
                self.progress_updated.emit(progress)
                self.msleep(50)
        
        self.progress_updated.emit(100)
        self.finished.emit()

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación mejorada"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FoodWizz - Sistema de Gestión Avanzado")
        self.setWindowIcon(QIcon("app_icon.png"))
        self.setMinimumSize(1400, 800)
        
        # Centrar ventana
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move(int((screen.width() - size.width()) / 2), 
                 int((screen.height() - size.height()) / 2))
        
        self.current_theme_name = user_data.get('theme', 'Claro')
        self.current_theme = THEME_LIGHT if self.current_theme_name == 'Claro' else THEME_DARK

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Menú lateral mejorado
        self.menu_container = QFrame()
        self.menu_container.setFixedWidth(280)
        self.menu_container.setGraphicsEffect(ModernShadowEffect(self.menu_container, blur_radius=30, offset=QPoint(5, 0)))
        
        menu_layout = QVBoxLayout(self.menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(0)
        
        # Logo/Header del menú
        menu_header = QFrame()
        menu_header.setFixedHeight(100)
        header_layout = QVBoxLayout(menu_header)
        header_layout.setContentsMargins(20, 20, 20, 10)
        
        logo_label = QLabel("FoodWizz")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: white;
            margin-bottom: 5px;
        """)
        
        version_label = QLabel("v6.0")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("""
            font-size: 12px; 
            color: rgba(255, 255, 255, 0.7);
        """)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(version_label)
        menu_layout.addWidget(menu_header)
        
        # Lista del menú
        self.menu = QListWidget()
        self.menu.setCursor(QCursor(Qt.PointingHandCursor))

        # Items del menú con iconos
        self.menu_items = [
            ("🛒 Órdenes", "Gestiona productos y órdenes"),
            ("📦 Inventario", "Control de stock y productos"),
            ("📊 Reportes", "Análisis y estadísticas"),
            ("👤 Mi Cuenta", "Perfil y configuraciones")
        ]
        
        for text, description in self.menu_items:
            item = QListWidgetItem()
            item.setSizeHint(QSize(self.menu.width(), 70))
            
            # Widget personalizado para el item
            item_widget = QFrame()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(20, 10, 20, 10)
            item_layout.setSpacing(2)
            
            title_label = QLabel(text)
            title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: white;")
            
            desc_label = QLabel(description)
            desc_label.setStyleSheet("font-size: 11px; color: rgba(255, 255, 255, 0.7);")
            
            item_layout.addWidget(title_label)
            item_layout.addWidget(desc_label)
            
            self.menu.addItem(item)
            self.menu.setItemWidget(item, item_widget)
        
        menu_layout.addWidget(self.menu)
        
        # Información del usuario en el menú
        user_info_frame = QFrame()
        user_info_frame.setFixedHeight(80)
        user_info_layout = QHBoxLayout(user_info_frame)
        user_info_layout.setContentsMargins(20, 15, 20, 15)
        
        # Mini avatar
        mini_avatar = QLabel(user_data['name'][:2].upper())
        mini_avatar.setFixedSize(40, 40)
        mini_avatar.setAlignment(Qt.AlignCenter)
        mini_avatar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {self.current_theme['gradient_start']}, stop:1 {self.current_theme['gradient_end']});
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 14px;
        """)
        
        user_info_text = QVBoxLayout()
        user_name = QLabel(user_data['name'])
        user_name.setStyleSheet("color: white; font-weight: 600; font-size: 13px;")
        user_role = QLabel("Administrador")
        user_role.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 11px;")
        
        user_info_text.addWidget(user_name)
        user_info_text.addWidget(user_role)
        user_info_text.setSpacing(2)
        
        user_info_layout.addWidget(mini_avatar)
        user_info_layout.addLayout(user_info_text)
        user_info_layout.addStretch()
        
        menu_layout.addWidget(user_info_frame)
        
        main_layout.addWidget(self.menu_container)

        # Contenedor de vistas
        self.stacked_layout = QStackedLayout()
        
        # Crear vistas
        self.orders_view = OrdersView()
        self.inventory_view = InventoryView()
        self.reports_view = ReportsView()
        self.account_view = AccountView(self.apply_theme)

        self.stacked_layout.addWidget(self.orders_view)
        self.stacked_layout.addWidget(self.inventory_view)
        self.stacked_layout.addWidget(self.reports_view)
        self.stacked_layout.addWidget(self.account_view)

        main_layout.addLayout(self.stacked_layout)

        # Conectar eventos
        self.menu.currentRowChanged.connect(self.display_view)
        self.menu.setCurrentRow(0)

        self.apply_theme(self.current_theme_name)

    def display_view(self, index):
        """Cambia la vista actual con animación"""
        self.stacked_layout.setCurrentIndex(index)
        
        # Actualizar vistas según sea necesario
        if index == 0:  # Órdenes
            self.orders_view.update_product_grid()
        elif index == 1:  # Inventario
            self.inventory_view.update_inventory_table()
        elif index == 2:  # Reportes
            self.reports_view.draw_plots()

    def apply_theme(self, theme_name):
        """Aplica el tema a toda la aplicación"""
        global current_theme
        if theme_name == "Oscuro":
            self.current_theme = THEME_DARK
            current_theme = THEME_DARK
        else:
            self.current_theme = THEME_LIGHT
            current_theme = THEME_LIGHT
        
        # Aplicar estilo a la ventana principal
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {self.current_theme['background']};
            }}
        """)

        # Estilo del contenedor del menú
        self.menu_container.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.current_theme['gradient_start']}, stop:1 {self.current_theme['gradient_end']});
                border: none;
            }}
        """)

        # Estilo del menú
        self.menu.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
                padding: 10px 0px;
                outline: 0;
            }}
            QListWidget::item {{
                border-radius: 15px;
                margin: 5px 15px;
                padding: 0px;
            }}
            QListWidget::item:hover {{
                background-color: rgba(255, 255, 255, 0.1);
            }}
            QListWidget::item:selected {{
                background-color: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
            }}
        """)
        
        # Aplicar tema a las vistas
        self.orders_view.apply_theme(self.current_theme)
        self.inventory_view.apply_theme(self.current_theme)
        self.reports_view.apply_theme(self.current_theme)
        self.account_view.apply_theme(self.current_theme)

def main():
    """Función principa"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo moderno
    
    # Configurar fuente de la aplicación
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Pantalla de carga
    splash_pix = QPixmap(700, 400)
    splash_pix.fill(QColor(COLOR_DARK))
    
    painter = QPainter(splash_pix)
    
    # Gradiente de fondo
    gradient = QLinearGradient(0, 0, 0, splash_pix.height())
    gradient.setColorAt(0, QColor(COLOR_PRIMARY))
    gradient.setColorAt(1, QColor(COLOR_SECONDARY))
    painter.fillRect(splash_pix.rect(), QBrush(gradient))
    
    # Logo y texto de la pantalla de carga
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Segoe UI", 48, QFont.Bold))
    painter.drawText(splash_pix.rect().adjusted(0, -50, 0, 0), Qt.AlignCenter, "FoodWizz")
    
    painter.setFont(QFont("Segoe UI", 20))
    painter.drawText(splash_pix.rect().adjusted(0, 20, 0, 0), Qt.AlignCenter, "Sistema de Gestión Avanzado")
    
    painter.setFont(QFont("Segoe UI", 14))
    painter.drawText(splash_pix.rect().adjusted(0, 80, 0, 0), Qt.AlignCenter, "v6.0 Pro")
    painter.end()

    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.show()

    # Barra de progreso mejorada
    progress = QProgressBar(splash)
    progress.setGeometry(100, splash_pix.height() - 80, splash_pix.width() - 200, 25)
    progress.setRange(0, 100)
    progress.setStyleSheet(f"""
        QProgressBar {{
            border: none;
            border-radius: 12px;
            text-align: center;
            color: white;
            background-color: rgba(255, 255, 255, 0.2);
            font-weight: bold;
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLOR_ACCENT}, stop:1 {COLOR_SUCCESS});
            border-radius: 12px;
        }}
    """)

    # Label de estado
    status_label = QLabel("Iniciando...", splash)
    status_label.setGeometry(100, splash_pix.height() - 50, splash_pix.width() - 200, 20)
    status_label.setAlignment(Qt.AlignCenter)
    status_label.setStyleSheet("color: white; font-size: 12px; font-weight: 600;")

    # Simular carga con hilo
    loading_thread = LoadingThread()
    loading_thread.progress_updated.connect(progress.setValue)
    loading_thread.status_updated.connect(status_label.setText)
    loading_thread.finished.connect(lambda: [splash.finish(window), window.show()])
    
    loading_thread.start()

    # Crear ventana principal
    window = MainWindow()
    
    app.processEvents()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()