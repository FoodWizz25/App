# FoodWizz 5.0 - Sistema de Gestión de Negocios de Alimentos

Una aplicación de escritorio moderna construida con PyQt5 para la gestión integral de negocios de alimentos.

## Características

- **Gestión de Productos**: Visualiza y gestiona tu menú de productos
- **Control de Inventario**: Añade, edita y elimina productos del inventario
- **Reportes y Análisis**: Visualiza gráficos de rendimiento del negocio
- **Configuración de Cuenta**: Personaliza la aplicación con temas claro y oscuro
- **Interfaz Moderna**: Diseño limpio con efectos de sombra y animaciones

## Instalación

1. Instala las dependencias:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Ejecuta la aplicación:
\`\`\`bash
python main.py
\`\`\`

## Uso

### Navegación
- **Órdenes**: Explora el menú de productos y gestiona órdenes
- **Inventario**: Administra el stock y información de productos
- **Reportes**: Visualiza gráficos de ventas y rendimiento
- **Cuenta**: Configura temas y preferencias

### Funcionalidades Principales

#### Gestión de Productos
- Visualización en tarjetas con imágenes
- Búsqueda por nombre
- Filtrado por categoría
- Detalles completos del producto

#### Control de Inventario
- Tabla completa de productos
- Añadir nuevos productos
- Editar productos existentes
- Eliminar productos
- Búsqueda en tiempo real

#### Reportes
- Gráfico de ganancias mensuales
- Distribución de ventas por categoría
- Visualización con Matplotlib

#### Temas
- Tema claro (predeterminado)
- Tema oscuro
- Cambio dinámico de temas

## Estructura del Proyecto

\`\`\`
foodwizz-app/
├── main.py              # Aplicación principal
├── productos.json       # Base de datos de productos
├── requirements.txt     # Dependencias
├── README.md           # Documentación
├── images/             # Imágenes de productos
└── icons/              # Iconos de la interfaz
\`\`\`

## Personalización

### Añadir Nuevos Temas
Modifica las constantes `THEME_LIGHT` y `THEME_DARK` en `main.py` para personalizar los colores.

### Añadir Nuevas Categorías
Actualiza la lista `categories` en el método `_show_product_dialog` de la clase `InventoryView`.

## Requisitos del Sistema

- Python 3.7+
- PyQt5 5.15+
- Matplotlib 3.7+
- Sistema operativo: Windows, macOS, Linux

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
