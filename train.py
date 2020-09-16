import os
import cv2
import numpy as np
from PIL import Image

def face_train():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    faces = []
    ids = []

    def getImagesAndLabels(path):

        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []

        for imagePath in imagePaths:

            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')

            id = int(path.split('.')[2])
            face = detector.detectMultiScale(img_numpy)

            for (x, y, w, h) in face:
                faces.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)

    print("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    for p_path in os.listdir('./dataset'):
        getImagesAndLabels('./dataset/' + p_path)

    if ids:
        recognizer.train(faces, np.array(ids))
        recognizer.write('trainer/trainer.yml')
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    else:
        print("\n [INFO] No face found.")
        return -1
    return 1


if __name__ == "__main__":
    face_train()
