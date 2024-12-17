import csv
import folium
import toolz as t

filepath = r'C:\Users\Python\final_exam_preparation\folium_mapping_practice\app\data\Electric_Vehicle_Charging_Stations.csv'
keys = ('Station Name', 'New Georeferenced Column')

def load_csv():
    with open(filepath, 'r') as csvfile:
        readr = csv.DictReader(csvfile)
        return list(map(lambda row: {key: row[key] for key in keys}, readr))


@t.curry
def process_coordinates(record, coord_key):
    longitude, latitude = record[coord_key].split('(')[-1].split(')')[0].split()
    record['latitude'] = float(latitude)
    record['longitude'] = float(longitude)
    return record


def create_map(records, center_coords, zoom=9):
    stations_map = folium.Map(location=center_coords, zoom_start=zoom)
    for record in records:
        coords = (t.get('latitude', record), t.get('longitude', record))
        folium.Marker(coords, popup=record['Station Name']).add_to(stations_map)
    return stations_map


def main():
    center_coords = [41.5025, -72.699997]

    stations_map = t.pipe(
        load_csv(),
        t.partial(map, process_coordinates(coord_key='New Georeferenced Column')),
        list,
        lambda records: create_map(records, center_coords)
    )

    output_path = filepath[:-4] + '_map.html'
    stations_map.save(output_path)
    print(f"Map saved to {output_path}")


if __name__ == "__main__":
    main()