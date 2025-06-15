import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QStackedLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget,
    QTableWidgetItem, QMessageBox, QFileDialog, QScrollArea, QDesktopWidget,
    QListWidgetItem, QGridLayout, QDialog, QTabWidget, QInputDialog
)
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis, QPieSlice
import random

# Constantes para rutas de imágenes y archivo de datos
DEFAULT_IMAGE_PATH = "img/default.png"
DATA_FILE = "productos.json"

# Colores para la aplicación
COLOR_PRIMARY = "#DDAA00"
COLOR_SECONDARY = "#85AAAA"
COLOR_DARK = "#173F4E"
COLOR_LIGHT_BG = "#FEFAE0"
COLOR_ACCENT = "#606C38"
COLOR_WARNING = "#FF7F0D"

class Product:
    def __init__(self, name, price, image_path, category, stock):
        self.name = name
        self.price = price
        self.image_path = image_path
        self.category = category
        self.stock = stock

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "image_path": self.image_path,
            "category": self.category,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["name"],
            data["price"],
            data["image_path"],
            data["category"],
            data["stock"]
        )

class Database:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_products(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [Product.from_dict(p) for p in data]
            except Exception as e:
                print(f"No se pudo cargar {self.file_path}. Error: {e}")
        return [
            Product("Beef Ramen", 23.00, "img/beef_ramen.jpg", "Ramen", 12),
            Product("Chicken Teriyaki", 18.50, "img/chicken_teriyaki.jpg", "Ramen", 8),
            Product("Sushi Roll", 12.00, "img/sushi_roll.jpg", "Other", 20),
            Product("Tofu Salad", 15.75, "img/tofu_salad.jpg", "Other", 5),
            Product("Tempura Udon", 20.00, "img/tempura_udon.jpg", "Ramen", 6),
            Product("Matcha Ice Cream", 7.50, "img/matcha_ice_cream.jpg", "Drink", 13),
            Product("Miso Soup", 6.00, "img/miso_soup.jpg", "Ramen", 25),
            Product("Green Tea", 4.50, "img/green_tea.jpg", "Drink", 9),
            Product("Spicy Ramen", 22.00, "img/spicy_ramen.jpg", "Ramen", 14),
            Product("Salmon Sashimi", 19.00, "img/salmon_sashimi.jpg", "Other", 7),
            Product("Vegetable Gyoza", 10.00, "img/vegetable_gyoza.jpg", "Other", 10),
            Product("Iced Coffee", 5.00, "img/iced_coffee.jpg", "Drink", 11),
            Product("Fruit Mochi", 6.50, "img/fruit_mochi.jpg", "Other", 15),
            Product("Pork Ramen", 24.00, "img/pork_ramen.jpg", "Ramen", 4),
            Product("Bubble Tea", 6.00, "img/bubble_tea.jpeg", "Drink", 18),
            Product("Shrimp Tempura", 17.50, "img/shrimp_tempura.jpg", "Other", 6),
            Product("Yakisoba", 16.00, "img/yakisoba.jpg", "Ramen", 3),
            Product("Coconut Water", 4.75, "img/coconut_water.jpg", "Drink", 20),
            Product("Seaweed Salad", 9.00, "img/seaweed_salad.jpg", "Other", 2),
            Product("Oolong Tea", 4.00, "img/oolong_tea.jpg", "Drink", 22)
        ]

    def save_products(self, products):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in products], f, ensure_ascii=False, indent=2)

class ProductCard(QWidget):
    def __init__(self, product):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        self.setStyleSheet(f"""
            background-color: {COLOR_LIGHT_BG};
            border: 2px solid {COLOR_PRIMARY};
            border-radius: 10px;
        """)
        pixmap = QPixmap(product.image_path)
        if pixmap.isNull():
            pixmap = QPixmap(DEFAULT_IMAGE_PATH)
        image = QLabel()
        image.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        name_label = QLabel(product.name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK}; font-size: 16px;")
        price_label = QLabel(f"${product.price:.2f}")
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet(f"color: {COLOR_ACCENT}; font-weight: 600;")
        stock_label = QLabel(f"Stock: {product.stock}")
        stock_label.setAlignment(Qt.AlignCenter)
        stock_label.setStyleSheet(f"color: {COLOR_WARNING}; font-style: italic;")

        layout.addWidget(image)
        layout.addWidget(name_label)
        layout.addWidget(price_label)
        layout.addWidget(stock_label)

class InventoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database(DATA_FILE)
        self.products = self.db.load_products()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.setStyleSheet(f"""
            border: 2px solid {COLOR_SECONDARY};
            padding: 8px;
            border-radius: 8px;
            font-size: 14px;
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

        controls = QHBoxLayout()
        controls.addWidget(self.search_input)
        controls.addWidget(self.category_filter)
        layout.addLayout(controls)

        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content.setLayout(self.grid)
        scroll.setWidget(content)
        layout.addWidget(scroll)

        self.update_product_grid()

    def update_product_grid(self):
        search = self.search_input.text().lower()
        category = self.category_filter.currentText()

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        row, col = 0, 0
        for product in self.products:
            if (category != "All" and product.category != category) or (search and search not in product.name.lower()):
                continue
            card = ProductCard(product)
            self.grid.addWidget(card, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

class OrdersView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database(DATA_FILE)
        self.products = self.db.load_products()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        title = QLabel("Órdenes")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_PRIMARY}; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(4)
        self.orders_table.setHorizontalHeaderLabels(["ID", "Producto", "Cantidad", "Total"])
        self.orders_table.setStyleSheet(f"""
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
        """)
        layout.addWidget(self.orders_table)

        self.update_orders_table()

    def update_orders_table(self):
        self.orders_table.setRowCount(len(self.products))
        for r, product in enumerate(self.products):
            self.orders_table.setItem(r, 0, QTableWidgetItem(str(r+1)))
            self.orders_table.setItem(r, 1, QTableWidgetItem(product.name))
            self.orders_table.setItem(r, 2, QTableWidgetItem(str(random.randint(1, 10))))
            self.orders_table.setItem(r, 3, QTableWidgetItem(f"${product.price * random.randint(1, 10):.2f}"))
        self.orders_table.resizeRowsToContents()

class ReportsView(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database(DATA_FILE)
        self.products = self.db.load_products()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        title = QLabel("Reportes")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_PRIMARY}; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(4)
        self.reports_table.setHorizontalHeaderLabels(["Producto", "Categoría", "Ventas", "Ingresos"])
        self.reports_table.setStyleSheet(f"""
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
        """)
        layout.addWidget(self.reports_table)

        self.update_report_table()

        # Add charts
        self.add_charts(layout)

    def update_report_table(self):
        self.reports_table.setRowCount(len(self.products))
        for r, product in enumerate(self.products):
            sales = random.randint(1, 100)
            self.reports_table.setItem(r, 0, QTableWidgetItem(product.name))
            self.reports_table.setItem(r, 1, QTableWidgetItem(product.category))
            self.reports_table.setItem(r, 2, QTableWidgetItem(str(sales)))
            self.reports_table.setItem(r, 3, QTableWidgetItem(f"${product.price * sales:.2f}"))
        self.reports_table.resizeRowsToContents()

    def add_charts(self, layout):
        # Create a pie chart for product categories
        pie_series = QPieSeries()
        categories = {}
        for product in self.products:
            if product.category in categories:
                categories[product.category] += 1
            else:
                categories[product.category] = 1

        for category, count in categories.items():
            slice = pie_series.append(category, count)
            slice.setLabelVisible(True)

        pie_chart = QChart()
        pie_chart.addSeries(pie_series)
        pie_chart.setTitle("Distribución de Productos por Categoría")
        pie_chart.setAnimationOptions(QChart.AllAnimations)
        pie_chart.legend().hide()

        pie_chart_view = QChartView(pie_chart)
        pie_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(pie_chart_view)

        # Create a bar chart for sales
        bar_series = QBarSeries()
        bar_set = QBarSet("Ventas")
        for product in self.products:
            bar_set.append(product.stock)

        bar_series.append(bar_set)

        bar_chart = QChart()
        bar_chart.addSeries(bar_series)
        bar_chart.setTitle("Ventas por Producto")
        bar_chart.setAnimationOptions(QChart.AllAnimations)

        categories = [product.name for product in self.products]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        bar_chart.addAxis(axis_x, Qt.AlignBottom)
        bar_series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max(product.stock for product in self.products))
        bar_chart.addAxis(axis_y, Qt.AlignLeft)
        bar_series.attachAxis(axis_y)

        bar_chart.legend().setVisible(True)
        bar_chart.legend().setAlignment(Qt.AlignBottom)

        bar_chart_view = QChartView(bar_chart)
        bar_chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(bar_chart_view)

class AccountView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet(f"background-color: {COLOR_LIGHT_BG}; color: {COLOR_DARK}; font-size: 14px;")

        title = QLabel("Cuenta")
        title.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {COLOR_PRIMARY}; margin-bottom: 20px;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

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

        personal_info_tab = QWidget()
        payment_tab = QWidget()

        self.setup_personal_info_tab(personal_info_tab)
        self.setup_payment_tab(payment_tab)

        self.tabs.addTab(personal_info_tab, "Información Personal")
        self.tabs.addTab(payment_tab, "Pagos y Suscripciones")

        layout.addWidget(self.tabs)

    def setup_personal_info_tab(self, tab):
        layout = QVBoxLayout(tab)

        self.pic_label = QLabel()
        self.pic_label.setFixedSize(128, 128)
        default_pix = QPixmap(DEFAULT_IMAGE_PATH)
        if default_pix.isNull():
            default_pix = QPixmap(128, 128)
            default_pix.fill(Qt.lightGray)
        self.pic_label.setPixmap(default_pix.scaled(128, 128, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        layout.addWidget(self.pic_label, alignment=Qt.AlignLeft)

        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Nombre:"), 0, 0, alignment=Qt.AlignRight)
        self.name_edit = QLineEdit("Humano Morales")
        form_layout.addWidget(self.name_edit, 0, 1)

        form_layout.addWidget(QLabel("Fecha de nacimiento:"), 1, 0, alignment=Qt.AlignRight)
        self.dob_edit = QLineEdit("")
        form_layout.addWidget(self.dob_edit, 1, 1)

        form_layout.addWidget(QLabel("Género:"), 2, 0, alignment=Qt.AlignRight)
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Prefiero no decirlo", "Masculino", "Femenino", "Otro"])
        form_layout.addWidget(self.gender_combo, 2, 1)

        form_layout.addWidget(QLabel("Correo electrónico:"), 3, 0, alignment=Qt.AlignRight)
        self.email_edit = QLineEdit("")
        form_layout.addWidget(self.email_edit, 3, 1)

        form_layout.addWidget(QLabel("Teléfono:"), 4, 0, alignment=Qt.AlignRight)
        self.phone_edit = QLineEdit("")
        form_layout.addWidget(self.phone_edit, 4, 1)

        layout.addLayout(form_layout)

        self.save_btn = QPushButton("Guardar Información")
        self.save_btn.clicked.connect(self.save_info)
        layout.addWidget(self.save_btn, alignment=Qt.AlignLeft)

    def setup_payment_tab(self, tab):
        layout = QVBoxLayout(tab)

        plan_group = QWidget()
        plan_layout = QVBoxLayout(plan_group)
        plan_label = QLabel("Plan de Suscripción Actual")
        plan_layout.addWidget(plan_label)

        self.plan_name_label = QLabel("Pro Plan")
        plan_layout.addWidget(self.plan_name_label)

        plan_desc = QLabel("El Pro Plan te permite obtener todas las características premium de FoodWizz.")
        plan_layout.addWidget(plan_desc)

        btn_upgrade = QPushButton("Actualizar Plan")
        btn_upgrade.clicked.connect(self.upgrade_plan_dialog)
        plan_layout.addWidget(btn_upgrade)

        layout.addWidget(plan_group)

        storage_group = QWidget()
        storage_layout = QVBoxLayout(storage_group)
        storage_label = QLabel("Almacenamiento de la cuenta")
        storage_layout.addWidget(storage_label)

        self.storage_bar = QLabel("70% de 1 TB en uso")
        storage_layout.addWidget(self.storage_bar)

        btn_manage_storage = QPushButton("Administrar almacenamiento")
        btn_manage_storage.clicked.connect(self.manage_storage_clicked)
        storage_layout.addWidget(btn_manage_storage)

        layout.addWidget(storage_group)

        payment_group = QWidget()
        payment_layout = QVBoxLayout(payment_group)
        payment_label = QLabel("Formas de pago")
        payment_layout.addWidget(payment_label)

        payment_desc = QLabel("Las formas de pago se guardan para que puedas usarlas cómodamente.")
        payment_layout.addWidget(payment_desc)

        self.payment_methods_list = QVBoxLayout()
        card1 = self.create_payment_card("Tarjeta Visa", "**** **** **** 1234", "12/24")
        card2 = self.create_payment_card("Paypal", "feomorales@gmail.com", "Cuenta activa")
        self.payment_methods_list.addWidget(card1)
        self.payment_methods_list.addWidget(card2)
        payment_layout.addLayout(self.payment_methods_list)

        btn_manage_pm = QPushButton("Administrar formas de pago")
        btn_manage_pm.clicked.connect(self.manage_payments_clicked)
        payment_layout.addWidget(btn_manage_pm)

        layout.addWidget(payment_group)

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

    def save_info(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Validación", "El nombre no puede estar vacío.")
            return
        QMessageBox.information(self, "Guardado", "Información personal guardada correctamente.")

    def upgrade_plan_dialog(self):
        plans = ["Basic Plan (Gratis)", "Pro Plan", "Wizz Plan (Premium)"]
        plan, ok = QInputDialog.getItem(self, "Actualizar Plan", "Selecciona un plan de suscripción:", plans, 1, False)
        if ok and plan:
            self.plan_name_label.setText(plan)
            QMessageBox.information(self, "Plan Actualizado", f"Has actualizado al {plan}.")

    def manage_storage_clicked(self):
        QMessageBox.information(self, "Administrar almacenamiento", "Funcionalidad para administrar almacenamiento próximamente.")

    def manage_payments_clicked(self):
        QMessageBox.information(self, "Administrar pagos", "Funcionalidad para administrar formas de pago próximamente.")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FoodWizz - Sistema de Inventario")
        self.setMinimumSize(1366, 768)
        qt_rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        qt_rect.moveCenter(center)
        self.move(qt_rect.topLeft())

        container = QWidget()
        self.setCentralWidget(container)
        self.main_layout = QHBoxLayout(container)
        container.setStyleSheet(f"background-color: {COLOR_LIGHT_BG};")

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
            self.menu.addItem(section)
        self.menu.setFixedWidth(180)

        self.stack = QStackedLayout()
        self.orders_view = OrdersView()
        self.inventory_view = InventoryView()
        self.reports_view = ReportsView()
        self.account_view = AccountView()

        self.stack.addWidget(self.orders_view)
        self.stack.addWidget(self.inventory_view)
        self.stack.addWidget(self.reports_view)
        self.stack.addWidget(self.account_view)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

        self.main_layout.addWidget(self.menu)
        content_widget = QWidget()
        content_widget.setLayout(self.stack)
        self.main_layout.addWidget(content_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
