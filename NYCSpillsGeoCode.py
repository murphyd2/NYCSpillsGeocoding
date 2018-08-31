"""Dylan Murphy 2018-08-14 for MOER"""
# runs with python 3.6 due to usaddress not being supported in 3.7
import csv
import usaddress
import datetime


class Goofy:
    "Class for easy storage and retrieval of data from the Spill CSV. All Columns in the CSV are shown here."
    def __init__(self, SpillNumber, ProgramFacilityName, Street1, Street2, Locality, County, ZIPCode,
                 SWISCode, DECRegion, SpillDate, ReceivedDate, ContributingFactor, Waterbody, Source, CloseDate
                 , MaterialName, MaterialFamily, Quantity, Units, Recovered,lat,lon):
        self.parsed_address = None
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
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return repr(
            (self.parsed_address, self.original_adr1, self.spillnumber, self.spill_date, self.factor,
             self.close_date, self.material, self.quantity, self.units,self.lat, self.lon))


    def set_house(self, string):
        self.housenumbers = string
        return self.housenumbers

    def set_spaced(self, string):
        self.spaced_numbers = string
        return self.spaced_numbers

    def set_street(self, string):
        self.letters = string
        return self.letters

    def set_latlon(self,latitude,longitude):
        self.lat = latitude
        self.lon = longitude
        return self.lat,self.lon


def sub_slash(adr_str):
    """This regex statement processes the initial spill files to avoid a case where intersections were improperly parsed
    as street addresses"""
    # https: // regex101.com / r / YlbKq2 / 1
    import re

    regex = r"( st)(/)(\w+)"

    subst = "\\g<1> & \\g<3>"

    # You can manually specify the number of replacements by changing the 4th argument
    result = re.sub(regex, subst, adr_str, 0, re.MULTILINE | re.IGNORECASE)

    return result


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
        tagged_address, address_type = usaddress.tag(string, tag_mapping={
            'AddressNumber': 'AddressNumber',
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
            'ThirdStreetName': 'Street 3',
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
            'NotAddress': 'NotAddress',
        })
        print(tagged_address, string[:-10])
        return tagged_address, address_type
    except usaddress.RepeatedLabelError as err:
        print('UsaddressCatch')
        tagged_address, address_type = UsaddressCatch(err.original_string, err.parsed_string)
        return tagged_address,address_type

def UsaddressCatch(original, parsed):
    with open("{} USaddressErrors.csv".format(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d %I")),
              'a') as f:
        file = csv.writer(f, dialect='excel')
        file.writerow([original, parsed])
    klist = []
    vlist = []
    tagged_address={'Street 1':'',
                    'IntersectionSeparator':'',
                    'Street 2':'',
                    'Address Number':'',
    }
    for (k,v) in parsed:
        klist.append(k)
        vlist.append(v)
    return False,False
    # if 'IntersectionSeparator' in vlist:
    #     address_type = "Intersection"
    #     inter_sep_idx = vlist.index('IntersectionSeparator')
    #     first_idx = vlist.index('StreetName')
    #
    #     tagged_address['IntersectionSeparator'] = klist[inter_sep_idx]
    #     tagged_address['Street 1'] = klist[first_idx]
    #     vlist.pop(first_idx)
    #     second_idx = vlist.index('StreetName')
    #     tagged_address['Street 2'] = klist[second_idx]
    #     return tagged_address, address_type
    #
    # elif 'AddressNumber' in vlist:
    #     #and intersectionsep not in
    #     address_type = 'Street Address'
    #     adr_num_idx = vlist.index('AddressNumber')
    #
    #     collect_street_portions = []
    #     for i in vlist[adr_num_idx:]:
    #         if 'StreetName' in i:
    #             collect_street_portions.append(vlist.index(i))
    #     street_string=''
    #     for idx in collect_street_portions:
    #         street_string += (klist[idx]+ ' ')
    #     streetname_after_adr = vlist.index('StreetName',adr_num_idx)
    #     print(klist[streetname_after_adr])
    #     print(street_string)
    #     tagged_address['Address Number']= klist[adr_num_idx]
    #     tagged_address['Street 1'] = street_string
    #     return tagged_address, address_type
    # else:
    #     return False,False


def function1_geosupport(taggedstr, borough, goofyobject):
    import geosupport
    countydict = {'Manhattan': 1, 'New York': 1, 'Bronx': 2, 'Kings': 3, 'Queens': 4, 'Richmond': 5}
    if borough.title() in countydict:
        boro_code = countydict[borough.title()]
    else:
        raise ValueError(
            "Something in function1_geosupport happened: tried to use {} to find borough code.".format(borough))

    if taggedstr:
        g = geosupport.Geosupport()
        result = g.call(function=1, house_number=taggedstr['AddressNumber'], borough_code=boro_code,
                        street_name_1=taggedstr['Street 1'])
        latitude, longitude = longlat_transform(result['SPATIAL X-Y COORDINATES OF ADDRESS']['X Coordinate'],
                          result['SPATIAL X-Y COORDINATES OF ADDRESS']['Y Coordinate'])
        goofyobject.set_latlon(latitude, longitude)
        return goofyobject



def function2_geosupport(taggedstr, borough, goofyobject):
    import geosupport
    countydict = {'Manhattan': 1, 'New York': 1, 'Bronx': 2, 'Kings': 3, 'Queens': 4, 'Richmond': 5}
    if borough.title() in countydict:
        boro_code = countydict[borough.title()]
    else:
        raise ValueError(
            "Something in function2_geosupport happened: tried to use {} to find borough code.".format(borough))
    if taggedstr:
        g = geosupport.Geosupport()
        result = g.call(function=2, street_1=taggedstr["Street 1"], street_2=taggedstr["Street 2"],
                        borough_code=boro_code)

        latitude, longitude =longlat_transform(result['SPATIAL COORDINATES']['X Coordinate'], result['SPATIAL COORDINATES']['Y Coordinate'])
        goofyobject.set_latlon(latitude, longitude)
        return goofyobject



def geocalls(parsedAddresses):
    """once all addresses are parsed, takes them and pass them into Geosupport functions.

    parsedAddresses = [(tagged address,address type) County, goofyobject]

    returns a list of all parsed rows as Goofy Objects"""
    from geosupport.error import GeosupportError
    outlist = []
    for address in parsedAddresses:
        if address[1] == 'Street Address':
            try:
                processed = function1_geosupport(address[0], address[2], address[3])
                outlist.append(processed)
            except (GeosupportError, ValueError) as e:
                errlog(e, address)
        elif address[1] == 'Intersection':
            try:
                processed = function2_geosupport(address[0], address[2], address[3])
                outlist.append(processed)
            except (GeosupportError, ValueError) as e:
                errlog(e, address)
                # print("Street 1, Street 2, error", taggedstr["Street 1"], taggedstr["Street 2"], e)
    return outlist

def longlat_transform(x1, y1):

    from pyproj import Proj, transform
    x1 = x1.lstrip('0')
    y1 = y1.lstrip('0')
    inProj = Proj("++proj=lcc +lat_1=41.03333333333333 +lat_2=40.66666666666666 +lat_0=40.16666666666666 +lon_0=-74 "
                  "+x_0=300000.0000000001 +y_0=0 +ellps=GRS80 +units=us-ft +no_defs  ", preserve_units=True)
    outProj = Proj(proj='longlat', datum='WGS84')

    lon, lat = transform(inProj, outProj, x1, y1)
    print(lat,lon)
    return lat,lon


def errlog(error, address):
    with open("{} GeosupportErrors.csv".format(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d %I")),
              'a', newline='') as f:
        file = csv.writer(f, dialect='excel')
        file.writerow(address)
        file.writerow([error])

def WriteTo(listofrows):
    with open('test.csv','w',newline='') as butter:
        fieldnames = ["Parsed Address","SpillNumber", "ProgramFacilityName", "Street1", "Street2", "Locality", "County", "ZIPCode",
                      "SWISCode", "DECRegion", "SpillDate", 'ReceivedDate', 'ContributingFactor', 'Waterbody', 'Source',
                      'CloseDate', 'MaterialName', 'MaterialFamily', 'Quantity', 'Units', 'Recovered', 'Latitude', 'Longitude']
        file = csv.writer(butter, dialect='excel')
        file.writerow(fieldnames)
        for row in listofrows:
            file.writerow(vars(row).values())



def main():
    """Parse mary full of grace... """
    with open("fullSpills.csv", 'r') as f:
        fieldnames = ["SpillNumber", "ProgramFacilityName", "Street1", "Street2", "Locality", "County", "ZIPCode",
                      "SWISCode", "DECRegion", "SpillDate", 'ReceivedDate', 'ContributingFactor', 'Waterbody', 'Source',
                      'CloseDate', 'MaterialName', 'MaterialFamily', 'Quantity', 'Units', 'Recovered']
        file = csv.DictReader(f, fieldnames=fieldnames, dialect='excel')
        file.__next__()
        line_count = 0
        parsed = []
        with open("{} USaddressErrors.csv".format(datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d %I")),
                  'w') as tt:
            tt.write("Original String, USaddress.parse() string\n")
            tt.close()
        for row in file:
            t = Goofy(row[fieldnames[0]], row[fieldnames[1]], row[fieldnames[2]], row[fieldnames[3]],
                      row[fieldnames[4]],
                      row[fieldnames[5]], row[fieldnames[6]], row[fieldnames[7]], row[fieldnames[8]],
                      row[fieldnames[9]],
                      row[fieldnames[10]], row[fieldnames[11]], row[fieldnames[12]], row[fieldnames[13]],
                      row[fieldnames[14]],
                      row[fieldnames[15]], row[fieldnames[16]], row[fieldnames[17]], row[fieldnames[18]],
                      row[fieldnames[19]], None, None)
            row['Street1'] = sub_slash(row['Street1'])
            tagged_address, address_type = usadr_tag(row["Street1"])
            if (tagged_address, address_type) != False:
                t.parsed_address = (tagged_address, address_type)
                parsed.append((tagged_address, address_type, row["County"],t))
                line_count += 1
            with open("{} GeosupportErrors.csv".format(
                    datetime.datetime.strftime(datetime.datetime.now(), "%Y_%m_%d %I")), 'w') as f:
                f.write("Tagged result from USAddress, USAddress Address Type, 'County' From Spill File,\n")
                f.write("Python-Geosupport.Geosupport.error GeosupportError message\n")

        matched = geocalls(parsed)
        WriteTo(matched)
        print("done.")
        return


main()
