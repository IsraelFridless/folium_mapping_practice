import os
import csv
import folium

current_dir = os.getcwd()
file_name = 'data/Electric_Vehicle_Charging_Stations.csv'
filepath = os.path.join(current_dir, file_name)

keys = ('Station Name', 'New Georeferenced Column')

def load_csv():
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            {key: row[key] for key in keys}
            for row in reader
        ]

def process_coordinates(record, coord_key):
    longitude, latitude = record[coord_key].split('(')[-1].split(')')[0].split()
    record['latitude'] = float(latitude)
    record['longitude'] = float(longitude)
    return record

def create_map(records, center_coords, zoom=9):
    stations_map = folium.Map(location=center_coords, zoom_start=zoom)
    for record in records:
        coords = (record['latitude'], record['longitude'])
        folium.Marker(coords, popup=record['Station Name']).add_to(stations_map)
    return stations_map

def main():
    center_coords = [41.5025, -72.699997]

    records = load_csv()
    processed_records = [process_coordinates(record, 'New Georeferenced Column') for record in records]
    stations_map = create_map(processed_records, center_coords)

    output_path = filepath[:-4] + '_map.html'
    stations_map.save(output_path)
    print(f"Map saved to {output_path}")

if __name__ == "__main__":
    main()
