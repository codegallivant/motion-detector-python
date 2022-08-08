import cv2
from PIL import Image
from PIL import ImageChops
import math, operator
from functools import reduce

    
class MotionDetector:

    def __init__(self):
        self.current_movement = None
        self.stop_demand = False
        self.cam_port = 0
        self.max_rms_diff = 7 #Number found by trial & error. Even with no movement, camera pictures may keep changing minutely. Hence rms difference is calculated. After some trial and error I found that with the camera I'm using, a suitable boundary for rms diff between almost same pictures is 7.
            

    def configure(self, cam_port = None, max_rms_diff = None):
        if cam_port != None:
            self.cam_port = cam_port
        if max_rms_diff != None:
            self.max_rms_diff = max_rms_diff        
    

   
    def start(self, callback=None):
        # Functions to help check similarity of images captured


        def rmsdiff(im1, im2): #Calculate the root-mean-square difference between two images
            h = ImageChops.difference(im1, im2).histogram()
            # calculate rms
            return math.sqrt(reduce(operator.add,
                map(lambda h, i: h*(i**2), h, range(256))
            ) / (float(im1.size[0]) * im1.size[1]))


        def check_similarity(image_1, image_2):
            diff = rmsdiff(image_1, image_2)
            return diff <= self.max_rms_diff


        # Continuously capturing pictures and calling functions to compare consecutive captures, then taking action depending on similarity
        first = True
        i=0
        d=[0,1]
        
        self.cam = cv2.VideoCapture(self.cam_port)

        while self.stop_demand is False:            

            result, frame =  self.cam.read()
            
            if result is False:
                raise Exception
                
            d[i%2] = frame
            if first is False:
                if check_similarity(Image.fromarray(d[0]),Image.fromarray(d[1])) is False:
                    self.current_movement = True
                    if callback != None:
                        callback()  
                        break         
                else:
                    self.current_movement = False
            # time.sleep(0.01)
            i=i+1
            i=i%2
            first = False



    def stop(self):
        self.stop_demand = True
        self.cam.release()
        self.current_movement = None
        self.stop_demand = False



