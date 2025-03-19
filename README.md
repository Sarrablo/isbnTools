
# IsbnTools 📚🔍

A Python tool to search for book information and covers using ISBN or book title, powered by Selenium and BeautifulSoup.

## 🚀 Features

- Search for books by title.
- Search for books by ISBN.
- Retrieve book cover image by ISBN.
- Automatic web navigation through the Spanish Ministry of Culture and ISBNdb.
- Custom User-Agent to avoid blocking.
- `close()` method to properly shut down the browser.

## 🛠 Requirements

- Python 3.7+
- Google Chrome
- ChromeDriver compatible with your Chrome version

## 📦 Installation

1. Clone this repository or download the files.
2. Install required dependencies:

```bash
pip install selenium beautifulsoup4
```

3. Make sure `chromedriver` is installed and available in your system PATH.  
   You can download it from: https://sites.google.com/chromium.org/driver/

## 🧠 Basic Usage

```python
from isbn_tools import IsbnTools  # Assuming the class is saved in isbn_tools.py

tools = IsbnTools()

# Search by title
result = tools.search_data_by_title("One Hundred Years of Solitude")
print(result)

# Search by ISBN
tools.search_data_by_isbn("9788497592208")

# Get book cover
cover_url = tools.get_cover_by_isbn("9788497592208")
print(cover_url)

# Close browser
tools.close()
```

## 📁 Project Structure

```
isbn_tools.py
README.md
```

## 📝 License

License GPL.

---

