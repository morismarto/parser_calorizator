from src import Parser, Saver, HTML_Handler

URL = 'https://www.sochetaizer.ru/goods/caloricity?page=27'


if __name__ == '__main__':
    parser = Parser(url=URL)
    parser.parse()
    html_handler = HTML_Handler(response=parser.response, url=parser.url)
    html_handler.handle_link()
    parser = Parser(url=html_handler.links)
    parser.parse()
    print(parser.execution_time)
    html_handler = HTML_Handler(response=parser.response, url=parser.url)
    html_handler.handle_all_links()
    Saver(data=html_handler.data, url=parser.url, output_type=['csv', 'json'], filename='data').save()
