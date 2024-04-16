__all__ = ['HTML_Handler']


from bs4 import BeautifulSoup
from requests import Response
from typing import Union


class HTML_Handler:
    def __init__(self, response: Response, url: Union[str, list]) -> None:
        ''' 
        Пример использования класса Handler:
            >>> html_handler = HTML_Handler(response=parser.response, url=parser.url)
            >>> html_handler.handle_all_links()
        '''
        self.__response = response
        self.__url = url
        self.__links: list = []
        self.__data: list= []

    @property
    def links(self) -> list:
        return self.__links
    
    @property
    def data(self) -> list:
        return self.__data

    def handle_link(self) -> None:
        soup = BeautifulSoup(markup=self.__response.text, features='lxml')
        html_a_tags = soup.findAll(name='a', class_='goods-table-item-info')
        for tag in html_a_tags:
            self.__links.append(f'{self.__url}'.replace('/goods/caloricity?page=27', tag.get('href'))) 

    def handle_all_links(self) -> None:
        for idx, res in enumerate(self.__response):
            soup: BeautifulSoup = BeautifulSoup(markup=res.text, features='lxml')
            try:
                name = soup.find(name='h1', class_='common-name').text
                description = soup.find(name='div', class_='body').text
                nutrients_name = [soup.find('table').find_all('td', class_='name')[i].text 
                                  for i in range(4)]
                nutrients_amount = [soup.find('table').find_all('td', class_='amount')[i].text 
                                    for i in range(4)]
            except:
                continue
            nutrients = {k: v for k, v in zip(nutrients_name, nutrients_amount)}
            self.__data.append({'Название': name, 'Описание': description, 'Пищевая ценность': nutrients})
        
            

            
            


        