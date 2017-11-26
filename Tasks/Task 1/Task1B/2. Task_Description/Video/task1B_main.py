#classes and subclasses to import
import cv2
import numpy as np
import os
import time

filename = 'results1B_544.csv'
#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#subroutine to write results to a csv
def writecsv(color,shape,cx,cy):
    global filename
    #open csv file in append mode
    filep = open(filename,'a')
    # create string data to write per image
    datastr = "," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    #write to csv
    filep.write(datastr)
    filep.close()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
def blend_transparent(face_img, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (face_img * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))


def main(video_file_with_path):
    cap = cv2.VideoCapture(video_file_with_path)
    out = cv2.VideoWriter('videooutput.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30, (1280, 720))

    image_red = cv2.imread("Overlay_Images/yellow_flower.png",-1)
    image_blue = cv2.imread("Overlay_Images/pink_flower.png",-1)
    image_green = cv2.imread("Overlay_Images/red_flower.png",-1)

    dictionary = {}
    count = 1


    while (cap.isOpened()):
        ret, frame = cap.read()

        if ret is True :

            img = frame
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, thresh = cv2.threshold(gray, 127, 255, 1)
            _, contours, h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

                colorCode = img[cy, cx]
                color = "Not Found"

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
                    else:
                        shape = "Trapezium"

                if colorCode[0] == 254 and colorCode[1] == 0 and colorCode[2] == 0:
                    color = "Blue"
                    temp = img[cy-100:cy+100,cx-100:cx+100]
                    resized_image = cv2.resize(image_blue, (200, 200))
                    result = blend_transparent(temp,resized_image)
                    img[cy - 100:cy + 100, cx - 100:cx + 100] = result
                    if (str(cx)+","+str(cy)) in dictionary.values():
                        pass
                    else:
                        dictionary[str(count)] = str(cx) + "," + str(cy)
                        count += 1
                        writecsv(color,shape,cx,cy)
                elif colorCode[0] == 0 and colorCode[1] == 127 and colorCode[2] == 0:
                    color = "Green"
                    temp = frame[cy - 100:cy + 100, cx - 100:cx + 100]
                    resized_image = cv2.resize(image_green, (200, 200))
                    result = blend_transparent(temp, resized_image)
                    img[cy - 100:cy + 100, cx - 100:cx + 100] = result
                    if (str(cx)+","+str(cy)) in dictionary.values():
                        pass
                    else:
                        dictionary[str(count)] = str(cx) + "," + str(cy)
                        count += 1
                        writecsv(color,shape,cx,cy)
                elif colorCode[0] == 0 and colorCode[1] == 0 and colorCode[2] == 254:
                    color = "Red"
                    temp = frame[cy - 100:cy + 100, cx - 100:cx + 100]
                    resized_image = cv2.resize(image_red, (200, 200))
                    result = blend_transparent(temp, resized_image)
                    img[cy - 100:cy + 100, cx - 100:cx + 100] = result
                    if (str(cx)+","+str(cy)) in dictionary.values():
                        pass
                    else:
                        dictionary[str(count)] = str(cx) + "," + str(cy)
                        count += 1
                        writecsv(color,shape,cx,cy)


            cv2.imshow('frame', frame)


            if cv2.waitKey(30) & 0xFF == ord('q'):
                break

            out.write(frame)

        else:
            break



    cap.release()
    out.release()
    cv2.destroyAllWindows()

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main("Video.mp4")
