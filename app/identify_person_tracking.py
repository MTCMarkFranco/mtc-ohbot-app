import cv2
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import dlib
import math

# Initialize video capture
cap = cv2.VideoCapture(0)

# Functions
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = math.dist(eye[1], eye[5])
    B = math.dist(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = math.dist(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear


# Initialize dlib's face detector and create a predictor
EYE_AR_THRESH = 0.3
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("recognition_models\\shape_predictor_68_face_landmarks.dat")

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the image to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = detector(gray, 0)

    # Loop over the face detections
    for face in faces:
        # Determine the facial landmarks for the face region
        x1 = face.left()  # left point
        y1 = face.top()  # top point
        x2 = face.right()  # right point
        y2 = face.bottom()  # bottom point

        # Create landmark object
        landmarks = predictor(image=gray, box=face)
        
        # Initialize lists to hold eye coordinates
        left_eye = []
        right_eye = []

        # Loop through all the points
        for n in range(36, 42):  # Loop for left eye
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            left_eye.append((x, y))

        for n in range(42, 48):  # Loop for right eye
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            right_eye.append((x, y))

        # Calculate the Eye Aspect Ratio for both eyes
        leftEAR = eye_aspect_ratio(left_eye)
        rightEAR = eye_aspect_ratio(right_eye)

        # Average the eye aspect ratio together for both eyes
        ear = (leftEAR + rightEAR) / 2.0

        # If the eye aspect ratio is below a certain threshold, consider that the eyes are closed
        if ear < EYE_AR_THRESH:
            print('The person is not looking at the camera')
        else:
            print('The person is looking at the camera')

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
