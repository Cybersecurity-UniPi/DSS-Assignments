import glob
import os
import simplekml
import PIL.Image
from PIL import Image

path_to_disk = '/home/jackson/Desktop/DSS/DSS-Assignments/2/mount/'
metadata_tag = 34853  # Metadata with coordinates
result_dict = dict()


def dms_to_decimal(cardinal_point: str, dms_value: tuple):
    degree = dms_value[0]
    minutes = dms_value[1] / 60.0
    seconds = dms_value[2] / 3600.0

    decimal = degree + minutes + seconds
    if cardinal_point == 'S' or cardinal_point == 'W':
        decimal *= -1

    return decimal


def extract_metadata(full_path: str):
    img: PIL.Image.Image = Image.open(full_path)
    exifmetadata = img._getexif()
    if exifmetadata:
        if metadata_tag in exifmetadata:
            geo_info = exifmetadata[metadata_tag]
            result_dict[full_path] = [
                # Latitude
                dms_to_decimal(cardinal_point=geo_info[1], dms_value=geo_info[2]),
                # Longitude
                dms_to_decimal(cardinal_point=geo_info[3], dms_value=geo_info[4])
            ]


if __name__ == '__main__':
    result = []
    for x in os.walk(path_to_disk):
        for y in glob.glob(os.path.join(x[0], '*.jpg')):
            try:
                extract_metadata(y)
            except Exception as e:
                pass

    kml = simplekml.Kml()
    for key in result_dict:
        vett = result_dict[key]
        kml.newpoint(description=key, coords=[(vett[1], vett[0])])
    kml.save("output.kml")
