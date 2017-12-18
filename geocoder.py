import csv
import requests

# requires fields named Address, City, State
# uses optional field called Zip Code
# if latitude and longitude are in ungeocoded file make sure they are called 'Latitude' and 'Longitude'
address_csv_in = r"C:\Users\tjohnson\Desktop\Demos\mason_demo_sites.csv"
iter_num = 0

address_csv_in = r"Z:\(G) Geographic Information Systems\GIS SUPPORT\185 - Savalot\DATA\Heat Map Sites\sal_sites_12_5_17.csv"

csvfile_out = address_csv_in.split('.csv')[0] + '_geocoded.csv'

gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
api_key = "AIzaSyDpa9FUmUBcVQwg37VRDoOs3W3JVUjaD00"

address_list = []
geocoded_address_list = []
extra_components_list = []

zip_present = False
sc_present = False
        

def read_addresses(ungeocoded_addresses_file):
    global address_list
    global extra_components_list
    global zip_present
    global sc_present
    with open(ungeocoded_addresses_file, 'r') as csv_in:
        reader = csv.DictReader(csv_in)
        
        if 'Zip Code' in reader.fieldnames:
            zip_present = True
        if 'Shopping Center' in reader.fieldnames:
            sc_present = True
        if 'Site' in reader.fieldnames:
            site = True
        
        
        for row in reader:
            if site is True:
                address_list.append(row['Site'].split(','))
            else:
                if zip_present and sc_present:
                    address_components_list = [row['Shopping Center'].strip(), row['Address'].strip(), row['City'].strip(), row['State'].strip(), row['Zip Code'].strip()]
                elif zip_present:
                     address_components_list = [row['Address'].strip(), row['City'].strip(), row['State'].strip(), row['Zip Code'].strip()]
                elif sc_present:
                    address_components_list = [row['Shopping Center'].strip(), row['Address'].strip(), row['City'].strip(), row['State'].strip()]
                    
                address_list.append(address_components_list)

       
def google_maps_geocode(address):
    address2 = ", ".join(address)
    address3 = address2.replace(" ", "%20")
    print(address3)
    #print(address3)
    r = requests.get(gmap_url + "address=" + address3 + "&key=" + api_key)
    print(gmap_url + "address=" + address3 + "&key=" + api_key)
    rj = r.json()
    #print(rj)
    street_address = city = state = zip_code = ""
    
    for item in rj['results'][0]['address_components']:
        if item['types'][0] == 'street_number':
            index = rj['results'][0]['address_components'].index(item)
            street_address = item['long_name'] + ' ' + rj['results'][0]['address_components'][index + 1]['long_name']
        if item['types'][0] == 'locality':
            city = item['long_name']
        if item['types'][0] == 'administrative_area_level_1':
            state = item['short_name']
        if item['types'][0] == 'postal_code':
            zip_code = item['long_name']
    full_address = rj['results'][0]['formatted_address']
    full = full_address.rsplit(',', 1)[0]
    lat = rj['results'][0]['geometry']['location']['lat']
    lng = rj['results'][0]['geometry']['location']['lng']
    accuracy = rj['results'][0]['geometry']['location_type']
            
    if zip_present and sc_present:
        addresses_component_list = address + [address[0] + ', ' + full, lat, lng, accuracy]
    elif zip_present:
        addresses_component_list = address + [full, lat, lng, accuracy] 
    elif sc_present:
        addresses_component_list = address + [zip_code, address[0] + ', ' + full, lat, lng, accuracy]
    else:
        addresses_component_list = address + [zip_code, full, lat, lng, accuracy] 
        
    geocoded_address_list.append([addresses_component_list])
            
    try:
        print(rj['results'][0]['address_components'][0]['long_name'] + ' ' + rj['results'][0]['address_components'][1]['long_name'])
        print(rj['results'][0]['address_components'][2]['long_name'])
        print(rj['results'][0]['address_components'][4]['short_name'])
        print(rj['results'][0]['address_components'][6]['long_name'])
        print(rj['results'][0]['formatted_address'])
        print(rj['results'][0]['geometry']['location']['lat'])
        print(rj['results'][0]['geometry']['location']['lng'])
        print(rj['results'][0]['geometry']['location_type'])
        print()
    except:
        pass
    
    
def write_to_file(geocoded_addresses):
    global sc_present
    global zip_present
    with open(csvfile_out, 'w', newline='') as outcsv:   
        writer = csv.writer(outcsv, delimiter=',')
        if sc_present:
            writer.writerow(['Shopping Center','Address', 'City', 'State', 'Zip Code', 'Full Address', 'Latitude', 'Longitude', 'Accuracy'])
        elif zip_present:
            writer.writerow(['Address', 'City', 'State', 'Zip Code', 'Full Address', 'Latitude', 'Longitude', 'Accuracy'])
        
        for item in geocoded_addresses:
            writer.writerows(item)
            
            
def run(number=0):
    global address_list
    if number == 0:
        read_addresses(address_csv_in)
        for item in address_list:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)
    else:
        read_addresses(address_csv_in)
        for item in address_list[:number]:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)
        
        
if __name__ == '__main__':
    run(iter_num)
