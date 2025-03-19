"""Tools for extract ISBN data"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import bs4


class IsbnTools:
    """Class for isbns"""

    def __init__(self):
        # Define a custom user agent
        my_user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
                " like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        # Set up Chrome options
        chrome_options = Options()
        # Set the custom User-Agent
        chrome_options.add_argument(f"--user-agent={my_user_agent}")
        chrome_options.add_argument("--no-sandbox")
        # Create a new instance of ChromeDriver with the desired options
        self.driver = webdriver.Chrome(options=chrome_options)

    def search_data_by_title(self, book_title):
        """Search ISBN in cultura.gob by name"""
        self.driver.get(
            ("https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do?"
                "cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es")
        )
        title = self.driver.find_element(By.ID,
                                         'params.liConceptosExt[0].texto')
        title.send_keys(book_title)
        buton = self.driver.find_element(By.XPATH, "//input[@tabindex='109']")
        buton.click()
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        isbn_resultado = soup.find_all("div", {"class": "isbnResultado"})
        if len(isbn_resultado) == 0:
            return dict(error="Not Found")
        total_len = len(isbn_resultado)
        isbn_resultado = isbn_resultado[0]
        author = (((isbn_resultado.find_all("span")[1]).text).replace(
            "\n", "").replace("\t", "").replace("Autor/es:", "")).strip()
        res = dict(isbn=isbn_resultado.find_all("a")[0].text,
                   title=isbn_resultado.find_all("a")[1].text,
                   author=author,
                   editor=isbn_resultado.find_all("a")[2].text,
                   url=isbn_resultado.find_all("a")[1]['href'],
                   retrieved_docs=total_len)
        return res

    def search_data_by_isbn(self, isbn):
        """Search data in cultura.gob by ISBN"""
        self.driver.get(
            ("https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do"
                "?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es")
        )
        _isbn = self.driver.find_element(By.ID, "params.cisbnExt")
        _isbn.send_keys(isbn)
        buton = self.driver.find_element(By.XPATH, "//input[@tabindex='109']")
        buton.click()
        time.sleep(0.2)
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        isbn_resultado = soup.find_all("div", {"class": "isbnResultado"})
        url = isbn_resultado[0].find("a")['href']
        url = f"https://www.cultura.gob.es{url}"
        self.driver.get(url)

    def get_cover_by_isbn(self, isbn):
        """Get the book cover from ISBN"""
        isbn = isbn.strip().replace("-", "")
        self.driver.get(f"https://isbndb.com/book/{isbn}")
        try:
            _image_container = self.driver.find_element(
                By.CLASS_NAME,
                ('artwork.text-center.col-12.col-sm-5.col-md-3.mb-8.md-sm-14.'
                    'd-inline-flex.justify-content-center.justify-content-sm-start')
            )
            return _image_container.find_element(
                By.XPATH, '//object').get_attribute("data")
        except NoSuchElementException:
            return "Not Found"

    def close(self):
        """Close the driver when the api is closed"""
        self.driver.quit()
