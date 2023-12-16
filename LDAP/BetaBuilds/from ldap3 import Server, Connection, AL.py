from ldap3 import Server, Connection, ALL, SAFE_SYNC
import xml.etree.ElementTree as ET
from xml.dom import minidom
server = Server('ldap://172.17.101.162:389')
conn = Connection(server, 'CN=Administrator, CN=Users,DC=knight,DC=local', 'BOCES10!', client_strategy=SAFE_SYNC, auto_bind=True)
status, result, response, _ = conn.search('OU=KnightCorp,DC=knight,DC=local', '(objectclass=organizationalPerson)', attributes='*')
root = ET.Element("directory")
item_list = ET.SubElement(root, "item_list")
list_of_dicts = [dict(obj) for obj in response]

infodicts = []
key = "raw_attributes"
current = {}

# Display the result
for i, obj_dict in enumerate(list_of_dicts):
    #print(f"Dictionary {i + 1}: {obj_dict} \n")
    current = obj_dict[key]
        #print(current["givenName"],"\n")
    item = ET.SubElement(item_list, "item")
    ln = ET.SubElement(item, "ln")
    sn= current['sn']
    text_string = str(sn)
    result = text_string[2:-1]
    ln.text = result

    fn = ET.SubElement(item, "fn")
    first = current['givenName']
    text_string = str(first)
    result = text_string[2:-1]
    fn.text = result

    ct = ET.SubElement(item, "ct")
    num = current['telephoneNumber']
    text_string =str(num)
    result = text_string[2:-1]
    ct.text = result

    sd = ET.SubElement(item, "sd")
    sd.text = str(i)

    rt = ET.SubElement(item, "rt")
    rt.text = "3"

    dc = ET.SubElement(item, "dc")
    dc.text = ""

    ad = ET.SubElement(item, "ad")
    ad.text = "0"

    ar = ET.SubElement(item, "ar")
    ar.text = "0"

    bw = ET.SubElement(item, "bw")
    bw.text = "0"

    bb = ET.SubElement(item, "bb")
    bb.text = "0"

tree = ET.ElementTree(root)
xml_str = ET.tostring(root, encoding='utf-8').decode()
xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")
xml_str = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<!-- $RCSfile$  $Revision: 35928 $ -->\n{xml_str}'

# Write to the XML file
with open("example.xml", "w") as file:
    file.write(xml_str)