import commodities_quotes as cq
import setup
import os


def main(quotes,path,start_date, end_date,
         instrument_type='commodities', ):
    #=os.path.abspath(__name__)):
    for quote in quotes:
        quote_setup = cq.Quotes(quote,start_date,end_date)
        
        data = quote_setup.get_data()

#print('my path:   ',path)
 #           data.to_csv(path+quote+'.csv',index=False)
        
        try:
            print('my path:   ',path)
            data.to_csv(path+quote+'.csv',index=False)
        except AttributeError:
            pass


if __name__=='__main__':
    
    instrument_type = 'commodities'
    setup_ = setup.Folders(instrument_type)
    setup_.check_folders()
    
    
    path = setup_.path
    print(path)
    
    start_date = '01/01/2020'
    end_date = '01/01/2021'
    quotes = ['Gold','CL']
    
    main(quotes,path,start_date,end_date)
    
    
