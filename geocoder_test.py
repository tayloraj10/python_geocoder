import csv
import requests

# requires fields named Address, City, State
# uses optional field called Zip Code
# if latitude and longitude are in ungeocoded file make sure they are called 'Latitude' and 'Longitude'
address_csv_in = r"C:\Users\tjohnson\Desktop\Demos\mason_demo_sites.csv"

csvfile_out = address_csv_in.split('.csv')[0] + '_geocoded.csv'

gmap_url = "https://maps.googleapis.com/maps/api/geocode/json?"
api_key = "AIzaSyDpa9FUmUBcVQwg37VRDoOs3W3JVUjaD00"

addresses = ["307 Fellowship Rd, Mt Laurel, NJ 08054",
             "300 Aspen Ct., Hanover, PA 17331"]

address_list = []
geocoded_address_list = []
extra_components_list = []


def read_addresses(ungeocoded_addresses_file):
    zip_present = False
    with open(ungeocoded_addresses_file, 'r') as csv_in:
        reader = csv.DictReader(csv_in)
        for row in reader:
            try:
                address_components_list = [row['Address'], row['City'], row['State'], row['Zip Code']]
                zip_present = True
            except:
                address_components_list = [row['Address'], row['City'], row['State']]
            address_list.append(address_components_list)
            if zip_present:
                try:
                    join_list = []
                    extra_components_list = [", ".join(address_components_list), row['Latitude'], row['Longitude']]
                except:
                    extra_components_list = [", ".join(address_components_list)]
            else:
                try:
                    extra_components_list = [", ".join(address_components_list), row['Latitude'], row['Longitude']]
                except:
                    extra_components_list = [", ".join(address_components_list)]


def google_maps_geocode(address):
    address2 = ", ".join(address)
    address2 = address2.replace(" ", "%20")
    # print(address2)
    r = requests.get(gmap_url + "address=" + address2 + "&key=" + api_key)
    rj = r.json()
    # print(rj)
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
    lat = rj['results'][0]['geometry']['location']['lat']
    lng = rj['results'][0]['geometry']['location']['lng']
    accuracy = rj['results'][0]['geometry']['location_type']

    addresses_component_list = [street_address, city, state, zip_code, full_address, lat, lng, accuracy]
    geocoded_address_list.append([addresses_component_list])
    geocoded_address_list.append([extra_components_list])

    print(rj['results'][0]['address_components'][0]['long_name'] + ' ' + rj['results'][0]['address_components'][1][
        'long_name'])
    print(rj['results'][0]['address_components'][2]['long_name'])
    print(rj['results'][0]['address_components'][4]['short_name'])
    print(rj['results'][0]['address_components'][6]['long_name'])
    print(rj['results'][0]['formatted_address'])
    print(rj['results'][0]['geometry']['location']['lat'])
    print(rj['results'][0]['geometry']['location']['lng'])
    print(rj['results'][0]['geometry']['location_type'])
    print()


def write_to_file(geocoded_addresses):
    with open(csvfile_out, 'w', newline='') as outcsv:
        writer = csv.writer(outcsv, delimiter=',')
        writer.writerow(['Address', 'City', 'State', 'Zip Code', 'Full Address', 'Latitude', 'Longitude', 'Accuracy',
                         'Original Address', 'Original Latitude', 'Original Longitude'])
        for item in geocoded_address_list:
            writer.writerows(item)


def run(number=0):
    if number == 0:
        read_addresses(address_csv_in)
        for item in address_list:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)
    else:
        read_addresses(address_csv_in)
        for item in address_list[:number + 1]:
            google_maps_geocode(item)
        write_to_file(geocoded_address_list)


if __name__ == '__main__':
    run()
