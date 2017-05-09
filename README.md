# Openface-on-Paradrop

# Train Face Recognition Classifier
docker pull m4a11205/paradrop-smartbase-multi

docker run -v /Users:/link/Users -p 9000:9000 -p 8000:8000 -t -i m4a11205/paradrop-smartbase-multi /bin/bash
docker run -v /home/ubuntu:/link/ubuntu -p 9000:9000 -p 8000:8000 -t -i m4a11205/paradrop-smartbase-multi /bin/bash

cd /root/openface

./util/align-dlib.py ./training-images/ align outerEyesAndNose ./aligned-images/ --size 96

./batch-represent/main.lua -outDir ./generated-embeddings/ -data ./aligned-images/

./demos/classifier_multi.py train ./generated-embeddings/



cp -f ./generated-embeddings/*.pkl /host/Users/Ted/Desktop/UW_Proj/Openface-on-Paradrop/chute/.
