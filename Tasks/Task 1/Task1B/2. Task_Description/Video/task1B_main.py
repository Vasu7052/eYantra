#classes and subclasses to import
import cv2
import numpy as np
import os

filename = 'results1B_teamid.csv'
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
    image_red = cv2.imread("Overlay_Images\\yellow_flower.png",-1)
    image_blue = cv2.imread("Overlay_Images\\pink_flower.png",-1)
    image_green = cv2.imread("Overlay_Images\\red_flower.png",-1)

#####################################################################################################
    #Write your code here!!!
#####################################################################################################

#####################################################################################################
    #sample of overlay code for each frame
    #x,y,w,h = cv2.boundingRect(current_contour)
    #overlay_image = cv2.resize(image_red,(h,w))
    #frame[y:y+w,x:x+h,:] = blend_transparent(frame[y:y+w,x:x+h,:], overlay_image)
#######################################################################################################

#################################################################################################
# DO NOT EDIT!!!
#################################################################################################
#main where the path is set for the directory containing the test images
if __name__ == "__main__":
    main(path_to_video_mp4_file_with_name)
