import cv2
import os
from PIL import Image

face_cascade = cv2.CascadeClassifier('./cascade/haarcascade_frontalface_default.xml')

def image_processing(filename, expected_size = False):
    print('[INFO] Processing ' + str(filename) + ' image')
    # Set Stpre Path
    baseStorePath = './images/cropped/'
    baseStorePath = baseStorePath + str(filename.split('.')[0]) + '/'
    os.mkdir(baseStorePath)

    # Tracking Faces Position
    base_image = cv2.imread('./images/' + str(filename))
    move_center_point = 5 # Tracking Center Point Move With Percent
    img = cv2.cvtColor(base_image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img, 1.1, 5)

    for index, (x, y, w, h) in enumerate(faces):
        storePath = baseStorePath
        if len(faces) > 1:
            storePath = baseStorePath + str( (index + 1) ) + '/'
            os.mkdir(storePath)
        
        img_height, img_width = img.shape

        if expected_size:
            expected_width, expected_height = expected_size
            crop_ratio = int(expected_width) / int(expected_height)
            img_height = int(img_width / crop_ratio)
    

        if img_width > img_height:
            print("[ERROR] " + filename + " can't crop landscape image")
            return False

        center_tracking_x = x + int((x+w - x) / 2) + 30
        center_tracking_y = y + int((y+h - y) / 2) + 40

        center_tracking_y = int(center_tracking_y + (center_tracking_y * (move_center_point/100)))

        x1 = int(center_tracking_x + (img_width/4)) 
        y1 = int(center_tracking_y + (img_height/4)) 
        x2 = int(center_tracking_x - (img_width/4)) 
        y2 = int(center_tracking_y - (img_height/4)) 

        im = Image.fromarray(cv2.cvtColor(base_image, cv2.COLOR_BGR2RGB))
        
        if expected_size:
            im.crop((x2, y2, x1, y1)).resize((int(expected_width), int(expected_height))).save(storePath + str(filename), dpi=(300,300))
        else:
            im.crop((x2, y2, x1, y1)).save(storePath + str(filename), dpi=(300,300))

        print('[SUCCESS] Finished Processing ' + str(filename) + ' image')


print('[INFO] Service is started!')
image_basepath = './images/'

try:
    list_dir = os.listdir(image_basepath)
except Exception as e:
    if str(e).find('WinError 3'):
        print('[ERROR] Please move all images to "images" folder')
        os.mkdir(image_basepath)
        os.mkdir(image_basepath + 'cropped/')
        exit()
    else:
        print('[ERROR] Unhandled Error ' + str(e))
        exit()

for item in list_dir:
    itemPath = image_basepath + str(item)
    if os.path.isfile(itemPath):
        if( item.lower().endswith(('.jpg', '.png', '.bmp'))):
            # Process Image
            image_processing(item, (354.330708661, 472.440944882))


# Checking For Empty Folder
list_dir = os.listdir(image_basepath + 'cropped/')
for folder in list_dir:
    checked_dir_path = image_basepath + 'cropped/' + str(folder) + '/'
    if( len(os.listdir(checked_dir_path)) < 1 ):
        print('[WARNING] Empty Folder Found, ' + str(folder))

print('[INFO] Service finished')