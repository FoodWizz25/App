import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QScrollArea, QMainWindow,
    QListWidget, QListWidgetItem, QStackedLayout, QLineEdit,
    QComboBox, QDesktopWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QFileDialog, QDialog, QTabWidget,
    QProgressBar, QSplashScreen, QTextEdit, QMenu
)
from PyQt5.QtGui import QPixmap, QIcon, QCursor, QFont
from PyQt5.QtCore import Qt, QTimer, QSize, QEvent


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Colores para la aplicación
COLOR_PRIMARY = "#DDAA00"
COLOR_SECONDARY = "#85AAAA"
COLOR_DARK = "#173F4E"
COLOR_LIGHT_BG = "#FEFAE0"
COLOR_ACCENT = "#606C38"
COLOR_WARNING = "#FF7F0D"

# Temas para aplicación (claro y oscuro)
THEME_LIGHT = {
    "background": COLOR_LIGHT_BG,
    "text": COLOR_DARK,
    "primary": COLOR_PRIMARY,
    "secondary": COLOR_SECONDARY,
    "accent": COLOR_ACCENT,
    "warning": COLOR_WARNING,
    "card_bg": COLOR_LIGHT_BG,
    "button_bg": COLOR_PRIMARY,
    "button_hover": "#C79700",
    "button_pressed": "#B38A00",
}

THEME_DARK = {
    "background": "#131A1C",
    "text": "#E1E8EB",
    "primary": "#10B981",
    "secondary": "#256D85",
    "accent": "#4ADE80",
    "warning": "#FACC15",
    "card_bg": "#172727",
    "button_bg": "#10B981",
    "button_hover": "#0F766E",
    "button_pressed": "#0E6351",
}

# Definición de constantes para rutas de imágenes y archivo de datos
DEFAULT_IMAGE_PATH = "img/default.png"  # Ruta de la imagen por defecto
DATA_FILE = "productos.json"  # Archivo donde se guardan los datos de los productos

# -------------------------------------------------
# Funciones para cargar y guardar productos
# -------------------------------------------------

def load_products():
    # Carga los productos desde un archivo JSON o usa datos predeterminados
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [tuple(p) for p in data]
        except Exception:
            QMessageBox.warning(None, "Error", "No se pudo cargar productos.json. Se cargarán valores por defecto.")
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
        ("Oolong Tea", 4.00, "img/oolong_tea.jpg", "Drink", 22)
    ]

def save_products(products):
    # Guarda los productos en un archivo JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

products = load_products()

# -------------------------------------------------
# Widget de Tarjeta de Producto con diseño integrado
# -------------------------------------------------

class ProductCard(QWidget):
    def __init__(self, product):
        super().__init__()
        name, price, image_path, category, stock = product
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        self.setStyleSheet(f"""
            background-color: {COLOR_LIGHT_BG};
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 10px;
            padding: 10px;
        """)

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)
        image = QLabel()
        image.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK}; font-size: 16px; font-family: 'Nunito';")

        price_label = QLabel(f"${price:.2f}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 600; font-family: 'Nunito';")

        stock_label = QLabel(f"Stock: {stock}")
        stock_label.setAlignment(Qt.AlignCenter)
        stock_label.setStyleSheet(f"color: {COLOR_WARNING}; font-style: italic; font-family: 'Nunito';")

        # Botón de favoritos con toggle y iconos modernos
        self.fav_button = QPushButton()
        self.fav_button.setCheckable(True)
        self.fav_button.setFixedSize(24, 24)
        self.fav_button.setStyleSheet("QPushButton { border: none; }")
        self.fav_button.setIcon(QIcon("heart_empty.png"))
        self.fav_button.toggled.connect(self.toggle_favorite)

        layout.addWidget(image, alignment=Qt.AlignCenter)
        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(stock_label)
        layout.addWidget(self.fav_button, alignment=Qt.AlignCenter)

    def toggle_favorite(self, checked):
        self.fav_button.setIcon(QIcon("heart_filled.png" if checked else "heart_empty.png"))

# -------------------------------------------------
# Widgets para la pestaña de Cuenta - NUEVO IMPLEMENTACION MODERNA
# -------------------------------------------------

# Sección: Tarjeta reutilizable con título e ícono  
class Card(QWidget):
    def __init__(self, title, icon_path):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(10)
        self.setStyleSheet(f"""
            background-color: {COLOR_LIGHT_BG};
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 12px;
        """)
        # Header con icono y título
        header = QHBoxLayout()
        icon_lbl = QLabel()
        icon_lbl.setPixmap(QPixmap(icon_path).scaled(24,24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_lbl.setFixedSize(28, 28)
        header.addWidget(icon_lbl)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet(f"font-weight: 900; font-size: 18px; color: {COLOR_DARK}; font-family: 'Nunito';")
        header.addWidget(title_lbl)
        header.addStretch()
        self.main_layout.addLayout(header)
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(8)
        self.main_layout.addLayout(self.content_layout)


# ==========================
# Perfil del usuario
# ==========================
class UserProfileCard(Card):
    def __init__(self):
        super().__init__("Perfil del Usuario", "icons/user_icon.png")
        # Imagen perfil editable
        self.profile_pic = QLabel()
        self.profile_pic.setFixedSize(128,128)
        self.profile_pic.setStyleSheet(f"border-radius: 64px; border: 3px solid {COLOR_PRIMARY}; background-color: {COLOR_LIGHT_BG};")
        self.profile_pic.setCursor(QCursor(Qt.PointingHandCursor))
        # Imagen default placeholder
        pix = QPixmap("https://storage.googleapis.com/workspace-0f70711f-8b4e-4d94-86f1-2a93ccde5887/image/d3bfd620-33d3-4efb-9f74-b1c63e50577e.png")
        self.profile_pic.setPixmap(pix.scaled(128,128,Qt.KeepAspectRatio,Qt.SmoothTransformation))
        self.profile_pic.mousePressEvent = self.change_profile_picture
        self.content_layout.addWidget(self.profile_pic, alignment=Qt.AlignCenter)

        # Campos de información
        self.name_edit = QLineEdit("Nombre completo")
        self.name_edit.setPlaceholderText("Nombre completo")
        self.email_edit = QLineEdit("correo@empresa.com")
        self.email_edit.setPlaceholderText("Correo electrónico corporativo")
        self.phone_edit = QLineEdit("+1 555 123 4567")
        self.phone_edit.setPlaceholderText("Número de teléfono")
        self.business_edit = QLineEdit("Nombre de la empresa o negocio")
        self.business_edit.setPlaceholderText("Empresa o nombre del negocio")

        # Estilo coherente para inputs
        for w in [self.name_edit, self.email_edit, self.phone_edit, self.business_edit]:
            w.setStyleSheet(f"""
                border: 1.5px solid {COLOR_SECONDARY};
                border-radius: 6px;
                padding: 6px 10px;
                font-family: 'Nunito';
                font-size: 14px;
                color: {COLOR_DARK};
            """)

        self.content_layout.addWidget(self.name_edit)
        self.content_layout.addWidget(self.email_edit)
        self.content_layout.addWidget(self.phone_edit)
        self.content_layout.addWidget(self.business_edit)

        self.save_btn = QPushButton("Guardar Cambios")
        self.save_btn.setFixedHeight(32)
        self.save_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.save_btn.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            font-weight: 900;
            font-family: 'Nunito';
            border-radius: 8px;
        """)
        self.save_btn.clicked.connect(self.save_profile)
        self.content_layout.addWidget(self.save_btn)

    def change_profile_picture(self, event):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar foto de perfil", "", "Imágenes (*.png *.jpg *.jpeg *.png)")
        if file_path:
            pix = QPixmap(file_path)
            if pix.isNull():
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen seleccionada.")
            else:
                self.profile_pic.setPixmap(pix.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def save_profile(self):
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        phone = self.phone_edit.text().strip()
        business = self.business_edit.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Validación", "Nombre y correo electrónico son obligatorios.")
            return
        # Simulación guardado
        QMessageBox.information(self, "Guardado", "Perfil guardado correctamente.")

# ==========================
# Datos de la Cuenta
# ==========================

class AccountDataCard(Card):
    def __init__(self):
        super().__init__("Datos de la Cuenta", "icons/account_icon.png")
        # Usamos QLabel estilizados para mostrar info estática
        self.user_id_lbl = QLabel("ID de Usuario: 001245")
        self.registration_lbl = QLabel("Fecha de registro: 22/12/2022")
        self.account_type_lbl = QLabel("Tipo de cuenta: Premium")
        self.sub_status_lbl = QLabel("Estado suscripción: Activa")

        for lbl in [self.user_id_lbl, self.registration_lbl, self.account_type_lbl, self.sub_status_lbl]:
            lbl.setStyleSheet(f"font-size: 14px; color: {COLOR_DARK}; font-family: 'Nunito'; padding-left:6px;")
            self.content_layout.addWidget(lbl)

# ==========================
# Configuración de la Aplicación
# ==========================

class AppSettingsCard(Card):
    def __init__(self, theme_change_callback, lang_change_callback):
        super().__init__("Configuración de la Aplicación", "icons/settings_icon.png")

        self.theme_change_callback = theme_change_callback
        self.lang_change_callback = lang_change_callback

        # Idioma
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Seleccionar idioma:")
        lang_label.setStyleSheet(f"font-weight: 700; font-family: 'Nunito'; color: {COLOR_DARK};")
        lang_layout.addWidget(lang_label)
        self.lang_combo = QComboBox()
        # Idiomas comunes
        self.lang_combo.addItems([
            "Español", "Inglés", "Francés", "Alemán", "Portugués", "Italiano", "Japonés"
        ])
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        self.content_layout.addLayout(lang_layout)

        # Tema
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Selector de tema:")
        theme_label.setStyleSheet(f"font-weight: 700; font-family: 'Nunito'; color: {COLOR_DARK};")
        theme_layout.addWidget(theme_label)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Claro", "Oscuro"])
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        self.content_layout.addLayout(theme_layout)

        self.apply_btn = QPushButton("Aplicar Cambios")
        self.apply_btn.clicked.connect(self.apply_changes)
        self.content_layout.addWidget(self.apply_btn)

        # Conectar señales de cambio para actualización inmediata
        self.lang_combo.currentIndexChanged.connect(self.apply_changes)
        self.theme_combo.currentIndexChanged.connect(self.apply_changes)

    def apply_changes(self):
        selected_theme = self.theme_combo.currentText()
        selected_lang = self.lang_combo.currentText()

        if self.theme_change_callback:
            self.theme_change_callback(selected_theme)
        if self.lang_change_callback:
            self.lang_change_callback(selected_lang)

        # Notificación
        # QMessageBox.information(self, "Configuración", "Idioma y tema aplicados.")

# ==========================
# Historial de Actividad
# ==========================

class ActivityHistoryCard(Card):
    def __init__(self):
        super().__init__("Historial de Actividad", "icons/history_icon.png")

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Fecha", "Acción", "Descripción"])
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.content_layout.addWidget(self.table)

        self.load_activity()

    def load_activity(self):
        # Datos simulados
        actions = [
            ("2023-01-01", "Agregar Producto", "Se añadió 'Beef Ramen' con stock inicial."),
            ("2023-01-05", "Editar Producto", "Actualización precio 'Sushi Roll'."),
            ("2023-01-11", "Eliminar Producto", "Se eliminó 'Yakisoba'."),
            ("2023-01-15", "Cambiar Stock", "Stock actualizado para 'Miso Soup'."),
            ("2023-01-20", "Actualizar Configuración", "Se cambió el tema a oscuro."),
        ]
        self.table.setRowCount(len(actions))
        for r, (fecha, accion, desc) in enumerate(actions):
            self.table.setItem(r, 0, QTableWidgetItem(fecha))
            self.table.setItem(r, 1, QTableWidgetItem(accion))
            self.table.setItem(r, 2, QTableWidgetItem(desc))
        self.table.resizeColumnsToContents()

# ==========================
# Soporte y Ayuda
# ==========================

class SupportHelpCard(Card):
    def __init__(self):
        super().__init__("Soporte y Ayuda", "icons/support_icon.png")

        self.faq_btn = QPushButton("Centro de Ayuda (FAQ)")
        self.faq_btn.clicked.connect(self.open_faq)
        self.contact_btn = QPushButton("Contactar Soporte")
        self.contact_btn.clicked.connect(self.contact_support)
        self.suggestions_btn = QPushButton("Enviar Sugerencias")
        self.suggestions_btn.clicked.connect(self.send_suggestions)

        for btn in [self.faq_btn, self.contact_btn, self.suggestions_btn]:
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"""
                background-color: {COLOR_PRIMARY};
                color: {COLOR_DARK};
                font-weight: 900;
                font-family: 'Nunito';
                border-radius: 8px;
            """)
            self.content_layout.addWidget(btn)

    def open_faq(self):
        QMessageBox.information(self, "Centro de Ayuda", "Acceso al Centro de Ayuda.")

    def contact_support(self):
        QMessageBox.information(self, "Contactar Soporte", "Información para contactar soporte.")

    def send_suggestions(self):
        QMessageBox.information(self, "Enviar Sugerencias", "Formulario para enviar sugerencias.")

# ==========================
# Términos y Seguridad
# ==========================

class TermsSecurityCard(Card):
    def __init__(self):
        super().__init__("Términos y Seguridad", "icons/terms_icon.png")

        self.privacy_btn = QPushButton("Política de Privacidad")
        self.privacy_btn.clicked.connect(self.open_privacy)
        self.terms_btn = QPushButton("Términos y Condiciones")
        self.terms_btn.clicked.connect(self.open_terms)
        self.logout_btn = QPushButton("Cerrar Sesión")
        self.logout_btn.clicked.connect(self.logout)
        self.delete_btn = QPushButton("Eliminar Cuenta")
        self.delete_btn.clicked.connect(self.delete_account)

        for btn in [self.privacy_btn, self.terms_btn, self.logout_btn, self.delete_btn]:
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.setFixedHeight(32)
            btn.setStyleSheet(f"""
                background-color: {COLOR_PRIMARY};
                color: {COLOR_DARK};
                font-weight: 900;
                font-family: 'Nunito';
                border-radius: 8px;
                margin-bottom: 8px;
            """)
            self.content_layout.addWidget(btn)

    def open_privacy(self):
        QMessageBox.information(self, "Política de Privacidad", "Acceso a la Política de Privacidad.")

    def open_terms(self):
        QMessageBox.information(self, "Términos y Condiciones", "Acceso a los Términos y Condiciones.")

    def logout(self):
        QMessageBox.information(self, "Cerrar Sesión", "Has cerrado sesión correctamente.")

    def delete_account(self):
        reply = QMessageBox.question(self, "Eliminar Cuenta", "¿Seguro que desea eliminar su cuenta? Esta acción es irreversible.", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "Cuenta Eliminada", "Su cuenta ha sido eliminada.")

# -------------------------------------------------
# Vista personal para "Cuenta"
# -------------------------------------------------

class AccountView(QWidget):
    def __init__(self, theme_callback, lang_callback):
        super().__init__()
        self.theme_callback = theme_callback
        self.lang_callback = lang_callback
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setContentsMargins(20,20,20,20)
        self.layout.setSpacing(20)

        # Crear todas las tarjetas y agregarlas
        self.profile_card = UserProfileCard()
        self.account_data_card = AccountDataCard()
        self.app_settings_card = AppSettingsCard(self.theme_callback, self.lang_callback)
        self.activity_card = ActivityHistoryCard()
        self.support_card = SupportHelpCard()
        self.terms_card = TermsSecurityCard()

        for card in [self.profile_card, self.account_data_card, self.app_settings_card,
                     self.activity_card, self.support_card, self.terms_card]:
            card.setMinimumWidth(400)
            self.layout.addWidget(card)

        self.layout.addStretch()
        scroll.setWidget(container)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)


# -------------------------------------------------
# Vista de Reportes con gráficos (sin cambios)
# -------------------------------------------------

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Reportes y Análisis de Ganancias")
        title.setStyleSheet(f"font-size: 22px; font-weight: 900; color: {COLOR_DARK}; font-family: 'Nunito';")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addSpacing(15)

        # Datos simulados
        self.months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
        self.ganancias = [1200, 1800, 1500, 2100, 1900, 2300]
        self.categorias = ['Ramen', 'Drink', 'Other']
        self.ventas_categoria = [5500, 3200, 2100]

        # Crear gráficos
        self.fig = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Dibujar todos los gráficos
        self.draw_plots()

    def draw_plots(self):
        self.fig.clear()

        ax1 = self.fig.add_subplot(2, 2, 1)
        ax1.bar(self.months, self.ganancias, color=COLOR_PRIMARY, edgecolor=COLOR_ACCENT)
        ax1.set_title('Ganancias Mensuales')
        ax1.set_ylabel('Ganancias ($)')
        ax1.tick_params(axis='x', rotation=30)

        ax2 = self.fig.add_subplot(2, 2, 2)
        ax2.plot(self.months, self.ganancias, marker='o', linestyle='-', color=COLOR_DARK)
        ax2.set_title('Evolución de Ganancias')
        ax2.set_ylabel('Ganancias ($)')
        ax2.tick_params(axis='x', rotation=30)

        ax3 = self.fig.add_subplot(2, 1, 2)
        ax3.pie(self.ventas_categoria,
                labels=self.categorias,
                autopct='%1.1f%%',
                colors=[COLOR_PRIMARY, COLOR_SECONDARY, COLOR_DARK],
                startangle=140,
                wedgeprops=dict(edgecolor='w'))
        ax3.set_title('Ventas por Categoría')

        self.fig.tight_layout()
        self.canvas.draw()

# -------------------------------------------------
# Vista de órdenes con filtros y grid de productos (sin cambios)
# -------------------------------------------------

class OrdersView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        controls = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.setFixedHeight(30)
        self.search_input.textChanged.connect(self.update_product_grid)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["All", "Ramen", "Drink", "Other"])
        self.category_filter.setFixedHeight(30)
        self.category_filter.currentTextChanged.connect(self.update_product_grid)

        controls.addWidget(self.search_input)
        controls.addWidget(self.category_filter)
        layout.addLayout(controls)

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setLayout(self.grid)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.update_product_grid()
        self.setLayout(layout)

    def update_product_grid(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.deleteLater()

        search = self.search_input.text().lower()
        cat = self.category_filter.currentText()

        row = col = 0
        for product in products:
            name, price, img, category, stock = product
            if (cat != "All" and category != cat) or (search and search not in name.lower()):
                continue
            card = ProductCard(product)
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

# -------------------------------------------------
# Vista de Inventario (sin cambios)
# -------------------------------------------------

class InventoryView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.inventory_search = QLineEdit()
        self.inventory_search.setPlaceholderText("Buscar en inventario...")
        self.inventory_search.setFixedHeight(30)
        self.inventory_search.textChanged.connect(self.update_inventory_table)
        layout.addWidget(self.inventory_search)

        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(["Imagen", "Producto", "Categoría", "Precio", "Stock"])
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.setColumnWidth(0, 60)
        layout.addWidget(self.inventory_table)

        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar Producto")
        btn_del = QPushButton("Eliminar Producto")
        btn_add.clicked.connect(self.add_product)
        btn_del.clicked.connect(self.remove_product)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)

        self.update_inventory_table()
        self.setLayout(layout)

    def update_inventory_table(self):
        search = self.inventory_search.text().lower()
        filtered = [p for p in products if search in p[0].lower()]

        self.inventory_table.setRowCount(len(filtered))
        for r, (n, pr, img, cat, st) in enumerate(filtered):
            lbl = QLabel()
            pm = QPixmap(img)
            if pm.isNull():
                pm = QPixmap(DEFAULT_IMAGE_PATH)
            lbl.setPixmap(pm.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lbl.setAlignment(Qt.AlignCenter)
            self.inventory_table.setCellWidget(r, 0, lbl)
            self.inventory_table.setItem(r, 1, QTableWidgetItem(n))
            self.inventory_table.setItem(r, 2, QTableWidgetItem(cat))
            self.inventory_table.setItem(r, 3, QTableWidgetItem(f"${pr:.2f}"))
            self.inventory_table.setItem(r, 4, QTableWidgetItem(str(st)))
        self.inventory_table.resizeRowsToContents()

    def add_product(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Producto")
        dialog.setFixedSize(400, 320)
        layout = QVBoxLayout(dialog)

        fields = {}
        for key in ["Nombre", "Categoría", "Precio", "Stock"]:
            h = QHBoxLayout()
            h.addWidget(QLabel(f"{key}:"))
            le = QLineEdit()
            h.addWidget(le)
            layout.addLayout(h)
            fields[key] = le

        self.selected_image_path = DEFAULT_IMAGE_PATH
        btn_img = QPushButton("Seleccionar Imagen")
        btn_img.clicked.connect(lambda: self.select_image(dialog))
        layout.addWidget(btn_img)

        btn_create = QPushButton("Crear")
        btn_create.clicked.connect(lambda: self.validate_and_create(fields, dialog))
        layout.addWidget(btn_create)

        dialog.exec_()

    def select_image(self, dialog):
        file_path, _ = QFileDialog.getOpenFileName(dialog, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path

    def validate_and_create(self, fields, dialog):
        try:
            name = fields["Nombre"].text().strip()
            cat = fields["Categoría"].text().strip()
            price = float(fields["Precio"].text())
            stock = int(fields["Stock"].text())

            if not name or not cat:
                raise ValueError("Nombre y categoría son obligatorios.")
            if price < 0 or stock < 0:
                raise ValueError("Precio y stock deben ser cero o positivos.")

            products.append((name, price, self.selected_image_path, cat, stock))
            save_products(products)
            self.update_inventory_table()
            dialog.accept()
        except ValueError as e:
            QMessageBox.warning(dialog, "Entrada no válida", str(e))

    def remove_product(self):
        row = self.inventory_table.currentRow()
        if row < 0:
            return
        name = self.inventory_table.item(row, 1).text()
        for i, p in enumerate(products):
            if p[0] == name:
                del products[i]
                break
        save_products(products)
        self.update_inventory_table()

# -------------------------------------------------
# Ventana Principal con integración sección cuenta, cambios a tema e idioma
# -------------------------------------------------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FoodWizz - Sistema de Inventario")
        self.setWindowIcon(QIcon("app_icon.png"))
        self.setMinimumSize(1300, 620)
        qt_rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qt_rect.moveCenter(center)
        self.move(qt_rect.topLeft())

        container = QWidget()
        self.setCentralWidget(container)
        self.main_layout = QHBoxLayout(container)

        self.menu = QListWidget()
        sections = {
            "Órdenes": "order.png",
            "Inventario": "inventory.png",
            "Reportes": "report.png",
            "Cuenta": "account.png"
        }
        for section, icon_path in sections.items():
            item = QListWidgetItem(QIcon(icon_path), section)
            self.menu.addItem(item)
        self.menu.setFixedWidth(160)
        self.menu.setStyleSheet(f"""
            QListWidget {{
                background-color: {COLOR_SECONDARY};
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
                font-family: 'Nunito';
            }}
            QListWidget::item {{ padding: 10px; height: 40px; }}
            QListWidget::item:selected {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_DARK};
                font-weight: bold;
            }}
        """)

        # Current settings state
        self.current_theme = "Claro"  # default
        self.current_language = "Español"

        # Create Views
        self.orders_view = OrdersView()
        self.inventory_view = InventoryView()
        self.reports_view = ReportsView()
        self.account_view = AccountView(
            theme_callback=self.apply_theme,
            lang_callback=self.apply_language
        )

        self.stack = QStackedLayout()
        self.stack.addWidget(self.orders_view)
        self.stack.addWidget(self.inventory_view)
        self.stack.addWidget(self.reports_view)
        self.stack.addWidget(self.account_view)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.main_layout.addWidget(self.menu)
        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        self.main_layout.addWidget(content_widget)

        # Apply default theme and language initially
        self.apply_theme(self.current_theme)
        self.apply_language(self.current_language)

    def apply_theme(self, theme_name):
        if theme_name == "Oscuro":
            theme = THEME_DARK
        else:
            theme = THEME_LIGHT
        style = f"""
            QMainWindow {{
                background-color: {theme['background']};
                font-family: 'Nunito', sans-serif;
                color: {theme['text']};
            }}
            QListWidget {{
                background-color: {theme['secondary']};
                color: {theme['text']};
                font-size: 16px;
                padding: 10px;
                border: none;
                font-family: 'Nunito';
            }}
            QListWidget::item {{
                padding: 10px;
                height: 40px;
            }}
            QListWidget::item:selected {{
                background-color: {theme['primary']};
                color: {theme['background']};
                font-weight: bold;
            }}
            QPushButton {{
                background-color: {theme['button_bg']};
                border: none;
                padding: 6px 12px;
                border-radius: 5px;
                font-weight: bold;
                color: {theme['background']};
                min-height: 32px;
                font-family: 'Nunito';
            }}
            QPushButton:hover {{
                background-color: {theme['button_hover']};
            }}
            QPushButton:pressed {{
                background-color: {theme['button_pressed']};
            }}
            QLabel {{
                color: {theme['text']};
                font-family: 'Nunito';
            }}
            QTableWidget {{
                background-color: {theme['card_bg']};
                color: {theme['text']};
                gridline-color: {theme['primary']};
                selection-background-color: {theme['primary']};
                selection-color: {theme['background']};
                font-family: 'Nunito';
            }}
            QHeaderView::section {{
                background-color: {theme['primary']};
                color: {theme['background']};
                padding: 4px;
                border: 1px solid {theme['secondary']};
                font-family: 'Nunito';
            }}
            QScrollArea {{
                background-color: {theme['background']};
                border: none;
            }}
            QLineEdit, QComboBox, QTextEdit {{
                border: 2px solid {theme['secondary']};
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                background-color: {theme['card_bg']};
                color: {theme['text']};
                font-family: 'Nunito';
            }}
        """
        self.setStyleSheet(style)
        self.current_theme = theme_name

    def apply_language(self, language_name):
        # Simple translation dictionary for key UI text for demo purposes
        translations = {
            "Español": {
                "Órdenes": "Órdenes",
                "Inventario": "Inventario",
                "Reportes": "Reportes",
                "Cuenta": "Cuenta",
            },
            "Inglés": {
                "Órdenes": "Orders",
                "Inventario": "Inventory",
                "Reportes": "Reports",
                "Cuenta": "Account",
            },
            "Francés": {
                "Órdenes": "Commandes",
                "Inventario": "Inventaire",
                "Reportes": "Rapports",
                "Cuenta": "Compte",
            },
            "Alemán": {
                "Órdenes": "Bestellungen",
                "Inventario": "Inventar",
                "Reportes": "Berichte",
                "Cuenta": "Konto",
            },
            "Portugués": {
                "Órdenes": "Pedidos",
                "Inventario": "Inventário",
                "Reportes": "Relatórios",
                "Cuenta": "Conta",
            },
            "Italiano": {
                "Órdenes": "Ordini",
                "Inventario": "Inventario",
                "Reportes": "Rapporti",
                "Cuenta": "Account",
            },
            "Japonés": {
                "Órdenes": "注文",
                "Inventario": "在庫",
                "Reportes": "レポート",
                "Cuenta": "アカウント",
            },
        }
        map_dict = translations.get(language_name, translations["Español"])

        # Actualizar etiquetas del menú
        for idx in range(self.menu.count()):
            text = self.menu.item(idx).text()
            key = text
            for k,v in map_dict.items():
                if v == text:
                    key = k
                    break
            new_text = map_dict.get(key, text)
            self.menu.item(idx).setText(new_text)

        self.current_language = language_name

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Aplicar fuente moderna If available
    try:
        from PyQt5.QtGui import QFontDatabase
        QFontDatabase.addApplicationFont("fonts/Nunito-Regular.ttf")
    except Exception:
        pass

    splash_pix = QPixmap("pantalla_de_carga.png")
    splash = QSplashScreen(splash_pix)
    splash.setWindowFlag(Qt.FramelessWindowHint)
    splash.setWindowOpacity(0.9)
    splash.showMessage("Cargando... 0%", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    splash.show()

    app.processEvents()

    window = MainWindow()
    window.show()

    splash.finish(window)
    sys.exit(app.exec_())
