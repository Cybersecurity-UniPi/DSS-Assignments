import os
from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS


def get_decimal_from_dms(dms, ref):
    degrees = dms[0]
    minutes = dms[1] / 60.0
    seconds = dms[2] / 3600.0

    decimal = round(degrees + minutes + seconds, 5)
    if ref in ['S', 'W']:
        decimal *= -1

    return decimal


path = r'E:/'
files_array = []
names_array = []
coords_array = []
for root, directories, file in os.walk(path):
    for file in file:
        if file.endswith(".jpg"):
            wrong_name = str(os.path.join(root, file))
            file_name = wrong_name.replace(os.sep, "/")
            files_array.append(file_name)

for x in files_array:

    print(x)

    img = Image.open(x)

    exif = img._getexif()

    if not exif:
        print("No EXIF metadata found\n")

    else:
        geotags = {}
        for (idx, tag) in TAGS.items():
            if tag == 'GPSInfo':
                if idx not in exif:
                    print("No EXIF geotagging found\n")

                for (key, val) in GPSTAGS.items():
                    if key in exif[idx]:
                        geotags[val] = exif[idx][key]

        print(geotags)
        lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])
        lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
        image_name = x.split("/")[-1]
        names_array.append(image_name)
        coords_array.append(str(lon) + "," + str(lat))
        print(lon, lat, "\n")

print(coords_array, "\n\n-----------\n\n")

kml_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml " \
             "xmlns=\"http://www.opengis.net/kml/2.2\">\n\t<Folder>\n\t\t<name>Placemarks</name>\n\t\t<description" \
             ">A list of placemarks</description>\n"
for (x, y) in zip(coords_array, names_array):
    kml_string += "\t\t<Placemark>\n"
    kml_string += "\t\t\t<name>" + y + "</name>\n"
    kml_string += "\t\t\t<description>A secret place</description>\n"
    kml_string += "\t\t\t<Point>\n"
    kml_string += "\t\t\t\t<coordinates>" + x + "</coordinates>\n"
    kml_string += "\t\t\t</Point>\n"
    kml_string += "\t\t</Placemark>\n"

kml_string += "\t</Folder>\n"
kml_string += "</kml>"
print(kml_string)
if os.path.exists("C:/Users/theas/Downloads/gps.kml"):
    os.remove("C:/Users/theas/Downloads/gps.kml")
with open("C:/Users/theas/Downloads/gps.kml", "a") as f:
    f.write(kml_string)
