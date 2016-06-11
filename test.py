from mifiel import ApiAuth
import requests

a = ApiAuth('as', 'asd')
req = requests.Request()
req.url = 'http://localhost:3000/api/v1/documents'
req.method = 'GET'
req = a.sign_request(req)
req.prepare()

