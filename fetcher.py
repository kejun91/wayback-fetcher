import mimetypes
import os
from pathlib import Path
import http_client

data_dir = os.path.join(Path(__file__).parent.resolve(), 'data')

def fetch_urls(website):
    timemap_url = f'https://web.archive.org/web/timemap/json?url={website}&matchType=prefix&collapse=urlkey&output=json&fl=original%2Cmimetype%2Ctimestamp%2Cendtimestamp%2Cgroupcount%2Cuniqcount&filter=!statuscode%3A%5B45%5D..&limit=10000'
    response = http_client.get(timemap_url)

    website_dir = os.path.join(data_dir, website)
    os.makedirs(website_dir, exist_ok=True)

    with open(os.path.join(website_dir, 'urls.json'), 'w') as f:
        f.write(response.text)

    for u in response.json()[1:]:
        url = u[0]
        fetch_snapshots(url, website_dir)

def fetch_snapshots(url, parent_dir):
    print(parent_dir)
    dir = os.path.join(parent_dir,url.split('/')[-1])
    print(url)
    print(dir)
    os.makedirs(dir,exist_ok=True)

    cdx_url = f'https://web.archive.org/cdx/search/cdx?url={url}&output=json'
    response = http_client.get(cdx_url)
    snapshots = response.json()
    for s in snapshots[1:]:
        timestamp = s[1]
        original = s[2]
        mime_type = s[3]

        arc_url = f'https://web.archive.org/web/{timestamp}/{original}'
        response = http_client.get(arc_url)
        store_content(dir, timestamp, mime_type, response.text)

def store_content(dir, timestamp, mime_type, content):
    ext = mimetypes.guess_extension(mime_type)
    with open(os.path.join(dir, timestamp + (('.' + ext) if ext is not None else '')), 'w', encoding='utf-8') as f:
        f.write(content)

websites = ['www.example.com']
if __name__ == '__main__':
    for w in websites:
        fetch_urls(w)