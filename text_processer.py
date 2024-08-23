import json
import os
from pathlib import Path
import re


def process_texts():
    unique_texts = []
    text_set = set()

    pattern = r"https://web\.archive\.org/web/\d{14}/"

    with open(os.path.join(Path(__file__).parent.resolve(), 'copypractice.json'), 'r') as f:
        content = f.read()
        d = json.loads(content)
        
        for k,v in d.items():
            text = v.get('text')
            if text is None or text == '':
                print('copypractice', k)
            else:
                if text not in text_set:
                    text_set.add(text)

                    if 'info' in v:
                        v['info'] = v.get('info','').replace('The sample text is taken from ', '')

                    if 'link' in v:
                        v['link'] = re.sub(pattern, '', v.get('link',''))
                    unique_texts.append(v)
    
    with open(os.path.join(Path(__file__).parent.resolve(), 'typingspeed.json'), 'r') as f:
        content = f.read()
        d = json.loads(content)
        
        for k,v in d.items():
            text = v.get('text')
            if text is None or text == '':
                print('typingspeed', k)
            else:
                if text not in text_set:
                    text_set.add(text)

                    if 'info' in v:
                        v['info'] = v.get('info','').replace('The sample text is taken from ', '')

                    if 'link' in v:
                        v['link'] = re.sub(pattern, '', v.get('link',''))
                    unique_texts.append(v)

    with open(os.path.join(Path(__file__).parent.resolve(), 'text_unique.json'), 'w') as f:
        json.dump(unique_texts, f)


# for t in ['copypractice','practicenumbers','typingspeed_alpha_numeric','typingspeed_num','typingspeed']:
#     process_texts(t)

process_texts()