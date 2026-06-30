# Gunicorn configuration
# This replaces ecosystem.config.js from Node.js version

bind = '0.0.0.0:5000'
workers = 2
worker_class = 'sync'
timeout = 120
keepalive = 5
errorlog = '/tmp/gunicorn-error.log'
accesslog = '/tmp/gunicorn-access.log'
loglevel = 'info'