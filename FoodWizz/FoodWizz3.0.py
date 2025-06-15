import sys
import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGridLayout, QScrollArea, QMainWindow,
    QListWidget, QListWidgetItem, QStackedLayout, QLineEdit,
    QComboBox, QDesktopWidget, QTableWidget, QTableWidgetItem,
    QMessageBox, QInputDialog, QFileDialog, QDialog, QTabWidget,
    QProgressBar, QSplashScreen, QTextEdit, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPainter, QColor, QMovie, QCursor
from PyQt5.QtCore import Qt, QTimer, QSize

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
# Widget de Tarjeta de Producto
# -------------------------------------------------

class ProductCard(QWidget):
    def __init__(self, name, price, image_path, stock):
        super().__init__()
        layout = QVBoxLayout(self)
        # Cargar imagen del producto o usar una por defecto
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)
        image = QLabel()
        image.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        # Configuración de etiquetas para nombre, precio y stock
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        price_label = QLabel(f"${price:.2f}")
        stock_label = QLabel(f"Stock: {stock}")
        # Botón de favoritos
        self.fav_button = QPushButton()
        self.fav_button.setIcon(QIcon("heart_empty.png"))
        self.fav_button.setCheckable(True)
        self.fav_button.setFixedSize(24, 24)
        self.fav_button.setStyleSheet("QPushButton { border: none; }")
        self.fav_button.toggled.connect(self.toggle_favorite)

        # Añadir widgets al layout
        layout.addWidget(image, alignment=Qt.AlignCenter)
        layout.addWidget(name_label, alignment=Qt.AlignCenter)
        layout.addWidget(price_label, alignment=Qt.AlignCenter)
        layout.addWidget(stock_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.fav_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setStyleSheet("""
            QWidget {
                background-color: #FEFAE0;
                border: 2px solid #DDAA00;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                font-family: 'Nunito';
                color: #173F4E;
            }
        """)

    def toggle_favorite(self, checked):
        # Cambia el ícono del botón de favoritos
        self.fav_button.setIcon(QIcon("heart_filled.png" if checked else "heart_empty.png"))

# -------------------------------------------------
# Widgets para la pestaña de Cuenta
# -------------------------------------------------

class PersonalInfoTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Título y subtítulo
        title = QLabel("Información Personal")
        title.setStyleSheet("font-size: 22px; font-weight: 900; color: #173F4E;")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        subtitle = QLabel("Información sobre ti y tus preferencias en los servicios")
        subtitle.setStyleSheet("font-size: 14px; color: #4B6E7F; margin-bottom: 20px;")
        layout.addWidget(subtitle)

        # Sección de foto de perfil
        pic_layout = QHBoxLayout()
        self.pic_label = QLabel()
        self.pic_label.setFixedSize(128, 128)
        self.pic_label.setStyleSheet("border-radius: 64px; border: 2px solid #DDAA00; background-color: #FEFAE0;")
        default_pix = QPixmap(DEFAULT_IMAGE_PATH)
        if default_pix.isNull():
            default_pix = QPixmap(128, 128)
            default_pix.fill(Qt.lightGray)
        self.pic_label.setPixmap(default_pix.scaled(128, 128, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.pic_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.pic_label.setToolTip("Haz clic para cambiar la foto de perfil")
        self.pic_label.mousePressEvent = self.change_profile_picture
        pic_layout.addWidget(self.pic_label, alignment=Qt.AlignLeft)

        pic_desc = QLabel(
            "Una foto de perfil te permite personalizar la cuenta.\n"
            "Haz clic en la imagen para cambiarla."
        )
        pic_desc.setWordWrap(True)
        pic_desc.setStyleSheet("color: #4B6E7F; font-size: 13px; padding-left: 15px;")
        pic_layout.addWidget(pic_desc, alignment=Qt.AlignLeft)
        layout.addLayout(pic_layout)

        # Sección de formulario: Nombre, Fecha de Nacimiento, Género, Correo Electrónico, Teléfono
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        label_style = "color: #173F4E; font-weight: bold; font-size: 14px;"

        form_layout.addWidget(QLabel("Nombre:"), 0, 0, alignment=Qt.AlignRight)
        self.name_edit = QLineEdit("Humano Morales")
        self.name_edit.setFixedWidth(250)
        form_layout.addWidget(self.name_edit, 0, 1)

        form_layout.addWidget(QLabel("Fecha de nacimiento:"), 1, 0, alignment=Qt.AlignRight)
        self.dob_edit = QLineEdit("")
        self.dob_edit.setFixedWidth(250)
        form_layout.addWidget(self.dob_edit, 1, 1)

        form_layout.addWidget(QLabel("Género:"), 2, 0, alignment=Qt.AlignRight)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Prefiero no decirlo", "Masculino", "Femenino", "Otro"])
        self.gender_combo.setCurrentIndex(0)
        self.gender_combo.setFixedWidth(250)
        form_layout.addWidget(self.gender_combo, 2, 1)

        form_layout.addWidget(QLabel("Correo electrónico:"), 3, 0, alignment=Qt.AlignRight)
        self.email_edit = QTextEdit()
        self.email_edit.setText("")
        self.email_edit.setFixedHeight(60)
        self.email_edit.setFixedWidth(250)
        form_layout.addWidget(self.email_edit, 3, 1)

        form_layout.addWidget(QLabel("Teléfono:"), 4, 0, alignment=Qt.AlignRight)
        self.phone_edit = QTextEdit()
        self.phone_edit.setText("")
        self.phone_edit.setFixedHeight(60)
        self.phone_edit.setFixedWidth(250)
        form_layout.addWidget(self.phone_edit, 4, 1)

        layout.addLayout(form_layout)

        # Sección de direcciones
        layout.addSpacing(15)
        addr_title = QLabel("Direcciones")
        addr_title.setStyleSheet("font-weight: 700; font-size: 18px; color: #173F4E;")
        layout.addWidget(addr_title, alignment=Qt.AlignLeft)
        addr_sub = QLabel(
            "Administra las direcciones asociadas con tu cuenta.\n"
            "Más información sobre las direcciones guardadas."
        )
        addr_sub.setStyleSheet("font-size: 13px; color: #4B6E7F; margin-bottom: 10px;")
        layout.addWidget(addr_sub)

        addr_grid = QGridLayout()
        addr_grid.setSpacing(10)
        addr_grid.addWidget(QLabel("Domicilio:"), 0, 0, alignment=Qt.AlignRight)
        self.home_addr = QLineEdit("Sin establecer")
        self.home_addr.setFixedWidth(300)
        addr_grid.addWidget(self.home_addr, 0, 1)

        addr_grid.addWidget(QLabel("Laboral:"), 1, 0, alignment=Qt.AlignRight)
        self.work_addr = QLineEdit("Sin establecer")
        self.work_addr.setFixedWidth(300)
        addr_grid.addWidget(self.work_addr, 1, 1)
        layout.addLayout(addr_grid)

        # Botón de guardar información
        self.save_btn = QPushButton("Guardar Información")
        self.save_btn.setFixedWidth(160)
        self.save_btn.setStyleSheet(
            "background-color: #DDAA00; color: #173F4E; font-weight: bold; padding: 6px 12px; border-radius: 6px;")
        self.save_btn.clicked.connect(self.save_info)
        layout.addSpacing(20)
        layout.addWidget(self.save_btn, alignment=Qt.AlignLeft)

    def change_profile_picture(self, event):
        # Abre un diálogo para seleccionar una nueva foto de perfil
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar foto de perfil", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            pix = QPixmap(file_path)
            if pix.isNull():
                QMessageBox.warning(self, "Error", "No se pudo cargar la imagen seleccionada.")
            else:
                self.pic_label.setPixmap(pix.scaled(128, 128, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
                self.current_profile_pic = file_path
        else:
            self.current_profile_pic = None

    def save_info(self):
        # Valida y guarda la información personal
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        QMessageBox.information(self, "Guardado", "Información personal guardada correctamente.")

class PaymentSubscriptionsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        title = QLabel("Pagos y Suscripciones")
        title.setStyleSheet("font-size: 22px; font-weight: 900; color: #173F4E; margin-bottom: 10px;")
        layout.addWidget(title, alignment=Qt.AlignLeft)

        info_label = QLabel(
            "Tu información de pagos, transacciones y suscripciones activas."
        )
        info_label.setStyleSheet("color: #4B6E7F; font-size: 14px; margin-bottom: 25px;")
        layout.addWidget(info_label)

        # Sección de Plan de Suscripción
        plan_group = QWidget()
        plan_layout = QVBoxLayout(plan_group)
        plan_label = QLabel("Plan de Suscripción Actual")
        plan_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #173F4E;")
        plan_layout.addWidget(plan_label)

        self.plan_name_label = QLabel("Pro Plan")
        self.plan_name_label.setStyleSheet(
            "font-size: 24px; font-weight: 900;"
            "color: #DDAA00; margin: 10px 0 15px 0;"
        )
        plan_layout.addWidget(self.plan_name_label)

        plan_desc = QLabel(
            "El Pro Plan te permite obtener todas las características premium de FoodWizz, "
            "con almacenamiento extendido y soporte prioritario."
        )
        plan_desc.setWordWrap(True)
        plan_desc.setStyleSheet("font-size: 14px; color: #4B6E7F;")
        plan_layout.addWidget(plan_desc)

        btn_upgrade = QPushButton("Actualizar Plan")
        btn_upgrade.setFixedWidth(160)
        btn_upgrade.setStyleSheet(
            "background-color: #DDAA00; color: #173F4E; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-top: 15px;"
        )
        btn_upgrade.clicked.connect(self.upgrade_plan_dialog)
        plan_layout.addWidget(btn_upgrade)

        layout.addWidget(plan_group)

        # Sección de Uso de Almacenamiento
        storage_group = QWidget()
        storage_layout = QVBoxLayout(storage_group)
        storage_label = QLabel("Almacenamiento de la cuenta")
        storage_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #173F4E; margin-top: 30px;")
        storage_layout.addWidget(storage_label)

        self.storage_bar = QProgressBar()
        self.storage_bar.setMinimum(0)
        self.storage_bar.setMaximum(1000000)
        self.storage_bar.setValue(707000)
        self.storage_bar.setFormat("%p% de 1 TB en uso")
        self.storage_bar.setTextVisible(True)
        self.storage_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #85AAAA;
                border-radius: 10px;
                text-align: center;
                color: #173F4E;
                font-weight: bold;
                font-size: 14px;
                background-color: #FEFAE0;
                height: 24px;
            }
            QProgressBar::chunk {
                background-color: #DDAA00;
                border-radius: 10px;
            }
        """)
        storage_layout.addWidget(self.storage_bar)
        btn_manage_storage = QPushButton("Administrar almacenamiento")
        btn_manage_storage.setFixedWidth(200)
        btn_manage_storage.setStyleSheet(
            "background-color: #85AAAA; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-top: 10px;"
        )
        btn_manage_storage.clicked.connect(self.manage_storage_clicked)
        storage_layout.addWidget(btn_manage_storage)

        layout.addWidget(storage_group)

        # Sección de Métodos de Pago
        payment_group = QWidget()
        payment_layout = QVBoxLayout(payment_group)
        payment_label = QLabel("Formas de pago")
        payment_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #173F4E; margin-top: 30px;")
        payment_layout.addWidget(payment_label)

        payment_desc = QLabel(
            "Las formas de pago se guardan para que puedas usarlas cómodamente."
        )
        payment_desc.setStyleSheet("font-size: 14px; color: #4B6E7F; margin-bottom: 10px;")
        payment_layout.addWidget(payment_desc)

        self.payment_methods_list = QVBoxLayout()
        card1 = self.create_payment_card("Tarjeta Visa", "**** **** **** 1234", "12/24")
        card2 = self.create_payment_card("Paypal", "", "Cuenta activa")
        self.payment_methods_list.addWidget(card1)
        self.payment_methods_list.addWidget(card2)
        payment_layout.addLayout(self.payment_methods_list)

        btn_manage_pm = QPushButton("Administrar formas de pago")
        btn_manage_pm.setFixedWidth(200)
        btn_manage_pm.setStyleSheet(
            "background-color: #DDAA00; color: #173F4E; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-top: 15px;"
        )
        btn_manage_pm.clicked.connect(self.manage_payments_clicked)
        payment_layout.addWidget(btn_manage_pm)

        layout.addWidget(payment_group)

        # Sección de Suscripciones
        subs_group = QWidget()
        subs_layout = QVBoxLayout(subs_group)
        subs_label = QLabel("Suscripciones")
        subs_label.setStyleSheet("font-size: 16px; font-weight: 700; color: #173F4E; margin-top: 30px;")
        subs_layout.addWidget(subs_label)

        subs_desc = QLabel(
            "Visualiza tus pagos recurrentes de servicios por suscripción."
        )
        subs_desc.setStyleSheet("font-size: 14px; color: #4B6E7F; margin-bottom: 15px;")
        subs_layout.addWidget(subs_desc)

        sub1 = QLabel("• Renovación: 12/10/2025")
        sub2 = QLabel("• Renovación: 01/01/2026")
        sub1.setStyleSheet("font-size: 14px; color: #173F4E;")
        sub2.setStyleSheet("font-size: 14px; color: #173F4E;")
        subs_layout.addWidget(sub1)
        subs_layout.addWidget(sub2)

        btn_manage_subs = QPushButton("Administrar suscripciones")
        btn_manage_subs.setFixedWidth(200)
        btn_manage_subs.setStyleSheet(
            "background-color: #85AAAA; color: white; font-weight: bold; padding: 6px 12px; border-radius: 6px; margin-top: 15px;"
        )
        btn_manage_subs.clicked.connect(self.manage_subscriptions_clicked)
        subs_layout.addWidget(btn_manage_subs)

        layout.addWidget(subs_group)
        layout.addStretch()

    def create_payment_card(self, method_type, details, extra):
        # Crea una tarjeta de método de pago
        card = QWidget()
        card.setStyleSheet(
            "background-color: #FEFAE0; border: 1px solid #DDAA00; border-radius: 8px; padding: 8px 12px; margin-bottom: 10px;"
        )
        h_layout = QHBoxLayout(card)
        icon = QLabel()
        icon.setFixedSize(32, 32)
        if "visa" in method_type.lower():
            icon.setPixmap(QPixmap("icons/payment_visa.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        elif "paypal" in method_type.lower():
            icon.setPixmap(QPixmap("icons/payment_paypal.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            icon.setPixmap(QPixmap("icons/payment_card.png").scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        h_layout.addWidget(icon)

        texts = QVBoxLayout()
        texts.addWidget(QLabel(f"<b>{method_type}</b>"))
        texts.addWidget(QLabel(details))
        texts.addWidget(QLabel(f"<i>{extra}</i>"))
        for i in range(texts.count()):
            item = texts.itemAt(i).widget()
            if item:
                item.setStyleSheet("color: #173F4E; font-size: 13px;")
        h_layout.addLayout(texts)
        h_layout.addStretch()
        return card

    def upgrade_plan_dialog(self):
        # Muestra un diálogo para actualizar el plan de suscripción
        plans = ["Basic Plan", "Pro Plan", "Wizz Plan (Premium)"]
        plan, ok = QInputDialog.getItem(
            self, "Actualizar Plan", "Selecciona un plan de suscripción:", plans, 1, False)
        if ok and plan:
            self.plan_name_label.setText(plan)
            QMessageBox.information(self, "Plan Actualizado", f"Has actualizado al {plan}.")

    def manage_storage_clicked(self):
        # Muestra un mensaje para administrar el almacenamiento
        QMessageBox.information(self, "Administrar almacenamiento", "Funcionalidad para administrar almacenamiento próximamente.")

    def manage_payments_clicked(self):
        # Muestra un mensaje para administrar los pagos
        QMessageBox.information(self, "Administrar pagos", "Funcionalidad para administrar formas de pago próximamente.")

    def manage_subscriptions_clicked(self):
        # Muestra un mensaje para administrar las suscripciones
        QMessageBox.information(self, "Administrar suscripciones", "Funcionalidad para administrar suscripciones próximamente.")

# -------------------------------------------------
# Vista de Reportes con gráficos
# -------------------------------------------------

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        title = QLabel("Reportes y Análisis de Ganancias")
        title.setStyleSheet("font-size: 22px; font-weight: 900; color: #173F4E;")
        layout.addWidget(title, alignment=Qt.AlignCenter)
        layout.addSpacing(15)

        # Datos simulados
        self.months = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio"]
        self.ganancias = [1200, 1800, 1500, 2100, 1900, 2300]
        self.categorias = ['Ramen', 'Drink', 'Other']
        self.ventas_categoria = [5500, 3200, 2100]

        # Crear gráficos
        self.fig = Figure(figsize=(10,6))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # Dibujar todos los gráficos
        self.draw_plots()

    def draw_plots(self):
        self.fig.clear()

        ax1 = self.fig.add_subplot(2, 2, 1)
        ax1.bar(self.months, self.ganancias, color='#DDAA00', edgecolor='#B38A00')
        ax1.set_title('Ganancias Mensuales')
        ax1.set_ylabel('Ganancias ($)')
        ax1.tick_params(axis='x', rotation=30)

        ax2 = self.fig.add_subplot(2, 2, 2)
        ax2.plot(self.months, self.ganancias, marker='o', linestyle='-', color='#173F4E')
        ax2.set_title('Evolución de Ganancias')
        ax2.set_ylabel('Ganancias ($)')
        ax2.tick_params(axis='x', rotation=30)

        ax3 = self.fig.add_subplot(2, 1, 2)
        ax3.pie(self.ventas_categoria,
                labels=self.categorias,
                autopct='%1.1f%%',
                colors=['#DDAA00', '#85AAAA', '#173F4E'],
                startangle=140,
                wedgeprops=dict(edgecolor='w'))
        ax3.set_title('Ventas por Categoría')

        self.fig.tight_layout()
        self.canvas.draw()

# -------------------------------------------------
# Ventana Principal
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

        # Menú lateral
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
        self.menu.setStyleSheet("""
            QListWidget {
                background-color: #85AAAA;
                color: white;
                font-size: 16px;
                padding: 10px;
                border: none;
            }
            QListWidget::item { padding: 10px; height: 40px; }
            QListWidget::item:selected {
                background-color: #DDAA00;
                color: #173F4E;
                font-weight: bold;
            }
        """)

        # Layout apilado para las diferentes vistas
        self.stack = QStackedLayout()
        self.orders_view = self.create_orders_view()
        self.inventory_view = self.create_inventory_view()
        self.reports_view = ReportsView()
        self.account_view = self.create_account_view()

        self.stack.addWidget(self.orders_view)
        self.stack.addWidget(self.inventory_view)
        self.stack.addWidget(self.reports_view)
        self.stack.addWidget(self.account_view)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.main_layout.addWidget(self.menu)
        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        self.main_layout.addWidget(content_widget)

    def create_orders_view(self):
        # Crea la vista de órdenes
        widget = QWidget()
        layout = QVBoxLayout(widget)

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
        widget.setLayout(layout)
        return widget

    def update_product_grid(self):
        # Actualiza la cuadrícula de productos según la búsqueda y el filtro
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

    def create_inventory_view(self):
        # Crea la vista de inventario
        widget = QWidget()
        layout = QVBoxLayout(widget)

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
        widget.setLayout(layout)
        return widget

    def update_inventory_table(self):
        # Actualiza la tabla de inventario según la búsqueda
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
        # Muestra un diálogo para agregar un nuevo producto
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
        # Abre un diálogo para seleccionar una imagen para el producto
        file_path, _ = QFileDialog.getOpenFileName(dialog, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg)")
        if file_path:
            self.selected_image_path = file_path

    def validate_and_create(self, fields, dialog):
        # Valida y crea un nuevo producto
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

    def remove_product(self):
        # Elimina el producto seleccionado
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

    def create_account_view(self):
        # Crea la vista de cuenta
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabBar::tab {
                background: #FEFAE0;
                color: #173F4E;
                padding: 10px 25px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: 700;
                font-size: 15px;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: #DDAA00;
                color: #173F4E;
            }
            QTabWidget::pane {
                border: 2px solid #DDAA00;
                border-radius: 10px;
                padding: 10px;
                background-color: #FEFAE0;
            }
        """)
        self.personal_tab = PersonalInfoTab()
        self.payment_tab = PaymentSubscriptionsTab()

        self.tabs.addTab(self.personal_tab, "Información Personal")
        self.tabs.addTab(self.payment_tab, "Pagos y Suscripciones")

        layout.addWidget(self.tabs)
        return widget

# -------------------------------------------------
# Pantalla de Carga
# -------------------------------------------------

class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.9)
        self.setEnabled(False)
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress_up)
        self.timer.start(50)

    def progress_up(self):
        # Actualiza el progreso de la pantalla de carga
        self.progress += 2
        if self.progress > 100:
            self.timer.stop()
            self.close()
        else:
            self.showMessage(f"Cargando... {self.progress}%", Qt.AlignBottom | Qt.AlignCenter, Qt.white)

# -------------------------------------------------
# Estilo General y Ejecución
# -------------------------------------------------

style_sheet = """
/* Estilo general de la ventana principal */
QMainWindow {
    background-color: #FEFAE0;
}

/* Estilo del menú lateral */
QListWidget {
    background-color: #85AAAA;
    color: white;
    font-size: 16px;
    padding: 10px;
    border: none;
}

QListWidget::item {
    padding: 10px;
    height: 40px;
}

QListWidget::item:selected {
    background-color: #DDAA00;
    color: #173F4E;
    font-weight: bold;
}

/* Estilo para los campos de entrada y combobox */
QLineEdit, QComboBox, QTextEdit {
    border: 2px solid #85AAAA;
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
    background-color: #FEFAE0;
    color: #173F4E;
}

/* Estilo para los botones */
QPushButton {
    background-color: #DDAA00;
    border: none;
    padding: 6px 12px;
    border-radius: 5px;
    font-weight: bold;
    color: #173F4E;
    min-height: 32px;
}

QPushButton:hover {
    background-color: #C79700;
}

QPushButton:pressed {
    background-color: #B38A00;
}

/* Estilo para las etiquetas */
QLabel {
    font-family: 'Nunito';
    color: #173F4E;
}

/* Estilo para las pestañas */
QTabWidget::pane {
    border: 2px solid #DDAA00;
    border-radius: 10px;
    padding: 10px;
    background-color: #FEFAE0;
}

QTabBar::tab {
    background: #FEFAE0;
    color: #173F4E;
    padding: 10px 25px;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    font-weight: 700;
    font-size: 15px;
    min-width: 150px;
}

QTabBar::tab:selected {
    background: #DDAA00;
    color: #173F4E;
}

/* Estilo para la tabla de inventario */
QTableWidget {
    background-color: #FEFAE0;
    color: #173F4E;
    gridline-color: #DDAA00;
    selection-background-color: #DDAA00;
    selection-color: #173F4E;
}

QHeaderView::section {
    background-color: #DDAA00;
    color: #173F4E;
    padding: 4px;
    border: 1px solid #85AAAA;
}

/* Estilo para el scroll area */
QScrollArea {
    background-color: #FEFAE0;
    border: none;
}

/* Estilo para los diálogos */
QDialog {
    background-color: #FEFAE0;
}

/* Estilo para la barra de progreso */
QProgressBar {
    border: 2px solid #85AAAA;
    border-radius: 10px;
    text-align: center;
    color: #173F4E;
    font-weight: bold;
    font-size: 14px;
    background-color: #FEFAE0;
    height: 24px;
}

QProgressBar::chunk {
    background-color: #DDAA00;
    border-radius: 10px;
}

/* Estilo para el ProductCard */
QWidget#ProductCard {
    background-color: #FEFAE0;
    border: 2px solid #DDAA00;
    border-radius: 10px;
    padding: 10px;
}

/* Estilo para el botón de favoritos */
QPushButton#fav_button {
    background-color: transparent;
    border: none;
}

/* Estilo para el área de texto */
QTextEdit {
    border: 2px solid #85AAAA;
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
    background-color: #FEFAE0;
    color: #173F4E;
}
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)

    # Muestra la pantalla de carga
    splash_pix = QPixmap("pantalla_de_carga.png")
    splash = SplashScreen(splash_pix)
    splash.show()

    # Simula la carga
    app.processEvents()
    window = MainWindow()
    window.show()
    splash.finish(window)
    sys.exit(app.exec_())
