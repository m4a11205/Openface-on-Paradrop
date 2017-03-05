import cv2, os
import numpy as np
from sklearn import tree, metrics

try:
    import PIL
    from PIL import Image, ImageChops
except Exception as e:
    print('No PIL, please install "python-imaging-library" if on OpenWrt')
    sys.exit(1)

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)


def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')

        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')

        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))

        # Detect the face in the image
        faces = faceCascade.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            #faceArea = image[y: y + h, x: x + w]
            faceArea = image
            images.append(faceArea)
            labels.append(nbr)

    # return the images list and labels list
    return images, labels

if __name__ == "__main__":
    print("Loaded OpenCV version: {}".format(cv2.__version__))

    # Path to the Yale Dataset
    path = './yalefaces'

    # Call the get_images_and_labels function and get the face images and the
    # corresponding labels
    images, labels = get_images_and_labels(path)

    features = []
    for img in images:
        features.append(img.ravel())

    clf = tree.DecisionTreeClassifier()
    clf.fit(features, labels)

    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
    for image_path in image_paths:
        predict_image_pil = Image.open(image_path).convert('L')
        predict_image = np.array(predict_image_pil, 'uint8')

        faces = faceCascade.detectMultiScale(
            predict_image,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        for (x, y, w, h) in faces:
            nbr_predicted = clf.predict(predict_image.reshape(1, -1))
            nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
            if nbr_actual == nbr_predicted:
                print "{} is Correctly Recognized".format(nbr_actual)
            else:
                print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
