import requests

url = 'http://localhost:8000/multi'
multiple_files = [('files', ('file1.txt', open('files/file1.txt', 'rb'), 'text/plain')),
                      ('files', ('file2.txt', open('files/file2.txt', 'rb'), 'text/plain'))]
r = requests.post(url, files=multiple_files)
print(r.text)