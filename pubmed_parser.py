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
    
    ids=pd.read_csv(ids,header=None)[0].values
    
    output_data={'title':[],'year':[],'lastname':[],'first_initial':[],'initials':[],'id':[],'journal':[]}
    authors={'_RefID':[],'LastName':[],'Initials':[]} #RefID    LastName    Initials
    counter=0
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
    for a in article.authors:
            authors['_RefID'].append(counter)
            authors['LastName'].append(a.split(' ')[0])
            authors['Initials'].append(a.split(' ')[1]+a.split(' ')[0][0])
        counter+=1
            
    res=pd.DataFrame(output_data)
    res['_RefID']=[i for i in range(len(res))]
    res['Author']=res['lastname']+', '+res['first_initial']
    res=res[['_RefID','Author', 'title','journal','year','id']]
    res.columns=['_RefID','Author','Title','Journal','RefYear','MedlineID']
    res['Published']='Yes'
    res.to_csv('tblReferences.csv',index=False)

    res2=pd.DataFrame(authors)
    res2.to_csv('tblAuthors.csv',index=False)

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
