import os
import xml.etree.ElementTree as ET

import cv2


def main():
    cap = cv2.VideoCapture("input_images/output_%04d.png")

    # input_image = cv2.imread("input_images/output_0001.png")
    # input_image = cv2.resize(input_image, (640, 360))
    background = cv2.imread("background/background.png")
    # background = cv2.resize(background, (640, 360))

    background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
    # fgbg = cv2.createBackgroundSubtractorMOG2()

    image_name_filename = "train.txt"
    try:
        os.remove(image_name_filename)
    except OSError:
        pass
    image_name_file = open(image_name_filename, "w")

    while True:
        # frame = input_image
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # frame = cv2.resize(frame, (640, 360))

        foreground = cv2.absdiff(frame, background)
        _, foreground_treshed = cv2.threshold(foreground, 15, 255, cv2.THRESH_BINARY)
        image, contours, hierarchy = cv2.findContours(foreground_treshed, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            idx_largest_contour = -1
            area_largest_contour = 0.0
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contours[i])
                if area_largest_contour < area:
                    area_largest_contour = area
                    idx_largest_contour = i
            if area_largest_contour > 200:
                # Let (x,y) be the top-left coordinate of the rectangle and (w,h) be its width and height.
                x, y, w, h = cv2.boundingRect(contours[idx_largest_contour])
                # frame = cv2.drawContours(frame, contours, idx_largest_contour, (0, 0, 255))
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                save_roi_to_xml_file(x, y, w, h, int(cap.get(cv2.CAP_PROP_POS_FRAMES)), image_name_file)

        cv2.imshow('frame', frame)
        cv2.imshow('mask(foreground)', foreground_treshed)

        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
    image_name_file.close()


def save_roi_to_xml_file(x, y, w, h, image_number, image_name_file):
    data_path = "input_images_roi/"
    filename = "output_" + "{:04d}".format(image_number)
    image_name_file.write(filename + "\n")

    full_filename = os.path.join(data_path, filename + ".xml")
    try:
        os.remove(full_filename)
    except OSError:
        pass

    print filename
    root = ET.Element("boundingBoxes")
    bounding_box = ET.SubElement(root, "boundingBox")
    ET.SubElement(bounding_box, "x").text = str(x)
    ET.SubElement(bounding_box, "y").text = str(y)
    ET.SubElement(bounding_box, "w").text = str(w)
    ET.SubElement(bounding_box, "h").text = str(h)
    tree = ET.ElementTree(root)
    tree.write(full_filename)


if __name__ == '__main__':
    main()
