"Dylan Murphy 2018-08-16"

import geosupport
def main():

    g = geosupport.Geosupport()
    spills="1 2	FIFTH AVENUE"
    result= g.call(function=1, house_number=2, borough_code= 1, street_name_1= "Fifth Ave")
    print(result)

main()