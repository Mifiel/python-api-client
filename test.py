from mifiel import Mifiel
from mifiel import Document

import random

app_id = '836dd40b613ffb1bb06585bdc57638ff0ff2dbc0'
secret_key = 'rkV4tj1sHxUM26OJpr2MK5U2re4luERo/SmXB1s6o/l9G/Ei4rFKrrArhEKMIufQgndZXaIywX05tPN2OvPt7w=='
mifiel = Mifiel(app_id, secret_key)

signatories = [{ 'email': 'some@email.com' }]
d = Document.create(mifiel, signatories, dhash='asd', callback_url='http://first_url/')
print(d.id)
print('callback_url', d.callback_url)

d = Document.get(mifiel, d.id)
print('id', d.id)
print('callback_url', d.callback_url)

d.callback_url = 'http://callback_url/{}'.format(random.randrange(0, 101, 2))
print('callback_url', d.callback_url)
d.save()

d = Document.get(mifiel, d.id)
print('callback_url', d.callback_url)
