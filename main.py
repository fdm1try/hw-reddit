import requests
import html
from datetime import datetime


if __name__ == '__main__':
    endpoint = 'https://api.stackexchange.com/2.3/search/advanced'
    params = {
        'site': 'stackoverflow',
        'order': 'asc',
        'sort': 'creation',
        'tagged': 'python',
        'fromdate': int(datetime.today().timestamp() - (48 * 3600)),
        'pagesize': 100,
        'page': 1
    }
    max_retry = 3
    retry = 0
    question_count = 0
    while True:
        response = requests.get(endpoint, params=params)
        if response.status_code != 200:
            if retry == max_retry:
                raise Exception(
                    'The maximum number of attempts to obtain data has been exceeded.\n',
                    'HTTP status code: ', response.status_code
                )
            retry += 1
            continue
        retry = 0
        data = response.json()
        if 'error_message' in data:
            raise Exception('Stackoverflow API ERROR: ', data['error_message'])
        question_count += len(data['items'])
        for question in data['items']:
            print(datetime.fromtimestamp(question['creation_date']).strftime('%Y-%m-%d %H:%M:%S'), end=' ')
            print(*map(lambda tag: f'#{tag}', question['tags']))
            print(html.unescape(question['title']))
            print(question['link'], '\n')
        if not data['has_more']:
            break
        params['page'] += 1
    print(f'{question_count} questions have been asked in the last two days.')
