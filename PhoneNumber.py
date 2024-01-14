import sys
import subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "phonenumbers"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "folium"])
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencage"])

import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode

class PhoneNumber:

    def __init__(self, phone_number):
        self.number = phone_number
        
    # Parsing the phone number string to convert it into phone number format
    def location_and_provider(self):
        phone_number = phonenumbers.parse(self.number)

        # Using the geocoder module of phonenumbers to get the location and returning it
        your_location = geocoder.description_for_number(phone_number,"en") 
        
        # Using the carrier module of phonenumbers to print the service provider name in console
        your_service_provider = carrier.name_for_number(phone_number,"en")
        return your_location, your_service_provider
    
    # Parsing the phone number string to convert it into phone number format
    def map_location(self):
        # Using the geocoder module of phonenumbers to get the location
        your_location  = self.location_and_provider()[0]
        
        # Using opencage to get the latitude and longitude of the location
        key = "af1c55430bc8444983f02e6e3746d4c5"
        geocoder = OpenCageGeocode(key)
        results = geocoder.geocode(your_location)

        # Assigning the latitude and longitude values to the lat and lng variables
        lat = results[0]['geometry']['lat'] # type: ignore
        lng = results[0]['geometry']['lng'] # type: ignore

        # Getting the map for the given latitude and longitude
        my_map = folium.Map(location=[lat, lng], zoom_start=9)

        # Adding a marker on the map to show the location name
        folium.Marker([lat, lng], popup=your_location).add_to(my_map)

        # save map to html file to open it and see the actual location in map format
        my_map.save("Location.html")
        return lat,lng
        

