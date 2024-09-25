# script to install service and enable/start it

# Copy the service file to the systemd directory
cp ./HealthCheck.service /etc/systemd/system/

# Reload the systemd daemon
systemctl daemon-reload

# Enable the service
systemctl enable HealthCheck.service

# Start the service
systemctl start HealthCheck.service