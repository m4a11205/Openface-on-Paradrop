import cv2
import sys

try:
    import PIL
    from PIL import Image, ImageChops
except Exception as e:
    print('No PIL, please install "python-imaging-library" if on OpenWrt')
    sys.exit(1)

if __name__ == "__main__":
    print("Loaded OpenCV version: {}".format(cv2.__version__))

    # Get user supplied values
    imagePath = sys.argv[1]
    cascPath = sys.argv[2]

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Read the image
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    fileName = "test.jpg"
    print('jpg: %s' % str(fileName))
    image = cv2.imwrite(fileName, image)