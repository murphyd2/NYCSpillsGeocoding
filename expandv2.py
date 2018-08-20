"""Dylan Murphy 2018-08-14 for MOER"""
#runs with pyton 3.6 due to usaddress not being supported in 3.7
import csv
import re
import usaddress
class Goofy:

    def __init__(self, numbers, spaced_numbers, letters, spillnumber, spill_date, factor, close_date, material,
                 quantity, units):
        self.housenumbers = numbers
        self.spaced_numbers = spaced_numbers
        self.letters = letters
        self.spillnumber = spillnumber
        self.spill_date = spill_date
        self.factor = factor
        self.close_date = close_date
        self.material = material
        self.quantity = quantity
        self.units = units

    def __repr__(self):
        return repr(
            (self.housenumbers, self.spaced_numbers, self.letters, self.spillnumber, self.spill_date, self.factor,
             self.close_date, self.material, self.quantity, self.units))

    def set_house(self, string):
        self.housenumbers = string
        return self.housenumbers

    def set_spaced(self, string):
        self.spaced_numbers = string
        return self.spaced_numbers

    def set_street(self, string):
        self.letters = string
        return self.letters

def regrab1(adr_str,object):
    """this regex expression goes after the simplest case: housenumber with a apace after it and no prefix"""
    regex = r"^((\d+)\s)(.+)"
    result = re.findall(regex, adr_str, re.MULTILINE)

    if result:
        # print(result)
        for i in result:
            Goofy.set_spaced(object, i[0])
            Goofy.set_house(object, i[1])
            Goofy.set_street(object, i[2])
    return object

def sub_slash(adr_str,object):
    regex = regex = r"(\W)(/)(\W)?"
    subst = "\\g<1>& "

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, adr_str, 0, re.MULTILINE)

    if result:
        for i in result:
            Goofy.set_street(object, i)
    return object

def main():
    """Parse mary full of grace... """
    with open("2018.08.14_Book1.csv",'r') as f:
        file=csv.reader(f,'excel')
        goofylist_of_rows=[]
        for row in file:
            t= Goofy(None,None,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
            goofylist_of_rows.append(sub_slash(row[0],t))
        print(goofylist_of_rows)
        if goofylist_of_rows:
            counter=0
            item_tot=0
            for x in goofylist_of_rows:
                item_tot+=1
                if None in (x.housenumbers,x.spaced_numbers):
                    counter+=1
            print("Percent filled: ",((counter/item_tot)*100))

main()
"""def directional_prefix(adr_str,object):
    regex= r"^((W|w|E|e|N|s|S)([A-Za-z]+)?)"
    result =re.findall(regex,adr_str,re.MULTILINE)
    if result:
        # print(result)
        for i in result:
            Goofy.set_spaced(object, i[0])
            Goofy.set_house(object, i[1])
            Goofy.set_street(object, i[2])
    return object
"""