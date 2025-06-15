import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QScrollArea, QMainWindow,
    QListWidget, QListWidgetItem, QStackedLayout, QLineEdit,
    QComboBox, QDesktopWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QFileDialog, QDialog, QTabWidget
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

# Definición de constantes para rutas de imágenes y archivo de datos
DEFAULT_IMAGE_PATH = "img/default.png"  # Ruta de la imagen por defecto
DATA_FILE = "productos.json"  # Archivo JSON para almacenar los productos

# Colores para la aplicación
COLOR_PRIMARY = "#DDAA00"  # Color primario
COLOR_SECONDARY = "#85AAAA"  # Color secundario
COLOR_DARK = "#173F4E"  # Color oscuro
COLOR_LIGHT_BG = "#FEFAE0"  # Color de fondo claro
COLOR_ACCENT = "#606C38"  # Color de acento
COLOR_WARNING = "#FF7F0D"  # Color de advertencia

# Función para cargar productos desde un archivo JSON
def load_products():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [tuple(p) for p in data]
        except Exception:
            QMessageBox.warning(None, "Error", "No se pudo cargar productos.json. Se cargarán valores por defecto.")
    # Lista de productos por defecto
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

# Función para guardar productos en un archivo JSON
def save_products(products):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)

products = load_products()  # Cargar productos al iniciar

# Widget de Tarjeta de Producto
class ProductCard(QWidget):
    def __init__(self, name, price, image_path, stock):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)  # Márgenes del layout
        layout.setSpacing(6)  # Espacio entre widgets
        self.setStyleSheet(f"""
            background-color: {COLOR_LIGHT_BG};
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 10px;
        """)
        # Cargar imagen del producto
        pixmap = QPixmap(image_path)
        if pixmap.isNull():  # Si la imagen no se carga, usar una por defecto
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)
        image = QLabel()
        image.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        # Configurar etiquetas para nombre, precio y stock
        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK}; font-size: 16px;")
        price_label = QLabel(f"${price:.2f}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 600;")
        stock_label = QLabel(f"Stock: {stock}")
        stock_label.setAlignment(Qt.AlignCenter)
        stock_label.setStyleSheet(f"color: {COLOR_WARNING}; font-style: italic;")

        # Añadir widgets al layout
        layout.addWidget(image)
        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(stock_label)

# Widgets para la pestaña de Cuenta
class PersonalInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)  # Márgenes del layout
        layout.setSpacing(12)  # Espacio entre widgets
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK};")

        # Título de la pestaña
        title = QLabel("Información Personal")
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; margin-bottom: 6px; color: {COLOR_PRIMARY};")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        # Subtítulo de la pestaña
        subtitle = QLabel("Información sobre ti y tus preferencias en los servicios")
        subtitle.setStyleSheet(f"font-size: 14px; margin-bottom: 12px; color:{COLOR_ACCENT};")
        layout.addWidget(subtitle)

        # Imagen de perfil
        self.pic_label = QLabel()
        self.pic_label.setFixedSize(128, 128)
        default_pix = QPixmap(DEFAULT_IMAGE_PATH)
        if default_pix.isNull():
            default_pix = QPixmap(128, 128)
            default_pix.fill(Qt.lightGray)
        self.pic_label.setPixmap(default_pix.scaled(128, 128, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.pic_label, alignment=Qt.AlignLeft)

        # Formulario para información personal
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(14)
        form_layout.setVerticalSpacing(10)
        form_layout.addWidget(QLabel("Nombre:"), 0, 0, alignment=Qt.AlignRight)
        form_layout.addWidget(QLineEdit("Humano Morales",
                                     placeholderText="Ingresa tu nombre",
                                     styleSheet=f"border: 1.5px solid {COLOR_SECONDARY}; padding: 6px;"), 0, 1)
        self.name_edit = form_layout.itemAtPosition(0, 1).widget()

        form_layout.addWidget(QLabel("Fecha de nacimiento:"), 1, 0, alignment=Qt.AlignRight)
        self.dob_edit = QLineEdit("", placeholderText="dd/mm/aaaa")
        self.dob_edit.setStyleSheet(f"border: 1.5px solid {COLOR_SECONDARY}; padding: 6px;")
        form_layout.addWidget(self.dob_edit, 1, 1)

        form_layout.addWidget(QLabel("Género:"), 2, 0, alignment=Qt.AlignRight)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Prefiero no decirlo", "Masculino", "Femenino", "Otro"])
        self.gender_combo.setStyleSheet(f"border: 1.5px solid {COLOR_SECONDARY}; padding: 4px;")
        form_layout.addWidget(self.gender_combo, 2, 1)

        form_layout.addWidget(QLabel("Correo electrónico:"), 3, 0, alignment=Qt.AlignRight)
        self.email_edit = QLineEdit("", placeholderText="correo@ejemplo.com")
        self.email_edit.setStyleSheet(f"border: 1.5px solid {COLOR_SECONDARY}; padding: 6px;")
        form_layout.addWidget(self.email_edit, 3, 1)

        form_layout.addWidget(QLabel("Teléfono:"), 4, 0, alignment=Qt.AlignRight)
        self.phone_edit = QLineEdit("", placeholderText="(000) 000-0000")
        self.phone_edit.setStyleSheet(f"border: 1.5px solid {COLOR_SECONDARY}; padding: 6px;")
        form_layout.addWidget(self.phone_edit, 4, 1)

        layout.addLayout(form_layout)

        # Botón para guardar información
        self.save_btn = QPushButton("Guardar Información")
        self.save_btn.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 10px 20px;
            font-weight: bold;
            border-radius: 8px;
        """)
        self.save_btn.clicked.connect(self.save_info)
        layout.addWidget(self.save_btn, alignment=Qt.AlignLeft)

    # Método para guardar información personal
    def save_info(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        QMessageBox.information(self, "Guardado", "Información personal guardada correctamente.")

class PaymentSubscriptionsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK};")

        # Título de la pestaña
        title = QLabel("Pagos y Suscripciones")
        title.setStyleSheet(f"font-size: 20px; font-weight: bold; margin-bottom: 10px; color: {COLOR_PRIMARY};")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        # Descripción de la pestaña
        info_label = QLabel("Tu información de pagos, transacciones y suscripciones activas.")
        info_label.setStyleSheet(f"font-size: 14px; color:{COLOR_ACCENT}; margin-bottom: 18px;")
        layout.addWidget(info_label)

        # Grupo para el plan de suscripción actual
        plan_group = QWidget()
        plan_layout = QVBoxLayout(plan_group)
        plan_layout.setSpacing(8)
        plan_label = QLabel("Plan de Suscripción Actual")
        plan_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK};")
        plan_layout.addWidget(plan_label)

        self.plan_name_label = QLabel("Pro Plan")
        self.plan_name_label.setStyleSheet(f"font-size: 16px; font-weight: 600; color: {COLOR_PRIMARY};")
        plan_layout.addWidget(self.plan_name_label)

        plan_desc = QLabel("El Pro Plan te permite obtener todas las características premium de FoodWizz.")
        plan_desc.setStyleSheet(f"font-size: 13px; color: {COLOR_ACCENT};")
        plan_layout.addWidget(plan_desc)

        # Botón para actualizar plan
        btn_upgrade = QPushButton("Actualizar Plan")
        btn_upgrade.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_upgrade.clicked.connect(self.upgrade_plan_dialog)
        plan_layout.addWidget(btn_upgrade)

        layout.addWidget(plan_group)

        # Grupo para el almacenamiento de la cuenta
        storage_group = QWidget()
        storage_layout = QVBoxLayout(storage_group)
        storage_layout.setSpacing(8)
        storage_label = QLabel("Almacenamiento de la cuenta")
        storage_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK};")
        storage_layout.addWidget(storage_label)

        self.storage_bar = QLabel("70% de 1 TB en uso")
        self.storage_bar.setStyleSheet(f"color: {COLOR_ACCENT};")
        storage_layout.addWidget(self.storage_bar)

        # Botón para administrar almacenamiento
        btn_manage_storage = QPushButton("Administrar almacenamiento")
        btn_manage_storage.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_manage_storage.clicked.connect(self.manage_storage_clicked)
        storage_layout.addWidget(btn_manage_storage)

        layout.addWidget(storage_group)

        # Grupo para formas de pago
        payment_group = QWidget()
        payment_layout = QVBoxLayout(payment_group)
        payment_layout.setSpacing(8)
        payment_label = QLabel("Formas de pago")
        payment_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK};")
        payment_layout.addWidget(payment_label)

        payment_desc = QLabel("Las formas de pago se guardan para que puedas usarlas cómodamente.")
        payment_desc.setStyleSheet(f"font-size: 13px; color: {COLOR_ACCENT};")
        payment_layout.addWidget(payment_desc)

        self.payment_methods_list = QVBoxLayout()
        card1 = self.create_payment_card("Tarjeta Visa", "**** **** **** 1234", "12/24")
        card2 = self.create_payment_card("Paypal", "feomorales@gmail.com", "Cuenta activa")
        self.payment_methods_list.addWidget(card1)
        self.payment_methods_list.addWidget(card2)
        payment_layout.addLayout(self.payment_methods_list)

        # Botón para administrar formas de pago
        btn_manage_pm = QPushButton("Administrar formas de pago")
        btn_manage_pm.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_manage_pm.clicked.connect(self.manage_payments_clicked)
        payment_layout.addWidget(btn_manage_pm)

        layout.addWidget(payment_group)

        # Grupo para suscripciones
        subs_group = QWidget()
        subs_layout = QVBoxLayout(subs_group)
        subs_layout.setSpacing(8)
        subs_label = QLabel("Suscripciones")
        subs_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK};")
        subs_layout.addWidget(subs_label)

        subs_desc = QLabel("Visualiza tus pagos recurrentes de servicios por suscripción.")
        subs_desc.setStyleSheet(f"font-size: 13px; color: {COLOR_ACCENT};")
        subs_layout.addWidget(subs_desc)

        sub1 = QLabel("• Renovación: 12/10/2025")
        sub2 = QLabel("• Renovación: 01/01/2026")
        sub1.setStyleSheet(f"color: {COLOR_ACCENT};")
        sub2.setStyleSheet(f"color: {COLOR_ACCENT};")
        subs_layout.addWidget(sub1)
        subs_layout.addWidget(sub2)

        # Botón para administrar suscripciones
        btn_manage_subs = QPushButton("Administrar suscripciones")
        btn_manage_subs.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 8px 14px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_manage_subs.clicked.connect(self.manage_subscriptions_clicked)
        subs_layout.addWidget(btn_manage_subs)

        layout.addWidget(subs_group)
        layout.addStretch()

    # Método para crear una tarjeta de pago
    def create_payment_card(self, method_type, details, extra):
        card = QWidget()
        card.setStyleSheet(f"""
            background-color: {COLOR_SECONDARY};
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 6px;
        """)
        h_layout = QHBoxLayout(card)
        texts = QVBoxLayout()
        lbl_type = QLabel(f"<b>{method_type}</b>")
        lbl_type.setStyleSheet(f"color: {COLOR_DARK};")
        lbl_details = QLabel(details)
        lbl_details.setStyleSheet(f"color: {COLOR_DARK};")
        lbl_extra = QLabel(f"<i>{extra}</i>")
        lbl_extra.setStyleSheet(f"color: {COLOR_ACCENT}; font-size: 11px;")
        texts.addWidget(lbl_type)
        texts.addWidget(lbl_details)
        texts.addWidget(lbl_extra)
        h_layout.addLayout(texts)
        h_layout.addStretch()
        return card

    # Método para actualizar el plan de suscripción
    def upgrade_plan_dialog(self):
        plans = ["Basic Plan (Gratis)", "Pro Plan", "Wizz Plan (Premium)"]
        plan, ok = QInputDialog.getItem(self, "Actualizar Plan", "Selecciona un plan de suscripción:", plans, 1, False)
        if ok and plan:
            self.plan_name_label.setText(plan)
            QMessageBox.information(self, "Plan Actualizado", f"Has actualizado al {plan}.")

    # Métodos para manejar clics en botones
    def manage_storage_clicked(self):
        QMessageBox.information(self, "Administrar almacenamiento", "Funcionalidad para administrar almacenamiento próximamente.")

    def manage_payments_clicked(self):
        QMessageBox.information(self, "Administrar pagos", "Funcionalidad para administrar formas de pago próximamente.")

    def manage_subscriptions_clicked(self):
        QMessageBox.information(self, "Administrar suscripciones", "Funcionalidad para administrar suscripciones próximamente.")

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK};")

        # Título de la pestaña
        title = QLabel("Reportes")
        title.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {COLOR_PRIMARY}; margin-bottom: 16px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        # Tabla para mostrar reportes
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(4)
        self.report_table.setHorizontalHeaderLabels(["Producto", "Categoría", "Ventas", "Ingresos"])
        self.report_table.verticalHeader().setVisible(False)
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.report_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.report_table.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_LIGHT_BG};
                font-weight: bold;
                padding: 4px;
            }}
            QTableWidget {{
                background-color: {COLOR_LIGHT_BG};
                gridline-color: {COLOR_SECONDARY};
                font-size: 14px;
            }}
            QTableWidget QTableCornerButton::section {{
                background-color: {COLOR_PRIMARY};
            }}
        """)

        layout.addWidget(self.report_table)

        self.update_report_table()  # Actualizar tabla de reportes

    # Método para actualizar la tabla de reportes
    def update_report_table(self):
        self.report_table.setRowCount(len(products))
        for r, (n, pr, _, cat, st) in enumerate(products):
            self.report_table.setItem(r, 0, QTableWidgetItem(n))
            self.report_table.setItem(r, 1, QTableWidgetItem(cat))
            self.report_table.setItem(r, 2, QTableWidgetItem(str(st)))
            self.report_table.setItem(r, 3, QTableWidgetItem(f"${pr * st:.2f}"))
        self.report_table.resizeRowsToContents()

# Ventana Principal
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FoodWizz - Sistema de Inventario")
        self.setMinimumSize(1366, 768)
        qt_rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qt_rect.moveCenter(center)
        self.move(qt_rect.topLeft())

        # Configuración del contenedor principal
        container = QWidget()
        self.setCentralWidget(container)
        self.main_layout = QHBoxLayout(container)
        container.setStyleSheet(f"background-color: {COLOR_LIGHT_BG};")

        # Configuración del menú lateral
        self.menu = QListWidget()
        self.menu.setStyleSheet(f"""
            background-color: {COLOR_DARK};
            color: {COLOR_LIGHT_BG};
            font-weight: bold;
            selection-background-color: {COLOR_PRIMARY};
            selection-color: {COLOR_DARK};
            font-size: 16px;
        """)
        sections = ["Órdenes", "Inventario", "Reportes", "Cuenta"]
        for section in sections:
            item = QListWidgetItem(section)
            self.menu.addItem(item)
        self.menu.setFixedWidth(180)

        # Configuración del layout apilado para cambiar vistas
        self.stack = QStackedLayout()
        self.orders_view = self.create_orders_view()
        self.inventory_view = self.create_inventory_view()
        self.reports_view = ReportsTab()
        self.account_view = self.create_account_view()

        self.stack.addWidget(self.orders_view)
        self.stack.addWidget(self.inventory_view)
        self.stack.addWidget(self.reports_view)
        self.stack.addWidget(self.account_view)

        # Conectar el menú con el layout apilado
        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

        self.main_layout.addWidget(self.menu)
        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        self.main_layout.addWidget(content_widget)

    # Método para crear la vista de órdenes
    def create_orders_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        widget.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        # Configuración de controles de búsqueda y filtro
        controls = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.setStyleSheet(f"""
            border: 2px solid {COLOR_SECONDARY};
            padding: 8px;
            border-radius: 8px;
            font-size: 14px;
            selection-background-color: {COLOR_PRIMARY};
        """)
        self.search_input.textChanged.connect(self.update_product_grid)

        self.category_filter = QComboBox()
        self.category_filter.addItems(["All", "Ramen", "Drink", "Other"])
        self.category_filter.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 8px;
            font-weight: bold;
            border-radius: 8px;
        """)
        self.category_filter.currentTextChanged.connect(self.update_product_grid)

        controls.addWidget(self.search_input)
        controls.addWidget(self.category_filter)
        layout.addLayout(controls)

        # Configuración del grid de productos
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setLayout(self.grid)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.update_product_grid()  # Actualizar grid de productos
        widget.setLayout(layout)
        return widget

    # Método para actualizar el grid de productos
    def update_product_grid(self):
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)

        search = self.search_input.text().lower()
        cat = self.category_filter.currentText()

        row = col = 0
        for name, price, img, category, stock in products:
            if (cat != "All" and category != cat) or (search and search not in name.lower()):
                continue
            card = ProductCard(name, price, img, stock)
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    # Método para crear la vista de inventario
    def create_inventory_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        widget.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        # Configuración de la barra de búsqueda
        self.inventory_search = QLineEdit()
        self.inventory_search.setPlaceholderText("Buscar en inventario...")
        self.inventory_search.setStyleSheet(f"""
            border: 2px solid {COLOR_SECONDARY};
            padding: 8px;
            border-radius: 8px;
            font-size: 14px;
        """)
        self.inventory_search.textChanged.connect(self.update_inventory_table)
        layout.addWidget(self.inventory_search)

        # Configuración de la tabla de inventario
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(5)
        self.inventory_table.setHorizontalHeaderLabels(["Imagen", "Producto", "Categoría", "Precio", "Stock"])
        self.inventory_table.verticalHeader().setVisible(False)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.inventory_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.inventory_table.setColumnWidth(0, 60)
        self.inventory_table.setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_LIGHT_BG};
                font-weight: bold;
                padding: 4px;
            }}
            QTableWidget {{
                background-color: {COLOR_LIGHT_BG};
                gridline-color: {COLOR_SECONDARY};
            }}
            QTableWidget QTableCornerButton::section {{
                background-color: {COLOR_PRIMARY};
            }}
        """)
        layout.addWidget(self.inventory_table)

        # Configuración de botones para agregar y eliminar productos
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Agregar Producto")
        btn_del = QPushButton("Eliminar Producto")
        btn_add.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
        """)
        btn_del.setStyleSheet(f"""
            background-color: {COLOR_WARNING};
            color: {COLOR_LIGHT_BG};
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: bold;
        """)
        btn_add.clicked.connect(self.add_product)
        btn_del.clicked.connect(self.remove_product)
        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_del)
        layout.addLayout(btn_layout)

        self.update_inventory_table()  # Actualizar tabla de inventario
        widget.setLayout(layout)
        return widget

    # Método para actualizar la tabla de inventario
    def update_inventory_table(self):
        search = self.inventory_search.text().lower()
        filtered = [p for p in products if search in p[0].lower()]

        self.inventory_table.setRowCount(len(filtered))
        for r, (n, pr, img, cat, st) in enumerate(filtered):
            lbl = QLabel()
            pm = QPixmap(img)
            if pm.isNull(): pm = QPixmap(DEFAULT_IMAGE_PATH)
            lbl.setPixmap(pm.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            lbl.setAlignment(Qt.AlignCenter)
            self.inventory_table.setCellWidget(r, 0, lbl)
            self.inventory_table.setItem(r, 1, QTableWidgetItem(n))
            self.inventory_table.setItem(r, 2, QTableWidgetItem(cat))
            self.inventory_table.setItem(r, 3, QTableWidgetItem(f"${pr:.2f}"))
            self.inventory_table.setItem(r, 4, QTableWidgetItem(str(st)))
        self.inventory_table.resizeRowsToContents()

    # Método para agregar un producto
    def add_product(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Agregar Producto")
        dialog.setFixedSize(400, 320)
        dialog.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK};")
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        fields = {}
        for key in ["Nombre", "Categoría", "Precio", "Stock"]:
            h = QHBoxLayout()
            lbl = QLabel(f"{key}:")
            lbl.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK};")
            h.addWidget(lbl)
            le = QLineEdit()
            le.setStyleSheet(f"border: 2px solid {COLOR_SECONDARY}; padding: 6px; border-radius: 6px;")
            h.addWidget(le)
            layout.addLayout(h)
            fields[key] = le

        self.selected_image_path = DEFAULT_IMAGE_PATH
        btn_img = QPushButton("Seleccionar Imagen")
        btn_img.setStyleSheet(f"""
            background-color: {COLOR_PRIMARY};
            color: {COLOR_DARK};
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_img.clicked.connect(lambda: self.select_image(dialog))
        layout.addWidget(btn_img)

        btn_create = QPushButton("Crear")
        btn_create.setStyleSheet(f"""
            background-color: {COLOR_ACCENT};
            color: {COLOR_LIGHT_BG};
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
        """)
        btn_create.clicked.connect(lambda: self.validate_and_create(fields, dialog))
        layout.addWidget(btn_create)

        dialog.exec_()

    # Método para seleccionar una imagen
    def select_image(self, dialog):
        file_path, _ = QFileDialog.getOpenFileName(dialog, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path

    # Método para validar y crear un producto
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
            self.update_product_grid()
            dialog.accept()
        except ValueError as e:
            QMessageBox.warning(dialog, "Entrada no válida", str(e))

    # Método para eliminar un producto
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
        self.update_product_grid()

    # Método para crear la vista de cuenta
    def create_account_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        widget.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK};")
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabBar::tab {{
                background: {COLOR_SECONDARY};
                color: {COLOR_LIGHT_BG};
                padding: 12px 20px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                margin-right: 8px;
                font-weight: 600;
                font-size: 14px;
            }}
            QTabBar::tab:selected {{
                background: {COLOR_PRIMARY};
                color: {COLOR_DARK};
            }}
            QTabWidget::pane {{
                border: 1px solid {COLOR_SECONDARY};
                top: -1px;
                background-color: {COLOR_LIGHT_BG};
                border-radius: 10px;
            }}
        """)
        self.personal_tab = PersonalInfoTab()
        self.payment_tab = PaymentSubscriptionsTab()

        self.tabs.addTab(self.personal_tab, "Información Personal")
        self.tabs.addTab(self.payment_tab, "Pagos y Suscripciones")

        layout.addWidget(self.tabs)
        return widget

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())