__all__ = ['Parser']


from requests import get, Response, Session
from typing import Union, Callable
from concurrent.futures import ThreadPoolExecutor
from time import time
from loguru import logger


class Parser:
    def __init__(self, url: Union[str, list], workers_count: int = None) -> None:
        '''
        Пример использования класса Parser:
            >>> p = Parser(url='https://google.com')

            >>> p.parse()
            Parser is running...

            >>> p.url
            https://google.com

            >>> parser.response
            <Response>

            >>> parser.execution_time
            0.3
        '''
        self.__url = url
        self.__response: Union[Response, list[Response]] = None
        self.__execution_time: str = None
        self.__threads: list[ThreadPoolExecutor] = None
        self.__workers_count = workers_count


    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __get_exec_time(function) -> Callable[..., None]:
        def wraper(self, *args, **kwargs) -> None:
            t1: float = time()
            function(self, *args, **kwargs)
            self.__execution_time = f'Execution time is:{time() - t1: .1f}'
        return wraper

    @property
    def url(self) -> str:
        return self.__url
    
    @url.setter
    def url(self, value: Union[str, list]) -> None:
        self.__url = value
    
    @property
    def response(self) -> Response:
        return self.__response
    
    @property
    def execution_time(self) -> float:
        return self.__execution_time

    @__get_exec_time
    def parse(self) -> Response:
        logger.info('Parser is running...')
        if isinstance(self.__url, str):
            self.__response = get(self.__url)
        elif isinstance(self.__url, list):
            with Session() as session:
                with ThreadPoolExecutor(max_workers=self.__workers_count) as executor:
                    self.__threads = [executor.submit(session.get, url) for url in self.__url]
                    self.__response = [thread.result() for thread in self.__threads]
        logger.info('Done')