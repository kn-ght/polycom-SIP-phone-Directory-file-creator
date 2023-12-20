serial = input("serial address for device")
from ldap3 import Server, Connection, ALL, SAFE_SYNC
import xml.etree.ElementTree as ET
from xml.dom import minidom
#change based on your server
server = Server('ldap://172.19.184.99:389')
#change based upon your server
conn = Connection(server, 'CN=Administrator, CN=Users,DC=knight,DC=local', 'BOCES10!', client_strategy=SAFE_SYNC, auto_bind=True)
status, result, response, _ = conn.search('OU=KnightCorp,DC=knight,DC=local', '(objectclass=organizationalPerson)', attributes='*')
root = ET.Element("directory")
item_list = ET.SubElement(root, "item_list")
list_of_dicts = [dict(obj) for obj in response]
infodicts = []
favnum = 0
scraped = []
for i,dics in enumerate(list_of_dicts):
    #print(dics['raw_attributes'],'\n')
    infodicts.append(dics['raw_attributes'])

for i in infodicts:
    las = i['sn']
    las=str(las)
    last = las[3:-2]
    firs=i['givenName']
    firs=str(firs)
    first = firs[3:-2]
    phon=i['telephoneNumber']
    phon=str(phon)
    phone=phon[3:-2]
    now = {'first':first,'last':last,'phone':phone}
    scraped.append(now)
scraped.sort(key=lambda x: x['last'])

for i in scraped:
    item = ET.SubElement(item_list, "item")
    ln = ET.SubElement(item, "ln")
    sn= i['last']
    result= str(sn)
    ln.text = result

    fn = ET.SubElement(item, "fn")
    first = i['first']
    result = str(first)
    fn.text = result

    ct = ET.SubElement(item, "ct")
    num = i['phone']
    result = str(num)
    ct.text = result

    sd = ET.SubElement(item, "sd")
    sd.text = str(favnum)
    favnum+=1
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
with open(serial+"-directory.xml", "w") as file:
    tree = ET.ElementTree(root)
    xml_str = ET.tostring(root, encoding='utf-8',xml_declaration=True).decode()
    xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")
    xml_str = f'{xml_str}'
    file.write(xml_str)
