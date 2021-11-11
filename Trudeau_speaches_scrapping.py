# Scrap Trudeau's speaches text in french and english into files

import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm 


languages = ['fr', 'en']
webpages = [f'https://pm.gc.ca/{languages[0]}/videos?page={i}' for i in range(28)]
classname = 'field field--name-body field--type-text-with-summary field--label-hidden field--item'

for lang in languages:
    lang_text = []
    webpage = get(f'https://pm.gc.ca/{lang}/videos').text
    hrefs = [(tag.a.text, tag.a['href']) 
             for tag in pd.Series(BeautifulSoup(webpage, 'lxml')("div", "invisible")).unique()]
    for i, href in enumerate(hrefs):
        i += 1
        field_name, link = href
        video_html = requests.get('https://pm.gc.ca' + link).text
        lang_text.append(' '.join([tag.text 
                                   for tag 
                                   in BeautifulSoup(video_html,
                                                    "lxml")('div',
                                                            classname)[0].find_all()][:-1]
                                 ).replace('\xa0', ''))
        if i % 50 == 0:
          print(f'{i} texts scrapped\n')
    with open(f'Trudeau_{lang}.txt', 'w') as f:
        f.write('\n'.join(lang_text))
    print(f'Trudeau_{lang}.txt created and saved\n')
