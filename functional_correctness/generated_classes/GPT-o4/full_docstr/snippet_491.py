class WebScraping(object):
    '''
    Object of Web-scraping.

    This is only a demo.
    '''
    def __init__(self, dom_object_list=None):
        self.__dom_object_list = dom_object_list or ['title', 'h1', 'h2', 'h3', 'p']
        self.__readable_web_pdf = False

    def get_readable_web_pdf(self):
        ''' getter '''
        return self.__readable_web_pdf

    def set_readable_web_pdf(self, value):
        ''' setter '''
        self.__readable_web_pdf = bool(value)

    def scrape(self, url):
        '''
        Execute Web-Scraping.
        The target dom objects are in self.__dom_object_list.

        Args:
            url:    Web site url.

        Returns:
            The result. this is a string.
        '''
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL format: {url}")
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts = []
        for tag in self.__dom_object_list:
            for elem in soup.find_all(tag):
                txt = elem.get_text(strip=True)
                if txt:
                    texts.append(txt)
        return '\n'.join(texts)