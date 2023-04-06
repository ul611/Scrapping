#!/usr/bin/env python
# coding: utf-8

# Scrap Trudeau's speeches text in French and English

import time
import pandas as pd
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
import re

start_time = time.time()
languages = {'fr': 'French', 'en': 'English'}
classname = 'field field--name-body field--type-text-with-summary field--label-hidden field--item'

n = {'fr': [0, []], 'en': [0, []]}

for lang in languages:
    print(f'Start processing {languages[lang]} language...')
    lang_text = []
    webpage = get(f'https://pm.gc.ca/{lang}/videos').text
    print(f'Start collecting video hyperlinks...')
    hrefs = [(tag.a.text, tag.a['href'])
             for tag in pd.Series(BeautifulSoup(webpage, 'lxml')("div", "invisible")).unique()]
    print(f'{len(hrefs)} links were collected.')
    print(f'Start handling video transcriptions...')
    for href in tqdm(hrefs):
        field_name, link = href
        video_html = get('https://pm.gc.ca' + link).text
        check = BeautifulSoup(video_html, "lxml")('div', classname)[0]
        if check.a:
            try:
                if 'https://twitter.com/' in check.a['href']:
                    n[lang][0] += 1
                    n[lang][1] += ['https://pm.gc.ca' + link]
                    continue
            except:
                # print('https://pm.gc.ca' + link) # fake links
                lang_text.append(' '.join([tag.text
                                   for tag
                                   in BeautifulSoup(video_html,
                                                    "lxml")('div',
                                                            classname)[0].find_all(name='p')]
                                 ).replace('\xa0', '\n'))
            
        lang_text.append('\n'.join([tag.text
                                   for tag
                                   in BeautifulSoup(video_html,
                                                    "lxml")('div',
                                                            classname)[0].find_all(name='p')]
                                 ).replace('\xa0', ''))

    print(f'Video transcriptions in {languages[lang]} were handled.')
    # save file with all speeches text
    with open(f'Trudeau_{lang}.txt', 'w') as f:
        f.write('\n'.join(lang_text))
    print(f'File "Trudeau_{lang}.txt" with all {languages[lang]} speeches text was saved.')
    # save links to videos without transcription
    print(f'Number of videos without transcription ({languages[lang]}) - {n[lang][0]}.')
    with open(f'videos_without_transcription_{lang}.txt', 'w') as f:
        f.write('\n'.join(n[lang][1]))
    print(f'File "videos_without_transcription_{lang}.txt" with links to {languages[lang]} videos without transcription was saved.')

end_time = time.time()
print(f'Everything is done. Time spent - {round(end_time - start_time)} (😱) seconds.')
