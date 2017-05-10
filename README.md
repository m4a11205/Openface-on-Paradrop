# SmartHouse for Paradrop
"SmartHouse" is a system combine with Paradrop smart router, a webcam, a SONOS speaker and a Flux LED bulb that forms an IoT prototype. It cantains a Paradrop chute and a mobile app. The following features has been developed so far:
  * Real-time Video Stream
  * Take photo of the video stream
  * LED Light switching
  * Change the color of LED
  * Change the brightness of LED
  * Play different music according to the results of facial recognition

## Requirements:
Wireless security cam that can connect to the Paradrop router. Sonos wireless speaker. FluxSmart WiFi LED Light Bulb.

## Description:
The concept of smart home developed rapidly. However, massive types of control protocols make it difficult to combine devices together for a cooperative work. In this case, Paradrop would provides a secure and smart way to coordinate multiple devices.  
We build a Paradrop chute that could control wireless camera, a led bulb and a wireless speaker through a mobile app. This chute also embedded a Openface lib.  

##Files

Dockerfile: load docker image
seccam.py: Takes in three arguments for caliberation, time and sensitivity. According to these parameter, the security camera takes pictures each time it detects motion and saves it on the router for future reference.  
LedControl.py: control led bulb  
smarthouse.py: main file, initialize default settings, get connection to speaker, led bulb and camera  
socoControl.py: control SONOS speaker  
test_soco.py  
run.sh  
face_classifier.py: run face recognition alogrithm  
haarcascade_frontalface_default.xml  
multi.py: multi-classifier for a majority vote of the recognition result  
Forest.pkl: Random forests ensemble learning method for classification, regression  
GaussianNB.pkl: Gaussian Naive Bayes classifiers  
LinearSvm.pkl: Linear Support vector machine classifiers  
Logic.pkl:Inductive logic programming classifiers  
RadialSvm.pkl: Radial Support vector machine classifiers  
classifier.pkl: Default classifier is linear SVM  
##ports exposed:  
80  
81  
8000  
8010  
8011: Camera  
8012: Led bulb  
8013  
8014  
8015: SONOS speaker  
8500  
9000  
## Getting started


## How to train face-recognition classifier
0. Put the photos used as training instances to LocalPath/training-images, where LocalPath is an user-specified path in the user's machine/router. Note that under LocalPath/training-images, users must create a folder for each person, and group all the photos accordingly. For example, if there are two people, namely P1 and P2, then the structure should look like this:
```
 LocalPath/training-images/P1/*.jpg
 LocalPath/training-images/P2/*.jpg
```

1. Pull and download the docker image
```
docker pull m4a11205/paradrop-smartbase-multi
```

2. Run the docker container
```
docker run -v /LocalPath:/link/LocalPath -p 9000:9000 -p 8000:8000 -t -i m4a11205/paradrop-smartbase-multi /bin/bash
```

3. Change directory to openface library
```
cd /root/openface
```

4. Crop and generate the aligned images for each training instances
```
./util/align-dlib.py /link/LocalPath/training-images/ align outerEyesAndNose ./aligned-images/ --size 96
```

5. Extract the face features for machine learning classification
```
./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/
```

6. Train the machine learning classifiers
```
./demos/classifier_multi.py train ./generated-embeddings/
```

7. Copy the trained classfiers to the chute
```
cp -f ./generated-embeddings/*.pkl /link/LocalPath/Openface-on-Paradrop/chute/.
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
