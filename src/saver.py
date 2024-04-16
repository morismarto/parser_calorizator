__all__ = ['Saver']

from typing import Union, Literal
from loguru import logger
import json
import csv
import os



OUT_TYPE = Literal['json', 'csv']

class Saver:
    def __init__(self, data: list, url: Union[str, list], output_type: Union[OUT_TYPE, list], filename: str) -> None:
        ''' 
        Пример использования класса Saver:
            >>> s = Saver(response=parser.response, url=parser.url, output_type='json', filename='data')

            >>> s.save()
            The saving process has been started...
            The response is saved in a json file
        '''
        self.__data = data
        self.__url = url
        self.__output_type = output_type 
        self.__filename = f'data/{filename}'

    def save(self) -> None:
        if not os.path.exists('data'):
            os.mkdir('data')
        if self.__output_type == 'json':
            self.__save_json()
        elif self.__output_type == 'csv':
            self.__save_csv()
        elif isinstance(self.__output_type, list):
            self.__save_json()
            self.__save_csv()

    def __save_json(self) -> None:
        with open(file=f'{self.__filename}.json', mode='a', encoding='utf-8') as file:
            json.dump(self.__data, file, ensure_ascii=False, indent=4)
        logger.info('The data is saved in a json file')

    def __save_csv(self) -> None:
        with open(file=f'{self.__filename}.csv', mode='a', encoding='utf-8') as file:
            writer = csv.writer(file)

            col_names = ('Название', 'Описание', 'Калорийность', 'Белки', 'Жиры', 'Углеводы')

            writer.writerow(col_names)

            for item in self.__data:
                writer.writerow(
            (
                item['Название'],
                item['Описание'], 
                item['Пищевая ценность']['Калорийность'], 
                item['Пищевая ценность']['Белки'], 
                item['Пищевая ценность']['Жиры'], 
                item['Пищевая ценность']['Углеводы']
            )
        )

        logger.info('The data is saved in a csv file')

