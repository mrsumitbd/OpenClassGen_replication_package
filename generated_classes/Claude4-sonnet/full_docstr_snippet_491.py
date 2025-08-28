class WebScraping(object):
    '''
    Object of Web-scraping.

    This is only a demo.
    '''
    
    def __init__(self):
        self.__readable_web_pdf = None
        self.__dom_object_list = ['p', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']

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
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            if url.lower().endswith('.pdf'):
                pdf_reader = PyPDF2.PdfReader(BytesIO(response.content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                self.set_readable_web_pdf(text)
                return text
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                scraped_text = ""
                
                for dom_object in self.__dom_object_list:
                    elements = soup.find_all(dom_object)
                    for element in elements:
                        scraped_text += element.get_text().strip() + "\n"
                
                return scraped_text.strip()
                
        except Exception as e:
            return f"Error scraping {url}: {str(e)}"