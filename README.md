# Project Title
SmartHouse - A mobile app combine with Paradrop smart router, a webcam, and a LED bulb that forms an IOT prototype.

## How to train face-recognition classifier
0. Put the photos used as training instances to LocalPath/training-images, where LocalPath is an user-specified path in the user's machine/router. Note that under LocalPath/training-images, users must create a folder for each person, and group all the photos accordingly. For example, if there are two people, namely P1 and P2, then the structure should look like this:
```
+ LocalPath/training-images/P1/*.jpg
+ LocalPath/training-images/P2/*.jpg
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
+ ./demos/classifier_multi.py train ./generated-embeddings/
```

7. Copy the trained classfiers to the chute
```
+ cp -f ./generated-embeddings/*.pkl /link/LocalPath/Openface-on-Paradrop/chute/.
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
