#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1A_544.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,(cx,cy)):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)

def main(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 127, 255, 1)
    _, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    objectList = []

    for cnt in contours:
        shape = ""
        approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
        if len(approx) == 5:
            shape = "Pentagon"
        elif len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            shape = "Square"
        elif len(approx) == 6:
            shape = "Hexagon"
        elif len(approx) > 15:
            shape = "Circle"

        M = cv2.moments(cnt)
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])

        font = cv2.FONT_HERSHEY_SIMPLEX

        colorCode = img[cy, cx]
        color = "Not Found"

        if 127 <= colorCode[0] <= 255 and colorCode[1] == 0 and colorCode[2] == 0:
            color = "Blue"
        elif colorCode[0] == 0 and 127 <= colorCode[1] <= 255 and colorCode[2] == 0:
            color = "Green"
        elif colorCode[0] == 0 and colorCode[1] == 0 and 127 <= colorCode[2] <= 255:
            color = "Red"

        if shape is "Square":
            x11 = approx[0][0][0]
            y11 = approx[0][0][1]
            x12 = approx[1][0][0]
            y12 = approx[1][0][1]

            x21 = approx[3][0][0]
            y21 = approx[3][0][1]
            x22 = approx[2][0][0]
            y22 = approx[2][0][1]

            m1 = (y12 - y11) / (x12 - x11)
            m2 = (y22 - y21) / (x22 - x21)

            m3 = (y11 - y21) / (x11 - x21)
            m4 = (y12 - y22) / (x12 - x22)

            if m1 == m2:
                if m3 == m4:
                    shape = "Rhombus"
                else:
                    shape = "Trapezium"

        newImg = cv2.putText(img, color, (cx - 35, cy - 35), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
        newImg = cv2.putText(img, shape, (cx - 20, cy - 20), font, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
        newImg = cv2.putText(img, '(' + str(cx) + ',' + str(cy) + ')', (cx - 5, cy - 5), font, 0.4, (0, 0, 0), 1,
                             cv2.LINE_AA)

        list = []
        list.append(color)
        list.append(shape)
        list.append((cx, cy))
        writecsv(color, shape, (cx, cy))
        objectList.append(list)

    picName = path[2:7] + "output.png"
    cv2.imwrite(picName, newImg)

    return objectList


#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    mypath = '.'
    # getting all files in the directory
    onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if f.endswith(".png")]
    # iterate over each file in the directory
    for fp in onlyfiles[:]:
        # Open the csv to write in append mode
        filep = open('results1A_544.csv', 'a')
        # this csv will later be used to save processed data, thus write the file name of the image
        filep.write(fp)
        # close the file so that it can be reopened again later
        filep.close()
        # process the image
        data = main(fp)
        print data
        # open the csv
        filep = open('results1A_544.csv', 'a')
        # make a newline entry so that the next image data is written on a newline
        filep.write('\n')

        # close the file
        filep.close()
