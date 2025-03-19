import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import bs4

class IsbnTools:
    def __init__(self):
        # Define a custom user agent
        my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        # Set up Chrome options
        chrome_options = Options()
        # Set the custom User-Agent
        chrome_options.add_argument(f"--user-agent={my_user_agent}")
        chrome_options.add_argument("--no-sandbox")
        # Create a new instance of ChromeDriver with the desired options
        self.driver = webdriver.Chrome(options=chrome_options)

    def search_data_by_title(self, book_title):
        self.driver.get(
            "https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es"
        )
        title = self.driver.find_element(By.ID, 'params.liConceptosExt[0].texto')
        title.send_keys(book_title)
        buton = self.driver.find_element(By.XPATH, "//input[@tabindex='109']")
        buton.click()
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        isbnResultado = soup.find_all("div", {"class": "isbnResultado"})
        if len(isbnResultado) == 0:
            return dict(error="Not Found")
        total_len = len(isbnResultado)
        isbnResultado = isbnResultado[0]
        author = (((isbnResultado.find_all("span")[1]).text).replace("\n", "").replace("\t", "").replace("Autor/es:", "")).strip()
        res = dict(
            isbn=isbnResultado.find_all("a")[0].text,
            title=isbnResultado.find_all("a")[1].text,
            author=author,
            editor=isbnResultado.find_all("a")[2].text,
            url=isbnResultado.find_all("a")[1]['href'],
            retrieved_docs=total_len
        )
        return res

    def search_data_by_isbn(self, isbn):
        self.driver.get(
            "https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es"
        )
        _isbn = self.driver.find_element(By.ID, "params.cisbnExt")
        _isbn.send_keys(isbn)
        buton = self.driver.find_element(By.XPATH, "//input[@tabindex='109']")
        buton.click()
        time.sleep(0.2)
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        isbnResultado = soup.find_all("div", {"class": "isbnResultado"})
        url = isbnResultado[0].find("a")['href']
        url = f"https://www.cultura.gob.es{url}"
        self.driver.get(url)

    def get_cover_by_isbn(self, isbn):
        isbn = isbn.strip().replace("-", "")
        self.driver.get(f"https://isbndb.com/book/{isbn}")
        try:
            _image_container = self.driver.find_element(
                By.CLASS_NAME,
                'artwork.text-center.col-12.col-sm-5.col-md-3.mb-8.md-sm-14.d-inline-flex.justify-content-center.justify-content-sm-start'
            )
            return _image_container.find_element(By.XPATH, '//object').get_attribute("data")
        except:
            return "Not Found"

    def close(self):
        self.driver.quit()



