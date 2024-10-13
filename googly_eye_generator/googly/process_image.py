import cv2
import numpy as np
from mtcnn import MTCNN
from typing import List
import time


class Model:
    """
    This class is used to get the detections using the MTCNN model, create googly eyes and overlay on original image
    """
    def __init__(self):

        self.time_dict = {}
        self.detector = MTCNN()



    def create_googly_eye(self, eye_rad_ht: int = 0, eye_rad_wt: int = 0, pupil_radius: int = 0, center: List[int] = None) -> np.ndarray:
        """
            This function is used to create the googly eye based on the eye dimensions
        """
        # Create a blank image with a transparent background
        eye_radius = min(eye_rad_ht,eye_rad_wt)
        googly_eye = np.zeros((eye_rad_ht*2, eye_rad_wt*2, 4), dtype=np.uint8)
        pupil_eye = np.zeros((eye_rad_ht*2, eye_rad_wt*2, 4), dtype=np.uint8)

        # Draw the white part of the eye
        cv2.circle(googly_eye, (googly_eye.shape[1]//2,googly_eye.shape[0]//2), eye_radius, (225, 225, 225, 255), -1)
        try:
            # For some shadow on the corner of the eye
            cv2.circle(googly_eye, (googly_eye.shape[1]//2,googly_eye.shape[0]//2), eye_radius-1, (192, 192, 192, 255), 1)
        except:
            print('Cannot draw shadow')

        # Get pupil radius randomly based on eye size
        pupil_x = np.random.randint((googly_eye.shape[1]//2) *0.8, (googly_eye.shape[1]//2) * 1.3)
        pupil_y = np.random.randint((googly_eye.shape[0]//2) *0.8, (googly_eye.shape[0]//2) * 1.3)
        # Get the pupil radius randomly such that its inside the white iris
        pupil_radius_changed = np.random.randint(pupil_radius*0.8,pupil_radius*1.2)

        # Draw the black part
        cv2.circle(pupil_eye,(pupil_x, pupil_y), pupil_radius_changed,(0,0,0,255),-1)
        try:
            # For some shadow around the pupil
            cv2.circle(pupil_eye,(pupil_x, pupil_y), pupil_radius_changed-3,(50,50,50,255),3)
        except:
            print('Cannot draw shadow')

        # Overlapping black pupil on white iris
        for i in range(googly_eye.shape[0]):
            for j in range(googly_eye.shape[1]):
                if googly_eye[i, j][3] != 0:  # Check alpha channel       
                    if (0 <=  i < googly_eye.shape[0]) and (0 <= j < googly_eye.shape[1]) and pupil_eye[i,j][3] != 0:
                            googly_eye[i,j] = pupil_eye[i,j]

        return googly_eye

    def get_output(self, image: np.ndarray) -> np.ndarray:
        """
            This function gets input from the API and detects teh eyes using MTCNN model and places the 
            googly eyes on the original image
        """
        # Read Image
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Detect faces and their landmarks
        detections = self.detector.detect_faces(rgb_image, threshold_pnet=0.7)

        for detection in detections:
            # Get the bounding box and keypoints (eyes) from the detection
            x, y, width, height = detection['box']
            keypoints = detection['keypoints']

            # Get eye positions from keypoints
            left_eye = keypoints['left_eye']
            right_eye = keypoints['right_eye']
            
            # Getting the width and height of the eyes from the size of the face bounding box
            googly_eye_width, googly_eye_height = (width*0.20) , (height*0.20)

            for eye in [left_eye, right_eye]:

                # Calculate the googly eyes height and width
                eye_rad_ht = np.random.randint(googly_eye_height-4,googly_eye_height-1)
                eye_rad_wt = np.random.randint(googly_eye_width-4,googly_eye_width-1)
            
                pup_rad = googly_eye_width//2
                # Create googly eyes based on the face box dimension
                googly_eye_image = self.create_googly_eye(eye_rad_ht,eye_rad_wt,pup_rad,eye)
                eye_x = eye[0]-googly_eye_image.shape[1]//2
                eye_y = eye[1]-googly_eye_image.shape[0]//2

                # Overlay the created googly eye on the face based on the eye center
                for i in range(googly_eye_image.shape[0]):
                    for j in range(googly_eye_image.shape[1]):
                        if googly_eye_image[i, j][3] != 0:  # Check alpha channel
                            
                            if (0 <= eye_y + i < image.shape[0]) and (0 <= eye_x + j < image.shape[1]):
                                image[eye_y + i, eye_x + j] = googly_eye_image[i, j][:3]

        return image
