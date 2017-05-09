# Project Title
SmartHouse - A mobile app combine with Paradrop smart router, a webcam, and a LED bulb that forms an IOT prototype.

## How to train face-recognition classifier

1. Pull and download the docker image
```
docker pull m4a11205/paradrop-smartbase-multi
```
+ docker run -v /Users:/link/Users -p 9000:9000 -p 8000:8000 -t -i m4a11205/paradrop-smartbase-multi /bin/bash

+ cd /root/openface

+ ./util/align-dlib.py ./training-images/ align outerEyesAndNose ./aligned-images/ --size 96

+ ./util/align-dlib.py /link/Users/training-images/ align outerEyesAndNose ./aligned-images/ --size 96

+ ./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/

+ ./demos/classifier_multi.py train ./generated-embeddings/

+ cp -f ./generated-embeddings/*.pkl /link/Users/Openface-on-Paradrop/chute/.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
