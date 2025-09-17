class WebScraping(object):
    '''
    Object of Web-scraping.

    This is only a demo.
    '''

    def __init__(self):
        self.__readable_web_pdf = None
        self.__dom_object_list = []

    def get_readable_web_pdf(self):
        ''' getter '''
        return self.__readable_web_pdf

    def set_readable_web_pdf(self, value):
        ''' setter '''
        self.__readable_web_pdf = value

    def scrape(self, url):
        '''
        Execute Web-Scraping.
        The target dom objects are in self.__dom_object_list.

        Args:
            url:    Web site url.

        Returns:
            The result. this is a string.

        @TODO(chimera0): check URLs format.
        '''
        import requests
        from bs4 import BeautifulSoup
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract text from DOM objects
            result = ""
            for dom_obj in self.__dom_object_list:
                elements = soup.select(dom_obj) if isinstance(dom_obj, str) else [soup.find(dom_obj)]
                for element in elements:
                    if element:
                        result += element.get_text() + "\n"
            
            return result.strip()
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"