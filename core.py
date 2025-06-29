import datetime
import sys,csv,xml.etree,pprint,json,re
from gvm.connections import UnixSocketConnection
from gvm.errors import GvmError
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeCheckCommandTransform
from gvmtools.helper import Table
import lxml.etree as ET
from lxml.etree import tostring
from base64 import b64decode
from pathlib import Path
import config, os

class Core:
    
    def __init__(self,action):
        
        self.action = action
    
    def get_tasks(id): 
        
        path = '/run/gvm/gvmd.sock'
        connection = UnixSocketConnection(path=path)
        transform = EtreeCheckCommandTransform() 

        gvm_user = config.authen.get("username", "")  
        gvm_pass = config.authen.get("password", "") 

        conf_username = gvm_user
        conf_password = gvm_pass
        
        fid = id
        
        try:

            with Gmp(connection=connection, transform=transform) as gmp:

                gmp.authenticate(username=conf_username,password=conf_password)
                
                response = gmp.get_tasks(filter_string=fid) 
                tasks = response.xpath("task")
                
                try:
                    i = 1
                    for task in tasks: 
                        task_id  = task.get("id")
                        i = i+1 
                        
                    t_response = gmp.get_task(task_id =task_id)  
                    
                    inner_html = tostring(t_response)  
                    
                    tt = str(inner_html,'utf-8') 
                    
                    tag = "status" 
                    reg_str = "<" + tag + ">(.*?)</" + tag + ">"
                    res = re.findall(reg_str, tt)
                    
                    # return res[0]
                
                    value = {
                    
                    "status": res[0],
                    
                    } 
                    
                    return json.dumps(value)
                    
                except:
                    
                    value = {
                    
                    "status": False,
                    
                    } 
                    
                    return json.dumps(value)

        except GvmError as e:

            msg = 'An error occurred'
            status = False
            
            value = {
                
                "status": status, 
                "message": msg, 
                
                } 
                
        return json.dumps(value) 
    
    def get_report_pdf(id):
        
        path = '/run/gvm/gvmd.sock'
        connection = UnixSocketConnection(path=path)
        transform = EtreeCheckCommandTransform() 

        gvm_user = config.authen.get("username", "")  
        gvm_pass = config.authen.get("password", "") 

        conf_username = gvm_user
        conf_password = gvm_pass
        
        fid = id
        
        try:

            with Gmp(connection=connection, transform=transform) as gmp:

                gmp.authenticate(username=conf_username,password=conf_password)
                
                response_xml_tmp = gmp.get_reports(filter_string=fid,details='True')
                reports_xml = response_xml_tmp.xpath("report")

                i = 1
                for task in reports_xml: 
                    report_id = task.get("id")
                    i = i+1
                    
                filename = report_id +".pdf"
                
                full_path = "/home/unitvas/APP/report/"+ filename
                
                response = gmp.get_report(report_id=report_id,report_format_id='c402cc3e-b531-11e1-9163-406186ea4fc5') 
                report_element = response.find("report")
                content = report_element.find("report_format").tail
                binary_base64_encoded_pdf = content.encode('ascii')
                binary_pdf = b64decode(binary_base64_encoded_pdf)
                pdf_path = Path(full_path).expanduser()
                pdf_path.write_bytes(binary_pdf) 
                
                value = {
                
                "status": True, 
                "id": filename, 
                
                } 
                
                return json.dumps(value)

        except GvmError as e:

            msg = 'An error occurred'
            status = False
            
            value = {
                
                "status": status, 
                "message": msg, 
                
                } 
                
        return json.dumps(value) 

    # def get_report_xml_old(id):
        
    #     path = '/run/gvm/gvmd.sock'
    #     connection = UnixSocketConnection(path=path)
    #     transform = EtreeCheckCommandTransform()

    #     ct = datetime.datetime.now() 
        
    #     gvm_user = config.authen.get("username", "")  
    #     gvm_pass = config.authen.get("password", "") 

    #     conf_username = gvm_user
    #     conf_password = gvm_pass
        
    #     fid = id
        
    #     try:

    #         with Gmp(connection=connection, transform=transform) as gmp:

    #             gmp.authenticate(username=conf_username,password=conf_password)
                
    #             response_xml_tmp = gmp.get_reports(filter_string=fid)
    #             reports_xml = response_xml_tmp.xpath("report")

    #             i = 1
    #             for task in reports_xml: 
    #                 report_id = task.get("id")
    #                 i = i+1
                
    #             response = gmp.get_report(report_id=report_id) 

    #             inner_html = tostring(response) 

    #             f = open('/home/unitvas/APP/report/'+report_id+'.xml', 'wb')
    #             f.write(inner_html)
    #             f.close() 
                
    #             value = {
                
    #             "status": 'True', 
    #             "id": report_id+'.xml', 
                
    #             } 
                
    #             return json.dumps(value)

    #     except GvmError as e:

    #         msg = 'An error occurred'
    #         status = False
            
    #         value = {
                
    #             "status": status, 
    #             "message": msg, 
                
    #             } 
                
    #     return json.dumps(value)


    def get_report_xml(id):
        path = '/run/gvm/gvmd.sock'
        connection = UnixSocketConnection(path=path)
        transform = EtreeCheckCommandTransform()

        ct = datetime.datetime.now()

        gvm_user = config.authen.get("username", "")
        gvm_pass = config.authen.get("password", "")

        conf_username = gvm_user
        conf_password = gvm_pass

        fid = id

        try:
            with Gmp(connection=connection, transform=transform) as gmp:
                gmp.authenticate(username=conf_username, password=conf_password)

                response_xml_tmp = gmp.get_reports(filter_string=fid)
                reports_xml = response_xml_tmp.xpath("report")

                for task in reports_xml:
                    report_id = task.get("id")
                    break
                filter_string = (
                    f"apply_overrides=0 levels=hmlg rows=1000 "
                    f"min_qod=0 sort-reverse=severity report_id={report_id}"
                )
                raw_results = gmp.get_results(filter_string=filter_string)
                result_xml = tostring(raw_results, pretty_print=True, encoding='utf-8')

                output_path = f"/home/unitvas/APP/report/{report_id}.xml"
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(result_xml)

                value = {
                    "status": True,
                    "id": f"{report_id}.xml"
                }

                return json.dumps(value)

        except GvmError as e:
            return json.dumps({
                "status": False,
                "message": f"An error occurred: {str(e)}"
            })
    

    def task_now(ip):
        
        path = '/run/gvm/gvmd.sock'
        connection = UnixSocketConnection(path=path)
        transform = EtreeCheckCommandTransform()

        ct = datetime.datetime.now()
        ts = ct.timestamp()

        gvm_user = config.authen.get("username", "")  
        gvm_pass = config.authen.get("password", "") 

        conf_username = gvm_user
        conf_password = gvm_pass
        
        # self.ip = ip
        
        ipaddress = ip  #IP Address for scanning
        # ipaddress= '192.168.19.162'  #IP Address for scanning
        prefix_time = str(ts)
        # Parameter for create target 
        name= 'UnitVAS Target IP '+ipaddress+' / '+prefix_time
        port_list_id ='33d0cd82-57c6-11e1-8ed1-406186ea4fc5'
        comment = 'Automatically generated by UnitVAS'

        # Parameter for create task 
        scan_config_id = 'daba56c8-73ec-11df-a475-002264764cea'
        scanner_id = '08b69003-5fc2-4037-a479-93b440211c73'
        
        try:

            with Gmp(connection=connection, transform=transform) as gmp:

                gmp.authenticate(username=conf_username,password=conf_password)
                # --- for create target  --- #
                response = gmp.create_target(name=name, hosts=[ipaddress], port_list_id=port_list_id,comment=comment)
                
                target_id = response.get("id")
                
                # --- for create task  --- #
                
                t_name= 'Automate Scan / IP '+ipaddress+' / '+prefix_time
                response = gmp.create_task(
                    name=t_name,
                    config_id=scan_config_id,
                    target_id=target_id,
                    scanner_id=scanner_id,
                )
                
                task_id = response.get("id")
                
                response = gmp.start_task(task_id)
                
                
                value = {
                
                "status": True, 
                "id": prefix_time, 
                
                } 
                
                # response = gmp.start_task(task_id) 

            return json.dumps(value)

                # --- End --- #

        except GvmError as e:

            msg = 'An error occurred'
            action = False
            
            value = {
                
                "status": action, 
                "id": msg, 
                
                }  

        return json.dumps(value)
