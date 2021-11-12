# Scrap Trudeau's speaches text in french and english

import pandas as pd
from bs4 import BeautifulSoup
from requests import get


languages = ['fr', 'en']
classname = 'field field--name-body field--type-text-with-summary field--label-hidden field--item'

n = {'fr':[0, []], 'en':[0, []]}

for lang in languages:
    lang_text = []
    webpage = get(f'https://pm.gc.ca/{lang}/videos').text
    hrefs = [(tag.a.text, tag.a['href']) 
             for tag in pd.Series(BeautifulSoup(webpage, 'lxml')("div", "invisible")).unique()]
    for i, href in enumerate(hrefs):
        field_name, link = href
        video_html = get('https://pm.gc.ca' + link).text
        check = BeautifulSoup(video_html, "lxml")('div', classname)[0]
        if check.a:
            try:
                'https://twitter.com/' in check.a['href']
                if 'https://twitter.com/' in check.a['href']:
                    n[lang][0] += 1
                    n[lang][1] += ['https://pm.gc.ca' + link]
                    if (i + 1) % 50 == 0:
                        print(f'{i + 1} links checked')
                    continue
            except:
                print('https://pm.gc.ca' + link)
                lang_text.append(' '.join([tag.text 
                                   for tag 
                                   in BeautifulSoup(video_html,
                                                    "lxml")('div',
                                                            classname)[0].find_all(name='p')]
                                 ).replace('\xa0', '\n'))
        if (i + 1) % 50 == 0:
            print(f'{i + 1} links processed')
            
        lang_text.append(' '.join([tag.text 
                                   for tag 
                                   in BeautifulSoup(video_html,
                                                    "lxml")('div',
                                                            classname)[0].find_all(name='p')]
                                 ).replace('\xa0', '\n'))
    with open(f'Trudeau_{lang}.txt', 'w') as f:
        f.write('\n'.join(lang_text))
