'Dylan Murphy 2018-07-03'

"""This Program cross checks addresses from the Petroleum spill database with addresses listed in 
the PLUTO csv file. It uses a binary search algorithms to search for matching addresses given one 
from the active spills in Spills.Geocoding excel file"""

class Id:
    def __init__(self,borough, block, lot, numbers, spaced_numbers, letters, BBL, x, y, E_des):
        self.borough = borough
        self.block= block
        self.lot= lot
        self.numbers=numbers
        self.spaced_numbers= spaced_numbers
        self.letters=letters
        self.BBL=BBL
        self.x=x
        self.y=y
        self.E_des= E_des
        
    def __repr__(self):
        return repr((self.borough, self.block, self.lot, self.numbers,self.spaced_numbers, self.letters, self.BBL, self.x,self.y,self.E_des))
    
class Goofy:
    def __init__(self,numbers, spaced_numbers, letters):
        self.numbers=numbers
        self.spaced_numbers= spaced_numbers
        self.letters=letters
        
    def __repr__(self):
        return repr((self.numbers,self.spaced_numbers, self.letters))
    
    
def binary_search(items, desired_item, start=0, end=None,):
    
    """Standard Binary search program takes 
    
    Parameters:
    items= a sorted list
    desired_item = single looking for a match (groovy baby)
    start= int value representing the index position of search section
    end = end boundary of the search section; when end == start
    
    Returns:
    None = only returned if the desired_item not found in items
    pos = returns the index position of desired_item if found.
    """
    
    if end == None:
        end = len(items)

    if start == end:
        return None
#        raise ValueError("%s was not found in the list." % desired_item)

    pos = (end - start) // 2 + start

    if desired_item == items[pos]:
        return pos
    elif desired_item > items[pos]:
        return binary_search(items, desired_item, start=(pos + 1), end=end)
    else: # desired_item < items[pos]:
        return binary_search(items, desired_item, start=start, end=pos)
    
def OperationFILE(BoroughKey, BoroughDict):
    """If it becomes a problem move the Dict's out of the OperationFILE namespace into the mainspace 
    and reconfig parameters to be a key to be searched, and a dict to search.
    This function Identifies which boroughs records are being searched. It takes a key and a dictonary and opens up a CSV associated with that key. PLUTO consists of 5 csv's 
    specific to each Borough therefore it is most efficent to search with borough specific 
    desired_items. It reads the CSV's using file.readlines() for now but if this is too slow or taxing will do it by for loops? ugh that'd be gross
    
    Parameters:
    BoroughKey= string that will be evaluated against BoroughDict's keys to retrieve associatedvalue
    BoroughDict= dictonary that will be searched for matching keys with csv filenames as values. 
        
    Returns:
    data = lines of the csv
    headers= the first line of the Pluto csv not split! each list entry is a row) i.e. the column headings
    lines= the meat of the csv no headers (not split! each list entry is a row)
    """
    
    if BoroughKey in BoroughDict:
        sheet = BoroughDict[BoroughKey]
        file= open(str(sheet), 'r')
        data = file.readlines()
        file.close()
        headers = data[0]
        meat = data[1:]#just the meat of the file no headers
        return(data, headers, meat)
    
    elif BoroughKey not in BoroughDict:
        raise ValueError("%s was not found in the files." % BoroughKey)
        
def pull(AddressField, meat, BBLField=None):
    """This function takes the meat of the data files and splits them into fields to be searched. 
    It creates a dict Pullback where the keys are the addresses of the E-Designation properties in 
    each Borough.
    
    Parameters:
    
    AddressField= the index of the field where the string address is contained
    BBLField= OPTIONAL; the index of the field where the properties Borough Block and Lot identifer is contained. 
    appended to the dictonary as a str.
    meat= the headerless lines of a file. 
    
    Returns:
    items= a list of the addresses to be used in binary_search function.
    Pullback= dictonary object of address keys and BBL values and linenumbers."""
    
    Pullback={}#keys are the addresses values are [BBL, linenumber in meat object,]
    items=[]#items to be searched against; will be parameter in binary_search
    linenumber=0
    for line in meat:
        fields=line.split(',')
#        print(fields) #success! splits into fields line by line
        linenumber+=1
        i=0 
        for column in fields:
            if i==AddressField:
                spaced=column.split(' ')
                if type(BBLField) is int: #SHOULD Only be if pull is being called by Pluto not spill files
                    Pullback[fields[AddressField]]=[str(fields[int(BBLField)]),linenumber]
#                    sortable=oakum(fields[i])
                    items.append(spaced)
                elif BBLField == None: #spill file 'Goofy' call
                    Pullback[fields[AddressField]]=[linenumber]
#                    sortable=oakum(fields[i])
                    items.append(spaced)
                else:
                    raise TypeError("%s threw a wrench in 103 and 106 if statements. Should be either an int or Nonetype." % BBLField)
            i+=1
    return(Pullback, items)

def repull(Pullback, items):
    
    Throwback={}
    index=0
    keylist=Pullback.keys()
    for key in keylist:
        (NewKey,AddressString)=oakum(key)
        if Throwback.has_key(NewKey)==True:
            oldvalue=Throwback.get(NewKey)
            del Throwback[NewKey]
            Throwback[NewKey]= oldvalue + AddressString
        elif Throwback.has_key(NewKey)==False:
            Throwback[NewKey]=AddressString
    
    return(Throwback)

def main():
        
    #CSV files:
    WhereTo = {'BK':"BK_PLUTO.csv",'BX':"BX_PLUTO.csv",'MN':"MN_PLUTO.csv",'QN':"QN_PLUTO.csv" ,'SI':"SI_PLUTO.csv",'test':'BK_shortfile.csv' }
    
    SpillFiles={'Bronx':'BronxSpills.csv','Brooklyn':"BrooklynSpills.csv" ,'New York':"ManhattanSpills.csv" ,'Queens':"QueensSpills.csv" ,'Richmond':"StatenIslandSpills.csv",'Spilltest':'BrooklynSpill_shortfile.csv' }
    
    #Borough Codes (for county names)
    BoroughDecodes= {'1': 'New York', '2':'Bronx', '3': 'Brooklyn', '4':'Queens', '5':'Richmond'}
    
    #SearchBorough set to BK for a debugging best thing to do is probably set an input stmt
    SearchBorough='test'
    
    (Plutodata,headers,Plutomeat)=OperationFILE(SearchBorough, WhereTo) 
    #calls pull on returned Plutolines
    (PlutoPullback, Plutoitems)=pull(3,Plutomeat,4) #calls the pull function
#    Plutoheaders=str(headers).split(',')
#    print(Plutoheaders)
  
    SpillBorough= 'Spilltest' 
#    
    (Goofydata,Goofyheaders,Goofymeat)=OperationFILE(SpillBorough, SpillFiles)
    (GoofyPullback, Goofyitems)=pull(0,Goofymeat)
##    print(GoofyPullback)
##    print("*********************************" +"""
###    """)
#    print(Goofyitems)
    print(Plutoitems)
    print("*********************************" +"""
    """)
    print(sorted(data, key=lambda item: (int(item.partition(' ')[0])
                               if item[0].isdigit() else float('inf'), item)))
    #matches=[]
#    i=0
#    for line in Goofyitems:
#        
#        index= binary_search(Plutoitems,Goofyitems[i],start=0,end=None)
#        i+=1
#        print(index)
#        if index != None:
#            matches.append(Plutoitems[index])
#    print(matches)    
            
main()
"""
    will eventually evaluate the first digit of the BBL string in the first item of the first nested list int the list of Pullback's 
    values to select
    #BoroughCode = [[ch=x[0] for i in PlutoPullback.values() for x in i]for i in range(1)] #will probably have to debug this 
    #SpillSelect= BoroughDecodes.get(str(BoroughCode))
    ******************************************** Junk Pile Follows *******************************************************
    WhereTo = {'BK':"BK_PLUTO.csv",'BX':"BX_PLUTO.csv" ,'MN':"MN_PLUTO.csv" ,'QN':"QN_PLUTO.csv" ,'SI':"SI_PLUTO.csv",'test':'BK_shortfile.csv' }
    
    SpillFiles={'Bronx':'BronxSpills.csv','Brooklyn':"BrooklynSpills.csv" ,'New York':"ManhattanSpills.csv" ,'Queens':"QueensSpills.csv" ,'Richmond':"StatenIslandSpills.csv",'Spilltest':'BrooklynSpill_shortfile.csv' }
try:
        (Plutofields,Plutoheaders,Plutolines)=OperationFILE(SearchBorough)
    except ValueError as err:
        print(err.args)
        
def WriteTo(mylist, outfile):
    file = open(str(outfile)+'CommunityBoard.csv','w')
    i=0
    for item in mylist:
        file.write(str(mylist[i])+',\n')
        i+=1
    file.close()"""