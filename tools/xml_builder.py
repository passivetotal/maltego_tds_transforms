from xml.dom import minidom

content = ''
content += '<?xml version="1.0" encoding="UTF-8"?><root>'
content += '<Value>www.passivetotal.org</Value>'
content += '<Weight>0</Weight>'
content += '<Entry Type="maltego.Domain"></Entry>'
content += '<TransformFields>'
content += '<Field Name="aKey">fuckitall</Field>'
content += '</TransformFields>'
content += '<AdditionalFields>'
content += '<Field Name="Derp">haha</Field>'
content += '</AdditionalFields>'
content += '</root>'
xmldoc = minidom.parseString(content)
nodes = xmldoc.getElementsByTagName('TransformFields')[0]
settings = nodes.getElementsByTagName('Field')
for setting in settings:
    name = setting.attributes["Name"].value
    value = setting.childNodes[0].data
    print name, value

print nodes