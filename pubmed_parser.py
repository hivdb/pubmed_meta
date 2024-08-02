from metapub import PubMedFetcher
import pandas as pd
import argparse


def parse_pubmed(ids):
    '''
    Inputs:
       ids: .csv file [NO HEADER] with a list of PMIDs of interest 1 on each line.

    Output:
       tblReferences.csv file with the following columns:
          _RefID
          Author
          Title
          Journal
          RefYear
          MedlineID
          first author last name
          first author first name initial
          first author initials
        tblAuthors.csv file with the following columns:
          _RefID
          LastName
          Initials
    '''

    ids = pd.read_csv(ids, header=None)[0].values
    print(ids)

    output_data = {
        'RefID': [],
        'title': [],
        'year': [],
        'Author': [],
        'id': [],
        'journal': []}
    authors = {
        'RefID': [],
        'LastName': [],
        'Initials': []
        }  # RefID    LastName    Initials

    counter = 3410

    for entry in ids:
        fetch = PubMedFetcher()
        article = fetch.article_by_pmid(entry)
        title = article.title
        year = article.year
        journal = article.journal

        author_list = article.authors_str.split(';')
        first_author = author_list[0].strip()
        first_author = first_author.replace(' ', ', ')

        output_data['RefID'].append(counter)
        output_data['title'].append(title)
        output_data['year'].append(year)
        output_data['Author'].append(first_author)
        output_data['journal'].append(journal)
        output_data['id'].append(entry)

        for a in author_list:
            authors['RefID'].append(counter)
            lastname, firstname = a.strip().rsplit(' ', 1)
            authors['LastName'].append(lastname)
            authors['Initials'].append(firstname)

        counter += 1

    res = pd.DataFrame(output_data)
    res = res[['RefID', 'Author', 'title', 'journal', 'year', 'id']]
    res.columns = ['RefID', 'Author', 'Title', 'Journal', 'RefYear', 'MedlineID']
    res['Published'] = 'Yes'
    res.to_csv('tblReferences.csv', index=False, encoding='utf-8-sig')

    res2 = pd.DataFrame(authors)
    res2.to_csv('tblAuthors.csv', index=False, encoding='utf-8-sig')


def main():
    parser = argparse.ArgumentParser("PUBMED METADATA PARSER")
    parser.add_argument("ids", help=".csv file containing Pubmed IDs", type=str)
    args = parser.parse_args()

    print('\n-----PROCESSING-----')
    print(args.ids)
    print('--------------------\n')

    parse_pubmed(args.ids)
    print('done!')


if __name__ == '__main__':
    main()
