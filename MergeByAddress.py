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
            if lefthalf[i].letters < righthalf[j].letters: #because its omparing ASCII values of the characters, a would be lower than z (97 < 122)
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
def WriteTo(linelist, outfile):
    """writes the sorted list to a CSV file with name outfile"""
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
    
    file = open("MN_PLUTO_SORTED.csv",'r')
    data= file.readlines()
    file.close()
    pointer=0
    linedict={} #effectively an enumerate of every line {"line+ str(intger)": <Id object>}
    lineList=[] #list of Id objects
    for line in data:
        Drew= "line"+str(pointer)
        fields=line.split(',')
        i=0
        for item in fields:
            WhoseLine= Id(fields[i],fields[i+1],fields[i+2],fields[i+3],fields[i+4],fields[i+5].upper(),fields[i+6],fields[i+7],fields[i+8],fields[i+9])
        pointer+=1
        linedict[Drew]=WhoseLine
        lineList.append(WhoseLine)
    #UnsortedList= linedict.values()
    #UnsortedList is a list containing Id objects
#    i=0
#    for item in lineList:
#        print(lineList[i].numbers)  
    mergeSort(lineList)
    WriteTo(lineList,"MN_PLUTO__ALPHA_SORTED.csv")
#    i=0
#    for item in lineList:
#        print(lineList[i].numbers)
#        i+=1
main()