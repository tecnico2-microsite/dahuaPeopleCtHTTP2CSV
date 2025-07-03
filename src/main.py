import requests, os
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
def read_config(abs_xml_path = os.path.join(os.path.abspath(__file__).removesuffix(os.path.abspath(__file__).split(os.path.sep)[-1]),"local.config.xml")):
    
    xml_root = ET.parse(abs_xml_path).getroot()
    xml_content = {}
    for child in xml_root:
        xml_content[child.tag] = child.text
    
    return xml_content

def main():
    print(read_config())
    

if __name__=="__main__":
    main()

#print(abs_xml_path)
