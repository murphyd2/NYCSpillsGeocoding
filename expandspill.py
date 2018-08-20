"Dylan Nurphy"
"2018-07-11"
"This file "
            
def digimon(string):
    """recurses over a string until it finds an alphabetical character, which it then returns the index of"""
    for ch in string:
        if ch.isalpha()==True:
            return(ch)
            break
        else:
            dex=string.index(ch)
            digimon(string[dex+1:])
            
# def aphid(string):
# #    "an attempt to accomplish the same goal as digimon() through iteration in the hopes it would be faster. abandoned because it through up bugs. Ideally this iterates over a string, skipping spaces and numbers until it reaches the first letter of the string. upon reaching that letter, should return that letter."
# #    i=0
# #    for ch in string[i]:
# #        if ch.isalpha()==True:
# #            return(ch)
# #        elif ch.isspace()==True:
# #            i+=1
# #        elif ch.isdigit()==True:
# #            i+=1

def xacto(fields,x,y,z):
    """xacto is a function which takes a list of strings iterates through this list until it reaches a passed index 'x' it then runs the recursive function digimon to find the first letter in the string,finds the index of that letter in the string, 
    splits the string into just numbers 'TopTP' and just letters 'BottomTP'. Because TopTP might have spaces between numbers it then runs the function glue to remove only the spaces leaving '123 4' as '1234' spaceless numbers are assigned to blue. 
    Making sure that x field is not blank, xacto splits the string at its first letter, removes the spaces from the address 
    numbers and inserts them into the list of strings after removing the original address. Spaceless numbers go into the 
    original position of the x address field, spaced numbers are inserted one to the right of x (y), and street names one to the right of that (z).

    This function takes 4 Parameters:
    fields= a list of strings
    x= an integer representing the index of the address field in each line
    y = index of the 'spaced' address numbers 
    z= the integer representing the index of the field containing the street name after xacto runs (x +2)"""
    i=0 
    for column in fields:
        if i ==x and column !='':
            address=str(column)
            Alpha=digimon(address)
            #check index character and adjacent letters to make sure they are not 'th' 'st'
            
            if Alpha != None and address.index(Alpha) != 0:
                PlaceOnTheTotemPole=address.index(Alpha)
                TopTP=''
                TopTP=address[:PlaceOnTheTotemPole]
                BottomTP=''
                BottomTP=address[PlaceOnTheTotemPole:]
                blue=""
                (blue)=glue(TopTP)
                AxingTheTP=TopTP +','+BottomTP
                fields.remove(column)
                fields.insert(x,blue) 
                fields.insert(x+1,TopTP) 
                fields.insert(x+2,BottomTP)

                i=z
            else:
                raise ValueError("{} is not a usable line. Taken as Address:{}. Letter: {}. Index: {}. SplitString:{}.".format(fields, address, Alpha, PlaceOnTheTotemPole, AxingTheTP))
        elif i<x:
            i+=1
        elif i==z or i>y:
            return(fields)

def WriteTo(linelist, outfile):
    """writes the edited csv data with its original headers (i.e. the headers aren't gapped appropriately w/ regard to the inserted y and z columns of xacto)(mostly out of laziness). takes a list and a string. list consists of lines to be written str is the new files name"""
    file = open(str(outfile),'w')
    i=0
    for line in linelist:
        s=''
        for field in line:
            if field==line[-1]:
                repr(field)
                s+=str(field)
            else:    
                s+=str(field)+','
        file.write(s)
        i+=1
    file.close()
    
    
def glue(number):
    i=0
    s=''
    red=''
    pop=number.split(' ')
    red=s.join(pop)
    return(red)

def iterate(dic,whichvalue,p,q,s):
    """iter's through a dictionary whose values are csv filenames. opens and reads each file in 
    sequence, then splits files into lists containing the headers and a list which is just the data. uses the module 
    progressbar2 to let me know its actually working so i dont freak out and close it in the middle of it (lol). goes line 
    by line in the data. first splits the line into its fields using commas, then attempts to append the returned values 
    of the xacto function to a list titled labels. if it doesnt work/ some shit goes down it prints an error message 
    raised in line 57

    
    
    Parameters:
    dic= dictonary object whose values consist of strings representing csv filenames
    whichvalue= specific key in dic
    p= integer which gets passed into the xacto function as x
    q= integer which gets passed into the xacto function as y
    s= integer which gets passed into the xacto function as z
    
    Returns:
    sheet= list object containg only a string which is a file name
    fields= list containg the entire contents of a file to written"""
    
    sheet= dic.get(whichvalue)
    file= open(str(sheet), 'r') 
    data = file.readlines()
    file.close()
    headers =list(data[0])
    meat = data[1:]#just the meat of the file no headers
    linenumber=0
    labels=[]
    for item in meat:
        fields=item.split(',')    
        try:
            labels.append(xacto(fields,p,q,s))
        except ValueError as err:
            print(err)
    fields=headers+labels
    return (sheet,fields)
    
def main():
    """Main. Takes no parameters, asks for user input to determine what csv files to run with."""
    while True: 
        #what type of source file
        try:
            filechoice=input("""To run through the Pluto addresses write 'PLUTO'. 
    For Spills, write 'Spill':""")
            if filechoice not in ['PLUTO','Spill']:
                raise ValueError
        except ValueError:
            print('Whoops try again')
            continue
        else:
            print("Expanding %s" % filechoice)
            break
            
    if filechoice=='PLUTO':
        WhereTo = {'QN':"QN_PLUTO.csv",'SI':"SI_PLUTO.csv",'MN':"MN_PLUTO.csv",'BK':"BK_PLUTO.csv",'BX':"BX_PLUTO.csv"}
        list1=[]
        keylist= WhereTo.keys()
        while True:
            #which borough
            try:
                yellow=str(input('Enter the Borough Key (BK, BX, MN, QN, SI): '))
                if yellow not in keylist:
                    raise ValueError
            except ValueError:
                print("Input did not match possible options: BK, BX, MN, QN, SI. Try again.")
                #better try again... Return to the start of the loop
                continue
            else:
                print("Running %s..." % yellow)
#                return yellow
                break
        
        print("Borough: "+str(yellow))
        whichvalue=yellow
        (plutosheet, plutofields)=iterate(WhereTo,whichvalue,3,4,5)
        list1.append([plutosheet, plutofields])
        
        for roger in list1:
            sheet=roger[0]
            fields=roger[1]
            WriteTo(fields,str(sheet[:-4]+"Formatted_DateProneData_NOExcel.csv"))

    if filechoice=='Spill':
        SpillFiles={'Bronx':'BronxSpills.csv','Brooklyn':"BrooklynSpills.csv" ,'New York':"ManhattanSpills.csv" ,'Queens':"QueensSpills.csv" ,'Richmond':"StatenIslandSpills.csv"}        
        list2=[]
        spill_list= SpillFiles.keys()
        while True:
            #which borough
            try:
                green=str(input('Enter the Borough Key, %s: ' % ['Bronx', 'Brooklyn', 'New York', 'Queens', 'Richmond']))
                if green not in spill_list:
                    raise ValueError
            except ValueError:
                print("Input did not match possible options: BK, BX, MN, QN, SI. Try again.")
                #better try again... Return to the start of the loop
                continue
            else:
                print("Running %s..." % green)
                break
        print("Borough"+str(green))
        whichvalue=green
        (goofysheet, goofyfields)=iterate(SpillFiles,whichvalue,0,1,3)
        list2.append([goofysheet,goofyfields])
        
        for roger in list2:
            sheet=roger[0]
            fields=roger[1]
            WriteTo(fields,str(sheet[:-4]+"Formatted_DateProneData_NOExcel.csv"))
main()
