import os
from pathlib import Path

from bs4 import BeautifulSoup


def get_text(data_type):
    texts = {}
    for dirpath, dirnames, filenames in os.walk(os.path.join(Path(__file__).parent.resolve(), 'data', data_type + '.php')):
        for file in filenames:
            # print(dirpath)
            # print(file)
            content = ''
            with open(os.path.join(dirpath, file), 'r') as f:
                content = f.read()
            s = BeautifulSoup(content, 'lxml')
            original_text = s.find('input', {'name':"originalText"})
            am_link = s.find('a', {'id':"amLink"})

            text = {}

            if original_text is None:
                sample_text = s.find('p',{'id':'sampleText'})
                if sample_text is not None:
                    text['text'] = sample_text.string
            else:
                text['text'] = original_text.get('value')
            
            if am_link is not None:
                text['link'] = am_link.get('href')
            
            # info = [s for s in s.find_all('span') if 'The sample text is taken from' in s.string][0]
            all_spans = s.find_all('span')
            if len(all_spans) > 0:
                text['info'] = all_spans[-1].get_text()
            texts[file.split('.')[0]] = text

    with open(dirpath.split(os.path.sep)[-1].split('.')[0] + '.json', 'w') as f:
        import json
        json.dump(texts, f)
    # print(texts)

# print(get_text())
for t in ['copypractice','practicenumbers','typingspeed_alpha_numeric','typingspeed_num','typingspeed']:
    get_text(t)