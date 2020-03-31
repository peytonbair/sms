import httplib

data = '{ "name": "this is a password" }'
conn = httplib.HTTPSConnection('enjyrenadmyxd.x.pipedream.net')
conn.request("POST", "/",data, {'Content-Type': 'application/json'})
