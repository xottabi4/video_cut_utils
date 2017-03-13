import os
import xml.etree.ElementTree as ET


def main():
    txtname = 'train.txt'
    with open(txtname, 'r') as f:
        image_names = [x.strip() for x in f.readlines()]

    for image_name in image_names:
        filename = os.path.join('input_images_roi', image_name + '.xml')
        tree = ET.parse(filename)
        root = tree.getroot()
        bounding_boxes = root.findall('boundingBox')
        if bounding_boxes is None:
            print image_name + " is has no boundingBox"
        for bounding_box in bounding_boxes:
            if bounding_box.find('w') is None:
                print image_name + " is has no empty x"
            if bounding_box.find('w').text == "":
                print image_name + " is has empty x element"


if __name__ == '__main__':
    main()
