"""Tools for extract ISBN data"""
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import bs4


class IsbnTools:
    """Class for isbns"""

    def __init__(self):
        # Define a custom user agent
        my_user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
            " like Gecko) Chrome/92.0.4515.159 Safari/537.36")
        # Set up Chrome options
        chrome_options = Options()
        # Set the custom User-Agent
        chrome_options.add_argument(f"--user-agent={my_user_agent}")
        chrome_options.add_argument("--no-sandbox")
        # Create a new instance of ChromeDriver with the desired options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.TRADUCTIONS ={
 'Título:': 'title',
 'Autor/es:': 'author',
 'Lengua de publicación:': 'publish_language',
 'Lengua/s de traducción:': 'traduction_language',
 'Edición:': 'edition',
 'Fecha Edición:': 'edition_date',
 'Fecha Impresión:': 'printed_date',
 'Publicación:': 'publisher',
 'Descripción:': 'desc',
 'Encuadernación:': 'format',
 'Materia/s:': 'matter',
 'Precio:': 'price'}


    def advanced_search(self,
                        title=None,
                        author=None,
                        collection=None,
                        editorial=None,
                        materia=None):
        """Use the advanced search"""

        self.driver.get(
            "https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do?"
            "cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es"
        )
        self.driver.get("https://www.cultura.gob.es/webISBN/buscarLibros.do")

        for _ in range(3):
            self.driver.find_element(
                By.XPATH, '//*[@id="anadirFiltro"]/span/input').click()

        filters = {
            "5": title,
            "1": author,
            "2": collection,
            "3": editorial,
            "4": materia
        }

        tabindex = 109

        for select_value, input_text in filters.items():
            if input_text:
                Select(
                    self.driver.find_element(
                        By.XPATH,
                        f"//select[@tabindex='{tabindex}']")).select_by_value(
                            select_value)
                tabindex += 1
                self.driver.find_element(
                    By.XPATH,
                    f"//input[@tabindex='{tabindex}']").send_keys(input_text)
                tabindex += 2

        self.driver.find_element(By.XPATH, "//input[@tabindex='154']").click()

        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        results = soup.find_all("div", class_="isbnResultado")

        if not results:
            return {"error": "Not Found"}

        total_results = len(results)
        first_result = results[0]
        spans = first_result.find_all("span")
        links = first_result.find_all("a")

        author_text = spans[1].get_text(strip=True).replace("Autor/es:",
                                                            "").strip()

        return {
            "isbn": links[0].text,
            "title": links[1].text,
            "author": author_text,
            "editor": links[2].text,
            "url": links[1]["href"],
            "retrieved_docs": total_results
        }

    def search_data_by_title(self, book_title):
        """Search ISBN in cultura.gob by name"""
        self.driver.get((
            "https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do?"
            "cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es"
        ))
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

    def get_data(self, xpath):
        """Get XPATH data"""
        return self.driver.find_element(By.XPATH,
                                        xpath).get_attribute("innerHTML")

    def search_data_by_isbn(self, isbn):
        """Search data in cultura.gob by ISBN"""
        self.driver.get((
            "https://www.cultura.gob.es/webISBN/tituloSimpleFilter.do"
            "?cache=init&prev_layout=busquedaisbn&layout=busquedaisbn&language=es"
        ))
        _isbn = self.driver.find_element(By.ID, "params.cisbnExt")
        _isbn.send_keys(isbn)
        buton = self.driver.find_element(By.XPATH, "//input[@tabindex='109']")
        buton.click()
        time.sleep(0.2)
        soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        isbn_resultado = soup.find_all("div", {"class": "isbnResultado"})
        _author = (((isbn_resultado[0].find_all("span")[1]).text).replace(
            "\n", "").replace("\t", "").replace("Autor/es:", "")).strip()
        url = isbn_resultado[0].find("a")['href']
        url = f"https://www.cultura.gob.es{url}"
        self.driver.get(url)
        _isbn_13 = self.get_data(
            "/html/body/div[1]/div[1]/div[3]/div/div[2]/div[1]/span/strong")
        try:
            _isbn_10 = self.get_data(
                "/html/body/div[1]/div[1]/div[3]/div/div[2]/div[2]/span/strong")
        except NoSuchElementException:
            _isbn_10 = None
        
        cont_soup = bs4.BeautifulSoup(self.driver.page_source, "html.parser")
        res = cont_soup.find_all("tr")
        result=dict(isbn_13=_isbn_13,isbn_10=_isbn_10)
        for item in res:
            result[self.TRADUCTIONS.get(item.find("th").text)]= item.find("td").text.split(";")[0].strip()
        match = re.match(r'^(\d+)', result['desc'])
        _pages = match.group(1)
        result["pages"]=_pages 
        return result

    def get_cover_by_isbn(self, isbn):
        """Get the book cover from ISBN"""
        isbn = isbn.strip().replace("-", "")
        self.driver.get(f"https://isbndb.com/book/{isbn}")
        try:
            _image_container = self.driver.find_element(
                By.CLASS_NAME,
                ('artwork.text-center.col-12.col-sm-5.col-md-3.mb-8.md-sm-14.'
                 'd-inline-flex.justify-content-center.justify-content-sm-start'
                 ))
            return _image_container.find_element(
                By.XPATH, '//object').get_attribute("data")
        except NoSuchElementException:
            return "Not Found"

    def get_full_report(self, isbn):
        """Get full report from a ISBN"""
        _gob_info = self.search_data_by_isbn(isbn)
        _cover = dict(cover=self.get_cover_by_isbn(isbn))
        return _gob_info | _cover

    def close(self):
        """Close the driver when the api is closed"""
        self.driver.quit()
