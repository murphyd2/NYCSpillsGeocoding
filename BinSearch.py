"Dylan Murphy"
"2018-07-13"
'Dylan Murphy 2018-07-03'

"""This Program cross checks addresses from the Petroleum spill database with addresses listed in 
the PLUTO csv file. these addresses have been edited and formatted in order to properly match.
It uses a binary search algorithms to search for matching addresses given one 
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
    items= a sorted list of Id objects
    desired_item = a Goofy Object looking for a matching .numbers field in items; single looking for a match (groovy baby)
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

    if desired_item.numbers == items[pos].numbers:
        checkfirstSpill=str(desired_item.letters.upper())
        checkfirstAddress=str(items[pos].letters.upper())
#        if checkfirstSpill[len(checkfirstSpill)//2:] in checkfirstAddress: # have to make sure that checkfirstspill shorter than checkfirst address
        if checkfirstSpill[1:-1] in checkfirstAddress:
            return pos
        else:
            i=1
            while desired_item.numbers==items[pos+i].numbers:
                checkfirstAddress=items[pos+i].letters.upper()
                if checkfirstSpill[1:-1] in checkfirstAddress:
                    print("Special case for {} + {} with {} + {}. Took {} steps".format(str(desired_item.numbers), checkfirstSpill, str(items[pos+i].numbers), checkfirstAddress, i))
                    return (pos+i)
                else:
                    i+=1
                    continue
            else:
                return 
            #if the next items dont match in numbers, and its been run thru to check for letter matches
            #return nothing
    elif int(desired_item.numbers) > int(items[pos].numbers):
        return binary_search(items, desired_item, start=(pos + 1), end=end)
    else: # desired_item < items[pos]:
        return binary_search(items, desired_item, start=start, end=pos)
    
def ReadThru(dic, key, SpillOrPluto):
    """This file takes a filename string, opens that file and reads its contents, and assigns each file the appropriate class objects.
    for the spill files which have a total of three fields in their 'meat' this class is 'Goofy' while for 
    
    Parameters:
    dic = dictonary object with values of filename strings
    key= key in dic to retrive a specific value 
    
    Returns:
    SpillObjects= list of Goofy objects from the Spill csv files.
    PlutoObjects= list of Id objects from the Pluto csv files.
    """
    
    
    sheet = dic.get(key)
    file= open(str(sheet), 'r')
    data = file.readlines()
    file.close()
    headers = data[0]
    meat = data[1:]#just the meat of the file no headers
    
    if SpillOrPluto=='Spill':
        SpillObjects=[]
        pointer = 1
        for line in meat:
            Drew= "line"+str(pointer)
            fields=line.split(',')
            i=0
            for item in fields:
                WhoseLine= Goofy(fields[i],fields[i+1],fields[i+2])
            SpillObjects.append(WhoseLine)        
            pointer+=1
            
        return SpillObjects
    
    elif SpillOrPluto=="Pluto":            
        PlutoObjects=[]
        pointer = 1
        for line in meat:
            Drew= "line"+str(pointer)
            fields=line.split(',')
            i=0
            for item in fields:
                WhoseLine= Id(fields[i],fields[i+1],fields[i+2],fields[i+3],fields[i+4],fields[i+5],fields[i+6],fields[i+7],fields[i+8],fields[i+9])
            PlutoObjects.append(WhoseLine)
            pointer+=1
            
        return PlutoObjects
    
def WriteTo(linelist, outfile):
    """writes the matches to a CSV file with name outfile"""
    file = open(str(outfile),'w')
    i=0
    for line in linelist:
        file.write(linelist[i].borough+ ',')
        file.write(linelist[i].block+ ',') 
        file.write(linelist[i].lot+ ',')
        file.write(linelist[i].numbers+ ',')
        file.write(linelist[i].spaced_numbers+ ',')
        file.write(linelist[i].letters+ ',')          
        file.write(linelist[i].BBL+ ',')
        file.write(linelist[i].x+ ',')
        file.write(linelist[i].y+ ',')
        file.write(linelist[i].E_des)
        i+=1
    file.close()
    
def main():
    plutodict={'BK':"BK_Pluto_2.0.csv",'BX':"BX_Pluto_2.0.csv",'SI':"SI_Pluto_2.0.csv"} 
    spillsdict={'BK':"BK_Spills_2.0.csv",'BX':"BX_Spills_2.0.csv",'SI':"SI_Spills_2.0.csv"}
    keylist= plutodict.keys()
    for i in keylist:
        SpillsList=ReadThru(spillsdict,i,'Spill')
        PlutoList=ReadThru(plutodict,i,'Pluto')
    #    i=0
    #    for item in mylist:
    #        print(SpillsList[i].letters)
    #        i+=1
        matchlist=[]
        for goo in SpillsList: #goo is goofy obj were searching for matches to
            matchindex=binary_search(PlutoList, goo, start=0, end=None)
            if matchindex != None:
                matchlist.append(matchindex)
    #    print(matchlist) #ok i have a match index this list has content 
        #is it right tho?
        #fixed an error where binary search was returning any items which matched in numbers 
        Matches=[]
        for success in matchlist:
            Matches.append(PlutoList[success])
        WriteTo(Matches, str(i)+"2.0_Matches.csv")
main()