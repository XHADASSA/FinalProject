import requests

# URL of the Flask server
server_url = 'http://localhost:3001/Main-Robots-suicide'

# Sending a POST request to the server
response = requests.post(server_url, json={'key': 'value'})

# Extracting and printing the response from the server
print(response.json())
