
from notion.client import NotionClient
from urllib.request import urlretrieve
import requests
import os
from keys import args

invalid_websites = [
    'https://ieeexplore.ieee.org',
    'https://arxiv.org/abs/'
]

arxiv_root = 'https://arxiv.org/pdf/'

headers = requests.utils.default_headers()
headers.update(
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2',
    }
)

def main(token_v2, output_folder, database_link):
    #setup token
    client = NotionClient(token_v2=token_v2)

    #get collection
    cv = client.get_collection_view(database_link) 

    for row in cv.collection.get_rows():
        if row.downloaded == False:
            d_link = row.link
            print('Downloading [{}]'.format(row.name))
            if row.link[:27] == invalid_websites[0]:
                print('Invalid URL:', row.link)
                continue
            
            if row.link[:22] == invalid_websites[1]:
                d_link = arxiv_root + row.link.split('/')[-1] + '.pdf'

            else: 
                d_link = row.link
            
            
            #try:
            if len(d_link) < 5:
                print('Invalid URL')
                continue
            else:
                conf  = row.Conference if row.Conference is not None else ''
                yr    = row.year if row.year is not None else ''
                fname = os.path.join(output_folder, conf + '_' + yr + '_' + row.name + '.pdf')

                try:
                    response = requests.get(d_link, headers=headers)
                    open(fname, 'wb').write(response.content)
                    #urlretrieve(d_link, filename=os.path.join(output_folder, conf + '_' + yr + '_' + row.name + '.pdf'))
                    row.downloaded = True
                except:
                    print('faided to download:', d_link)
    


if __name__ == '__main__':
    print(args)
    main(**args)
