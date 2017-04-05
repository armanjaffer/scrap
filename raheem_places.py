from googleplaces import GooglePlaces, types, lang

YOUR_API_KEY = 'AIzaSyDTp7DLKhLED-9dejMzOfk_T4U0azDIfmA'

coord = {"lat": 38.909088, "lng": -77.042686}
google_places = GooglePlaces(YOUR_API_KEY)

def find_police(coordinates, google_pl, m_radius):
    """
    coordinates = {"lat": flt, "lng": flt}
    google_pl = API thing
    rtn = closest police place, all places, query  result
    """
    query_result = google_places.nearby_search(
        lat_lng=coord,
        radius=m_radius, types=[types.TYPE_POLICE])
    if query_result.has_attributions:
        print(query_result.html_attributions)

    closest_department, min_dist = None, 1000000000
    for place in query_result.places:
        # print (place.name)
        # print("GEOLOCATION")
        # print (place.geo_location)
        # print (place.place_id)
        dist_x = float(place.geo_location["lat"]) - coord["lat"]
        dist_y = float(place.geo_location["lng"]) - coord["lng"]
        dist = (dist_x**2 + dist_y**2)**.5
        if dist < min_dist:
            closest_department, min_dist = place, dist
        place.get_details()
        # print (place.details) # A dict matching the JSON response from Google.
        # print (place.local_phone_number)
        # print (place.international_phone_number)
        # print (place.website)
        # print (place.url)
    if query_result.has_next_page_token:
        query_result_next_page = google_places.nearby_search(
            pagetoken=query_result.next_page_token)
    return closest_department, query_result.places, query_result


result = find_police(coord, google_places, 1000)

print(result[0].local_phone_number)

# Are there any additional pages of results?

