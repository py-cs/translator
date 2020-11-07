import requests
from bs4 import BeautifulSoup
import sys

BASE_URL = 'https://context.reverso.net/translation'
langs = ['Arabic', 'German', 'English', 'Spanish',
         'French', 'Hebrew', 'Japanese', 'Dutch',
         'Polish', 'Portuguese', 'Romanian',
         'Russian', 'Turkish']


def top_num(data, num):
    return '\n' + '\n'.join(data[:num]) + '\n'


def translate(src, trg, word):
    direction = f'{langs[src].lower()}-{langs[trg].lower()}'
    url = '/'.join((BASE_URL, direction, word))
    user_agent = 'Mozilla/5.0'
    response = requests.get(url, headers={'User-Agent': user_agent})
    if response.status_code != 200:
        print('Something wrong with your internet connection')
        return None
    soup = BeautifulSoup(response.content, 'html.parser')
    elements = soup.find_all('a', class_='translation ltr dict no-pos')
    if not elements:
        print(f'Sorry, unable to find {word}')
        return None
    translations = [el.text.strip() for el in elements]
    elements = soup.find_all('div', class_=['src ltr', 'trg ltr'])
    examples = [el.text.strip() for el in elements]
    examples = [f'{examples[i]}:\n{examples[i+1]}' for i in range(0, len(examples), 2)]
    return f'\n{langs[trg]} Translations:\n{top_num(translations, 1)}' \
           f'\n{langs[trg]} Examples:\n{top_num(examples, 1)}'


def print_report(output):
    print(output)
    with open(f'{word}.txt', 'w', encoding='utf-8') as f:
        f.write(output)


def parse_args():
    args = sys.argv
    src = args[1].capitalize()
    if src in langs:
        src = langs.index(src)
    else:
        print(f"Sorry, the program doesn't support {src}")
        return None

    trg = args[2].capitalize()
    if trg in langs:
        trg = langs.index(trg)
    elif trg == 'All':
        trg = -1
    else:
        print(f"Sorry, the program doesn't support {trg}")
        return None
    
    word = args[3]
    return src, trg, word


args = parse_args()
if args:
    src, trg, word = args
    if trg == -1:
        output = ''
        for i in range(13):
            lng_output = translate(src, i, word)
            if lng_output:
                output += lng_output
        print_report(output)
    else:
        print_report(translate(src, trg, word))
