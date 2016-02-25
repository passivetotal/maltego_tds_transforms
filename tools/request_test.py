import requests

url = 'http://127.0.0.1:8443/get_tags'

content = ''
content += '<?xml version="1.0" encoding="UTF-8"?><root>'
content += '<Value>1.186.114.229</Value>'
content += '<Weight>0</Weight>'
content += '<Entity Type="maltego.IP"></Entity>'
content += '<Limits SoftLimit="100"></Limits>'
content += '<TransformFields>'
content += '<Field Name="username">brandon@passivetotal.org</Field>'
content += '<Field Name="aKey">af62207054be38875f1566c21122e69d52c69ef680bf22d738a71d0a08a413db</Field>'
content += '</TransformFields>'
content += '<AdditionalFields>'
content += '<Field Name="Derp">haha</Field>'
content += '</AdditionalFields>'
content += '</root>'

response = requests.post(url, data=content)
print response.content
