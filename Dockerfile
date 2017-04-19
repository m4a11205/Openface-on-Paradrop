#  - Finds ip address webcam - used for detecting motion
# Version 1.10.00
#FROM m4a11205/paradrop-openface-base
FROM m4a11205/paradrop-smartbase
MAINTAINER Paradrop Team <info@paradrop.io>

# Install dependencies.  You can add additional packages here following the example.
#RUN apt-get update && apt-get install -y \
#	<package> \
#	apache2 \
#	iptables \
#	nodejs \
#	python-virtualenv \
#	python-imaging \
#	&& apt-get clean \
#	&& rm -rf /var/lib/apt/lists/*

# Install Flask
# RUN pip install Flask
RUN pip install soco


# Apache site configuration
ADD chute/000-default.conf /etc/apache2/sites-available/

#  Get the web frontend
ADD chute/web /var/www/html

# Install files required by the chute.
#
# ADD <path_inside_repository> <path_inside_container>
#
ADD chute/*.py /usr/local/bin/
ADD chute/classifier.pkl /usr/local/bin/
ADD chute/run.sh /usr/local/bin/run.sh

# Set the work dir for nodejs photo server
WORKDIR "/var/www/html"

EXPOSE 80 81 8000 8010 8011 8012 8013 8500 9000

CMD ["/bin/bash", "/usr/local/bin/run.sh"]
