# Importing the libraries
from PIL import Image
from keras.applications.vgg16 import preprocess_input
import base64
from io import BytesIO
import json
import random
import cv2
from keras.models import load_model
import numpy as np
from keras.preprocessing import image
import pickle
from mtcnn.mtcnn import MTCNN
from numpy import expand_dims


#name=input("Enter the name")
names=["name","B"]

model = load_model('facenet_keras.h5')

face_cascade=cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

class VideoCamera(object):

    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture('./input_vid/vid.mp4')
    
    def __del__(self):
        #releasing camera
        self.video.release()

    def face_extractor(self,img):

        faces = face_cascade.detectMultiScale(img, 1.3, 5)
        
        if faces is ():
            return None
        
        # Crop all faces found
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
            cropped_face = img[y:y+h, x:x+w]

        return cropped_face


    def get_frame(self):
       #extracting frames
       i=0
       while(self.video.isOpened()):

        ret, image = self.video.read()
        
        ####\
        '''

        #using detect faces function to retrive box, confidence and landmarks of faces
        results = detector.detect_faces(image)
        #if face not detected just skip the image
       
        '''
        face = self.face_extractor(image)
        print("2. Face extracted")
        #resized for FaceNet model
        #cv2.imshow('frame',image)
        #cv2.waitKey(0)
        if type(face) is np.ndarray:

            face_pixels = cv2.resize(face,(160,160))
            face_pixels = face_pixels.astype('float32')
            print("inif")
            
            mean, std = face_pixels.mean(), face_pixels.std()
            face_pixels = (face_pixels - mean) / std
            
            samples = expand_dims(face_pixels, axis=0)
            #Face embeddings collected
            yhat = model.predict(samples)
            print("3. Face Embeddings Collected")
            #Loading FaceEmbedding model file
            filename = 'finalized_model.sav'
            prediction_model = pickle.load(open(filename, 'rb'))
            
            #comparing the embeddings
            yhat_class = prediction_model.predict(yhat)
            #Retrieving the probability of the prediction
            yhat_prob = prediction_model.predict_proba(yhat)
            #print("4. Predicting class and probability done")
            
            class_index = yhat_class[0]
            #print("Index",class_index)
            class_probability = yhat_prob[0,class_index] * 100
            
            print('Prediction Probablity:%.3f' %(class_probability))
            #setting threshold based on probability
            if(class_probability>99.7):
                #print("Name:",names[class_index])
                cv2.putText(image ,names[class_index],(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                print(names[class_index])
                if(names[class_index]=="name"):
	                cv2.imwrite('./output/{}.jpg'.format(i),image)
	                i += 1
            else:
                #print("Person not matched")
                cv2.putText(image,"unknown",(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,255,0),2,cv2.LINE_AA)
                print("unknown")
                ####\
        #print("outsideif")
        #ret, jpeg = cv2.imencode('.jpg', image)
        #return jpeg.tobytes()


instance = VideoCamera()
instance.get_frame()
