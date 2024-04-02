from metapub import PubMedFetcher
import pandas as pd
import argparse

def parse_pubmed(ids):
    '''
    Inputs:
       ids: .csv file [NO HEADER] with a list of PMIDs of interest 1 on each line.
    
    Output:
       tblReferences.csv file with the following columns: 
          RefID
          Author
          Title
          Journal
          RefYear
          MedlineID
          first author last name
          first author first name initial
          first author initials
        tblAuthors.csv file with the following columns: 
          RefID
          LastName
          Initials
    '''
    
    ids=pd.read_csv(ids,header=None)[0].values
    
    output_data={'title':[],'year':[],'lastname':[],'first_initial':[],'initials':[],'id':[],'journal':[]}
    for entry in ids:
        fetch = PubMedFetcher()
        article = fetch.article_by_pmid(entry)
        title=article.title
        year=article.year
        journal=article.journal
        lastname=article.author1_last_fm.split(' ')[0]
        first_initial=article.author1_last_fm.split(' ')[1]
        initials=first_initial + lastname[0]
        
        output_data['title'].append(title)
        output_data['year'].append(year)
        output_data['lastname'].append(lastname)
        output_data['first_initial'].append(first_initial)
        output_data['journal'].append(journal)
        output_data['initials'].append(initials)
        output_data['id'].append(entry)
            
    res=pd.DataFrame(output_data)
    res['RefID']=None

    authors=res[['RefID','lastname','initials']]
    authors.columns=['RefID','LastName','Initials']
    authors.to_csv('tblAuthors.csv',index=False)

    res['Author']=res['lastname']+', '+res['first_initial']
    res=res[['RefID','Author', 'title','journal','year','id']]
    res.columns=['RefID','Author','Title','Journal','RefYear','MedlineID']
    res['Published']='Yes'
    res.to_csv('tblReferences.csv',index=False)

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
