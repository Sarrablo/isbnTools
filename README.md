
# IsbnTools 📚🔍

Herramienta en Python para consultar información de libros y portadas mediante ISBN o título de libro, utilizando Selenium y BeautifulSoup.

## 🚀 Características

- Búsqueda de libros por título.
- Búsqueda de libros por ISBN.
- Obtención de la portada del libro por ISBN.
- Navegación automática en páginas del Ministerio de Cultura y ISBNdb.
- User-Agent personalizado para evitar bloqueos.
- Método `close()` para cerrar correctamente el navegador.

## 🛠 Requisitos

- Python 3.7+
- Google Chrome
- ChromeDriver compatible con tu versión de Chrome

## 📦 Instalación

1. Clona este repositorio o descarga los archivos.
2. Instala las dependencias necesarias:

```bash
pip install selenium beautifulsoup4
```

3. Asegurate de tener `chromedriver` instalado y disponible en tu PATH. Puedes descargarlo desde: https://sites.google.com/chromium.org/driver/

## 🧠 Uso básico

```python
from isbn_tools import IsbnTools  # Suponiendo que guardaste la clase en isbn_tools.py

tools = IsbnTools()

# Buscar por título
resultado = tools.search_data_by_title("Cien años de soledad")
print(resultado)

# Buscar por ISBN
tools.search_data_by_isbn("9788497592208")

# Obtener portada
cover_url = tools.get_cover_by_isbn("9788497592208")
print(cover_url)

# Cerrar navegador
tools.close()
```

## 📁 Estructura del Proyecto

```
isbn_tools.py
README.md
```

## 📝 Licencia

Este proyecto se entrega sin licencia específica. Puedes usarlo, modificarlo y adaptarlo libremente.

---

¡Felices búsquedas bibliográficas! 📖✨
