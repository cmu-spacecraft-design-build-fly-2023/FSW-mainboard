# Testing script for the UART communication with the payload 

import sys
import time
import gc

from apps.data_handler import DataHandler as DH


for path in ["/hal", "/apps"]:
    if path not in sys.path:
        sys.path.append(path)



# Just for debug purposes - need initial SD card scan
print("SD Card Directories: ", DH.list_directories())
DH.delete_all_files()
DH.scan_SD_card()


## Put Jetson Code here 
DH.register_image_process()


# Define messages to send to the payload (for testing purposes) HERE

end_img = False

def data_available(): # temporary fct for data_available
    return True

while True:

    if data_available(): # Put here the condition to check if there is an image to send
        
        # All reading/writing code here 
        
        # img_bytes = # INSERT here 
        # DH.log_image(img_bytes)

        if end_img:
            DH.image_completed()






























