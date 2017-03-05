#!/bin/bash

# Create the image cache directory
mkdir -p /var/www/html/motionLog
chmod a+rw /var/www/html/motionLog

# Execute LED Bulb Control
python /usr/local/bin/LedControl.py > LedControl.log 2> LedControl.err &

# Execute the file, one pic every 2 seconds
python /usr/local/bin/smarthouse.py -m_sec 5.0 > smarthouse.log 2> smarthouse.err &

# Add the symlink
ln -s --relative /var/www/html/motionLog /var/www/html/app-dist/

# Allow client traffic for development
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Enable mod rewrite
/usr/sbin/a2enmod rewrite

# Make sure apache2 is running and rewrite is enabled
/etc/init.d/apache2 restart

# Run photo server
/usr/bin/nodejs photo-server.js > photo-server.log 2> photo-server.err &

while true; do
    sleep 300
done

# If execution reaches this point, the chute will stop running.
exit 0
