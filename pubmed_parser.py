from metapub import PubMedFetcher
import pandas as pd
import argparse

def parse_pubmed(ids):
    '''
    Inputs:
       ids: .csv file [NO HEADER] with a list of PMIDs of interest 1 on each line.
    
    Output:
       .csv file with the following columns: 
          article
          title
          year
          first author last name
          first author first name initial
          first author initials
    '''
    
    ids=pd.read_csv(ids,header=None)
    input_data=''
    for v in ids[0].values:
        input_data+=str(v)+','
    input_data=input_data[0:-1]
    
    
    output_data={'title':[],'year':[],'lastname':[],'first_initial':[],'initials':[]}
    for entry in input_data.split(','):
        fetch = PubMedFetcher()
        article = fetch.article_by_pmid(entry)
        title=article.title
        year=article.year
        lastname=article.author1_last_fm.split(' ')[0]
        first_initial=article.author1_last_fm.split(' ')[1]
        initials=first_initial + lastname[0]
        
        output_data['title'].append(title)
        output_data['year'].append(year)
        output_data['lastname'].append(lastname)
        output_data['first_initial'].append(first_initial)
        output_data['initials'].append(initials)
            
    pd.DataFrame(output_data).to_csv('meta_data.csv',index=False)


def main():
    parser = argparse.ArgumentParser("PUBMED METADATA PARSER")
    parser.add_argument("ids", help=".csv file containing Pubmed IDs", type=str)
    args = parser.parse_args()
    
    print('\n-----PROCESSING-----')
    print(args.ids)
    print('--------------------\n')

    parse_pubmed(args.ids)
    print('done!')

main()
