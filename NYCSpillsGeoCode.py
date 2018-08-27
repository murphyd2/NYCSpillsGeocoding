"""Dylan Murphy 2018-08-14 for MOER"""
#runs with pyton 3.6 due to usaddress not being supported in 3.7
import csv
import usaddress

class Goofy:

    def __init__(self,SpillNumber,ProgramFacilityName,Street1,Street2,Locality,County,ZIPCode,
                 SWISCode,DECRegion,SpillDate,ReceivedDate,ContributingFactor,Waterbody,Source,CloseDate
                 ,MaterialName,MaterialFamily,Quantity,Units,Recovered):
        self.housenumbers = None
        self.spaced_numbers = None
        self.letters = None
        self.parsed_address = [self.housenumbers,self.spaced_numbers,self.letters]
        self.spillnumber = SpillNumber
        self.PFN = ProgramFacilityName
        self.original_adr1 = Street1
        self.original_adr2 = Street2
        self.locality = Locality
        self.borough = County
        self.zip_code = ZIPCode
        self.swis = SWISCode
        self.dec = DECRegion
        self.spill_date = SpillDate
        self.recvd_date = ReceivedDate
        self.factor = ContributingFactor
        self.sink = Waterbody
        self.source = Source
        self.close_date = CloseDate
        self.material = MaterialName
        self.materialfamily = MaterialFamily
        self.quantity = Quantity
        self.units = Units
        self.recovered = Recovered

    def __repr__(self):
        return repr(
            (self.parsed_address, self.original_adr1,self.spillnumber, self.spill_date, self.factor,
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

def usadr_tag(string):
    """This function takes the string occupying the "Street 1" field in the Spill file and uses a custom mapping of
    Usaddress's tag function to parse the written address into a usable format that can be run through geosupport.
    Parameters:
    string- the string occupying "row["Street 1"] in the spill file

    Returns:
        tagged-address- a tuple in format (x,y) where x is an OrderedDict with custom tags instead of the default keys
        y is the address type according to usaddress;(choices are Street Address {most useful}, intersection{potentially
        viable}, Ambiguous{probably not}, and Unparsed{almost definitely not} """
    try:
        tagged_address,address_type= usaddress.tag(string,tag_mapping={
        'AddressNumber':'AddressNumber',
        'StreetName': 'Street 1',
        'StreetNamePreDirectional': 'Street 1',
        'StreetNamePreModifier': 'Street 1',
        'StreetNamePreType': 'Street 1',
        'StreetNamePostDirectional': 'Street 1',
        'StreetNamePostModifier': 'Street 1',
        'StreetNamePostType': 'Street 1',
        'BuildingName': 'Building Name',
        'CornerOf': 'CornerOf',
        'IntersectionSeparator': 'IntersectionSeparator',
        'SecondStreetName': 'Street 2',
        'SecondStreetNamePreDirectional': 'Street 2',
        'SecondStreetNamePreModifier': 'Street 2',
        'SecondStreetNamePreType': 'Street 2',
        'SecondStreetNamePostDirectional': 'Street 2',
        'SecondStreetNamePostModifier': 'Street 2',
        'SecondStreetNamePostType': 'Street 2',
        'LandmarkName': 'LandmarkName',
        'USPSBoxGroupID': 'address1',
        'USPSBoxGroupType': 'address1',
        'USPSBoxID': 'address1',
        'USPSBoxType': 'address1',
        'OccupancyType': 'address2',
        'OccupancyIdentifier': 'address2',
        'SubaddressIdentifier': 'address2',
        'SubaddressType': 'address2',
        'PlaceName': 'City',
        'StateName': 'State',
        'ZipCode': 'zip_code',
        'NotAddress':'NotAddress',
})
        print(tagged_address)
        return tagged_address,address_type
    except usaddress.RepeatedLabelError as err:
        UsaddressCatch(err.original_string,err.parsed_string)

def UsaddressCatch(original,parsed):
    pass

def function1_geosupport(taggedstr,borough):
    import geosupport
    countydict={'Manhattan':1,'Bronx': 2,'Kings':3,'Queens': 4,'Richmond':5 }
    if borough.title() in countydict:
        boro_code = countydict[borough.title()]
    else:
        print("Something in function1_geosupport happened: tried to use {} to find borough code.".format(borough))
        return
    if taggedstr:
        g = geosupport.Geosupport()
        result = g.call(function=1, house_number=taggedstr['AddressNumber'], borough_code=boro_code, street_name_1=taggedstr['Street 1'])
        print(result)
def main():
    """Parse mary full of grace... """



    with open("fullSpills.csv",'r') as f:
        fieldnames = ["SpillNumber","ProgramFacilityName","Street1","Street2","Locality","County","ZIPCode",
                      "SWISCode","DECRegion","SpillDate",'ReceivedDate','ContributingFactor','Waterbody','Source',
                      'CloseDate','MaterialName','MaterialFamily','Quantity','Units','Recovered']
        file=csv.DictReader(f,fieldnames=fieldnames,dialect='excel')
        goofylist_of_rows=[]
        file.__next__()
        line_count=0
        for row in file:
            if line_count <=15:
                t= Goofy(row[fieldnames[0]],row[fieldnames[1]],row[fieldnames[2]],row[fieldnames[3]],row[fieldnames[4]],
                             row[fieldnames[5]],row[fieldnames[6]],row[fieldnames[7]],row[fieldnames[8]],row[fieldnames[9]],
                             row[fieldnames[10]],row[fieldnames[11]],row[fieldnames[12]],row[fieldnames[13]],row[fieldnames[14]],
                             row[fieldnames[15]],row[fieldnames[16]],row[fieldnames[17]],row[fieldnames[18]],row[fieldnames[19]])
                tagged_address,address_type = usadr_tag(row["Street1"])
                if address_type == 'Street Address':
                    function1_geosupport(tagged_address,row["County"])
                line_count+=1
            else:
                print("done.")
                return

main()
"""
        if goofylist_of_rows:
            counter=0
            item_tot=0
            for x in goofylist_of_rows:
                item_tot+=1
                if None in (x.housenumbers,x.spaced_numbers):
                    counter+=1
            print("Percent filled: ",((counter/item_tot)*100))
            
def directional_prefix(adr_str,object):
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