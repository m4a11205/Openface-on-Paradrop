# Security Cam v2
#  - Finds ip address webcam - used for detecting motion
# Version 1.10.00
FROM paradrop/workshop
MAINTAINER Paradrop Team <info@paradrop.io>

# Install dependencies.  You can add additional packages here following the example.
RUN apt-get update && apt-get install -y \
#	<package> \
	apache2 \
	iptables \
	nodejs \
	python-virtualenv \
	python-imaging \
	&& apt-get clean \
	&& rm -rf /var/lib/apt/lists/*

# Install pip
# RUN easy_install pip

# Install Flask
RUN pip install Flask

# Install sklearn
RUN sudo pip install --upgrade pip
RUN sudo pip install numpy
RUN sudo pip install scipy
RUN sudo pip install -U scikit-learn

# Install OpenCV
RUN sudo pip install opencv-python

# Apache site configuration
ADD chute/000-default.conf /etc/apache2/sites-available/

#  Get the web frontend
ADD chute/web /var/www/html

# Install files required by the chute.
#
# ADD <path_inside_repository> <path_inside_container>
#
ADD chute/smarthouse.py /usr/local/bin/smarthouse.py
ADD chute/LedControl.py /usr/local/bin/LedControl.py
ADD chute/test_cv.py /usr/local/bin/test_cv.py
ADD chute/haarcascade_frontalface_default.xml /usr/local/bin/haarcascade_frontalface_default.xml
ADD chute/yalefaces /usr/local/bin/yalefaces
ADD chute/run.sh /usr/local/bin/run.sh

# Set the work dir for nodejs photo server
WORKDIR "/var/www/html"

EXPOSE 80 81 8010 8011 8012

CMD ["/bin/bash", "/usr/local/bin/run.sh"]
