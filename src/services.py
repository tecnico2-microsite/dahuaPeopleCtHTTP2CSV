import requests, os, csv
from requests.auth import HTTPDigestAuth
from datetime import date,timedelta
import xml.etree.ElementTree as ET
def read_config(abs_xml_path = os.path.join(os.path.abspath(__file__).removesuffix(os.path.abspath(__file__).split(os.path.sep)[-1]),"local.config.xml")):
    
    xml_root = ET.parse(abs_xml_path).getroot()
    xml_content = {}
    for child in xml_root:
        xml_content[child.tag] = child.text
    
    return xml_content

def get_token_request(url_object,channel,dateSince=str(date.today() - timedelta(days=1)),dateUntil=str(date.today())):
    url = f"{url_object['url']}cgi-bin/videoStatServer.cgi?action=startFind&channel={channel}&condition.StartTime={dateSince}%2000:00:00&condition.EndTime={dateUntil}%2000:00:00&condition.Granularity=Hour&condition.RuleType=NumberStat"
    
    response=requests.get(url,auth=url_object["auth"])
    
    response_object = response.text.split("=")
    response_object= {
        "token":response_object[1].split("\r")[0],
        "totalCount":response_object[2].split("\r")[0]
    }
    
    
    return response_object

def get_peopleCounting_wtoken(url_object,channel,token_object):
    url = f"{url_object['url']}cgi-bin/videoStatServer.cgi?action=doFind&channel={channel}&token={token_object['token']}&beginNumber=0&count={token_object['totalCount']}"
    
    response=requests.get(url,auth=url_object["auth"])
    response_object = response.text.split("\r\n")
    response_object.pop(0)
    
    parsed_response = []
    
    for i in range(len(response_object)//8):
        index_hour = response_object[7+(8*i)].split("=")[1]
        index_entries = response_object[3+(8*i)].split("=")[1]
        index_exits = response_object[4+(8*i)].split("=")[1]
        
        parsed_response.append([channel,index_hour,index_entries,index_exits])
    
    return parsed_response

def generate_CSV(parsed_response,path=os.path.join(os.path.abspath(__file__).removesuffix(os.path.abspath(__file__).split(os.path.sep)[-1]),"export")):
    date = parsed_response[0][1].split(" ")[0]
    
    with open(f"{path}{os.path.sep}{date}.csv","w+") as file:
        writer = csv.writer(file)
        header=["Canal","Hora","Núm. entradas","No. Salida"]
        writer.writerow(header)
        for i in range(len(parsed_response)):
            row=[parsed_response[i][0],parsed_response[i][1],parsed_response[i][2],parsed_response[i][3]]
            writer.writerow(row)
        file.close()
    

def generate_day(day):
    """Parámetro de entrada 'day' debería verse tal que YYYY-MM-DD"""
    config = read_config()
    url = f"http://{config['ip']}:{config['port']}/"
    username = config["username"]
    password= config["password"]
    channel=config["channel"]
    url_object={
        "url":url,
        "auth":HTTPDigestAuth(username,password)
    }
    dateUntil=day.split("-")
    dateUntil=str(date(int(dateUntil[0]),int(dateUntil[1]),int(dateUntil[2]))+timedelta(days=1))
    token_object = get_token_request(url_object,channel,day,dateUntil)
    generate_CSV(get_peopleCounting_wtoken(url_object,channel,token_object))
    return "success"
    
    

def generate_yesterday():
    config = read_config()
    url = f"http://{config['ip']}:{config['port']}/"
    username = config["username"]
    password= config["password"]
    channel=config["channel"]
    url_object={
        "url":url,
        "auth":HTTPDigestAuth(username,password)
    }
    
    token_object = get_token_request(url_object,channel)
    generate_CSV(get_peopleCounting_wtoken(url_object,channel,token_object))
    return "success"
    


def main():
    config = read_config()
    url = f"http://{config['ip']}:{config['port']}/"
    username = config["username"]
    password= config["password"]
    channel=config["channel"]
    
    url_object={
        "url":url,
        "auth":HTTPDigestAuth(username,password)
    }
    
    token_object = get_token_request(url_object,channel)
    print(generate_CSV(get_peopleCounting_wtoken(url_object,channel,token_object)))
if __name__=="__main__":
    main()
    

#print(abs_xml_path)
