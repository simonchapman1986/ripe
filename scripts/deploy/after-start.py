import requests

check_instance_uri = 'http://local-reporting.local/api/v1/check_instance/'
print 'checking instance at {}:'.format(check_instance_uri)

response = requests.get(check_instance_uri)
print response.text
