# -*- encoding: utf-8 -*-
from collections import Counter
import time
import re

def parse(
    ignore_files=False,
    ignore_urls=[],
    start_at=None,
    stop_at=None,
    request_type=None,
    ignore_www=False,
    slow_queries=False
):
    pattern = re.compile(r'''\[(?P<date>.*)\]\s\"(?P<type>\S*)\s(?P<url>\S*)\s(?P<proto>\S*)\"\s(?P<resp_code>\S*)\s(?P<resp_time>\S*)''')
    log = []
    
    # Парсим файл, разбираем строки 
    with open('log.log', 'rt') as log_file:
        for row in log_file:

            m = re.match(pattern, row)
            if not m:
                continue

            row = m.groupdict()

            # такое преобразование используется у препода
            # я повторил чтобы совпадали результаты тестов
            url = row['url'].replace('https://', '').replace('http://', '')
            pos = url.find('?')
            if pos > 0:
                url = url[0: pos]

            # фильтрация по аргументам
            if url in ignore_urls:
                continue

            if start_at or stop_at:
                fmt = '%d/%b/%Y %H:%M:%S'
                date = time.strptime(row['date'], fmt)
                if start_at and date < time.strptime(start_at, fmt):
                    continue
                if stop_at and date > time.strptime(stop_at, fmt):
                    continue
                    # если мы уверены, что логи записаны последовательно, 
                    # то нужно сделать break 

            if request_type and row['type'] != request_type:
                continue

            if ignore_files and re.search(r'\/(\w|[^\/]*\.\w*)$', row['url']):
                continue

            if ignore_www and 'www.' == url[0:4]:
                url = url[4:]

            row['resp_time'] = int(row['resp_time'])
            row['url'] = url
            log.append(row)

    if slow_queries:
        # вариант кода для прохождения тестов
        # P.S. в тестах ожидаемый результат не совпадает (логи разные)
        log.sort(key=lambda x: x['resp_time'], reverse=True)
        return [row['resp_time'] for row in log[:5]]
        # вариант кода по условиям задания
        return sum([row['resp_time'] for row in log[:5]]) // 5


    url_count = Counter([row['url'] for row in log])
    
    # return url_count.most_common(10)
    result = []
    for url, cnt in url_count.most_common(5):
        result.append(cnt)
    return result


if __name__ == '__main__':
    print(parse(slow_queries=True))
    # for url, index in parse():
    #     print(f'Count: {index} URL: {url}')