
from notion.client import NotionClient
from urllib.request import urlretrieve
import os

invalid_websites = [
    'https://ieeexplore.ieee.org',
    'https://arxiv.org/abs/'
]

arxiv_root = 'https://arxiv.org/pdf/'

def main(token_v2, output_folder, database_link):
    #setup token
    client = NotionClient(token_v2=token_v2)

    #get collection
    cv = client.get_collection_view(database_link) 

    for row in cv.collection.get_rows():
        if row.downloaded == False:
            d_link = row.link
            print('Downloading 【{}】'.format(row.name))
            if row.link[:27] == invalid_websites[0]:
                print('Invalid URL')
                continue
            
            if row.link[:22] == invalid_websites[1]:
                d_link = arxiv_root + row.link.split('/')[-1] + '.pdf'

            else: 
                d_link = row.link
            
            try:
                urlretrieve(d_link, filename=os.path.join(output_folder, row.Conference + '_' + row.year + '_' + row.name + '.pdf'))
                row.downloaded = True
            except:
                print('Invalid URL')
    


if __name__ == '__main__':

    args = dict(
        token_v2 = '',
        output_folder =  '',
        database_link =  ''
    )
    
    main(**args)