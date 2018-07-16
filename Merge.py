"Dylan Murphy"
"2018-07-12"
"This program attempts to take a csv file. create a dictonary with the building numbers as the keys. merge sort the keys and then create a sorted list of addresses by placing the values for that key [the whole address] at that index"

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
       
def purell(obj):
    scrubbed=''
    i=0
    for ch in obj.numbers:
        if ch.isalnum()==True:
            scrubbed+=obj.numbers[i]
            i+=1
        else:
            i+=1
    return scrubbed

def mergeSort(alist):
#    print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if int(lefthalf[i].numbers) < int(righthalf[j].numbers):
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1
#    print("Merging ",alist)
def WriteTo(linelist, outfile, SoP):
    """writes the sorted list to a CSV file with name outfile"""
    file = open(str(outfile),'w')
    i=0
    if SoP == 'P':
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
        
    elif SoP == 'S':
        for line in linelist:
            file.write(linelist[i].numbers+ ',')
            file.write(linelist[i].spaced_numbers+ ',')
            file.write(linelist[i].letters)
            i+=1
        file.close()
        
def SoP(SoP,dic,key):
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
    
    if SoP=='P':
        lineList=[]
        for line in meat:
            fields=line.split(',')
            i=0
            for item in fields:
                WhoseLine= Id(fields[i],fields[i+1],fields[i+2],fields[i+3],fields[i+4],fields[i+5],fields[i+6],fields[i+7],fields[i+8],fields[i+9])
                WhoseLine.numbers= purell(WhoseLine)      
            lineList.append(WhoseLine)
        
        return lineList
    
    elif SoP=='S':
        lineList=[]
        for line in meat:
            fields=line.split(',')
            i=0
            for item in fields:
                WhoseLine= Goofy(fields[i],fields[i+1],fields[i+2])
                WhoseLine.numbers= purell(WhoseLine)
            lineList.append(WhoseLine)
        
        return lineList
    
def main():
    plutodict={'BK':"BK_PLUTOFormatted_DateProneData_NOExcel.csv",'BX':"BX_PLUTOFormatted_DateProneData_NOExcel.csv",'SI':"SI_PLUTOFormatted_DateProneData_NOExcel.csv"} 
    spillsdict={'BK':"BrooklynSpillsFormatted_DateProneData_NOExcel.csv",'BX':"BronxSpillsFormatted_DateProneData_NOExcel.csv",'SI':"StatenIslandSpillsFormatted_DateProneData_NOExcel.csv"}
    
    keylist= plutodict.keys()
    for i in keylist:
        PlutoList=SoP('P', plutodict,i)
        SpillList=SoP('S', spillsdict,i)
 
        SortedBruv=mergeSort(SpillList)
        WriteTo(SpillList,str(i)+"_Spills_2.0.csv",'S')

        FixedBro=mergeSort(PlutoList)
        WriteTo(PlutoList,str(i)+"_Pluto_2.0.csv",'P')

main()