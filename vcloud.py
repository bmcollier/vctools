import xml.etree.ElementTree as ET
import requests
import base64
import logging
import pytest
import threading
from time import sleep

class VCloudSession:
    
    def __init__(self, username, password, organisation, endpoint):
        
        self.headers = {}
        self.username = username
        self.password = password
        self.organisation = organisation
        self.endpoint = endpoint
        
        #logging.getLogger().setLevel(logging.INFO)
        
        login = {'Accept':'application/*+xml;version=5.1', \
           'Authorization':'Basic '+ base64.b64encode(username + "@" + organisation + ":" + password)}
        response = requests.post(endpoint + 'sessions', headers = login)
        for key, value in response.headers.iteritems():
            if key == "x-vcloud-authorization":
                self.headers[key]=value
        logging.info("Headers: %s", self.headers)
        logging.info("Status code %s", response.status_code)
        self.last_status = response.status_code
    
    def organisation_url(self):
        
        response = requests.get(self.endpoint + 'org', data=None, headers = self.headers)
        root = ET.fromstring(response.content)
        for child in root:
                self.organisation = child.get("href")
        
        response = requests.get(self.organisation, data=None, headers = self.headers)
        self.root = ET.fromstring(response.content)
        
        return self.organisation
    
    def get_catalogue(self):
        response = requests.get(self.endpoint + 'vms/query', data=None, headers = self.headers)
        return response.text
    
    def list_vapps(self):
        payload = {"page": "1", "pageSize":"25", "format":"idrecords"}
        response = requests.get(self.endpoint + 'vApps/query', data=None, headers = self.headers, params=payload)
        return response.text
    
    def list_vapp_templates(self):
        response = requests.get(self.endpoint + 'vAppTemplates/query', data=None, headers = self.headers)
        return response.text
    
    def get_vapp(self, vapp_id):
        response = requests.get(self.endpoint + "/vApp/" + vapp_id, data=None, headers = self.headers)
        return response.text
    
    def suspend_vapp(self, vapp_id):
        response = requests.post(self.endpoint + "/vApp/" + vapp_id + "/power/action/suspend", data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def get_memory_config(self, vapp_id):
        response = requests.get(self.endpoint + "/vApp/" + vapp_id + '/virtualHardwareSection/memory', data=None, headers=self.headers)
        tree = ET.fromstring(response.content)
        return tree
    
    def set_memory_config_8gb(self, vapp_id):
        tree = ET.parse("8gb_mem.xml")
        root = tree.getroot() 
        xmlstring = ET.tostring(root, encoding='utf8', method='xml')
        response = requests.put(self.endpoint + "/vApp/" + vapp_id + "/virtualHardwareSection/memory", data=xmlstring, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def set_memory_config_2gb(self, vapp_id):
        tree = ET.parse("2gb_mem.xml")
        root = tree.getroot() 
        xmlstring = ET.tostring(root, encoding='utf8', method='xml')
        response = requests.put(self.endpoint + "/vApp/" + vapp_id + "/virtualHardwareSection/memory", data=xmlstring, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def shutdown_vapp(self, vapp_id):
        response = requests.post(self.endpoint + "/vApp/" + vapp_id + "/power/action/shutdown", data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def reboot_vapp(self, vapp_id):
        response = requests.post(self.endpoint + "/vApp/" + vapp_id + "/power/action/reboot", data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def poweron_vapp(self, vapp_id):    
        response = requests.post(self.endpoint + "/vApp/" + vapp_id + "/power/action/powerOn", data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['id']
    
    def poweroff_vapp(self, vapp_id):
        response = requests.post(self.endpoint + "/vApp/" + vapp_id + "/power/action/powerOff", data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        print response.text
        return root.attrib['id']
    
    def get_task_status(self, task_id):
        response = requests.get(self.endpoint + "/task/" + task_id, data=None, headers=self.headers)
        root = ET.fromstring(response.content)
        return root.attrib['status']
    
    def poll(self, api_function, vm_id):
        task_id = api_function(vm_id).split(":")[3]
        status = None
        while status != "success":
            sleep(0)
            print status
            status = self.get_task_status(task_id)

    def boost(self, vm_id, status_store, progress_store):
        boost_steps = (self.shutdown_vapp, self.set_memory_config_8gb, self.poweron_vapp)
        progress = 0
        for step in boost_steps:
            self.poll(step, vm_id)
            progress += (100/len(boost_steps))
            progress_store[vm_id]=progress
            status_store[vm_id]="Running"
        progress = 100
        progress_store[vm_id]=progress
        status_store[vm_id]="Complete"

    def deboost(self, vm_id, status_store, progress_store):
        boost_steps = (self.shutdown_vapp, self.set_memory_config_2gb, self.poweron_vapp)
        progress = 0
        for step in boost_steps:
            self.poll(step, vm_id)
            progress += (100/len(boost_steps))
            progress_store[vm_id]=progress
            status_store[vm_id]="Running"
        progress = 100
        progress_store[vm_id]=progress
        status_store[vm_id]="Complete"

class boost(threading.Thread):
    def __init__(self, threadID, vm_id, settings, status_store, progress_store):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.vm_id = vm_id
        self.settings = settings
        self.status_store = status_store
        self.progress_store = progress_store
    def run(self):
        vc_session = VCloudSession(self.settings.username, self.settings.password, self.settings.organisation, self.settings.endpoint)
        vc_session.boost(self.vm_id, self.status_store, self.progress_store)

class deboost(threading.Thread):
    def __init__(self, threadID, vm_id, settings, status_store, progress_store):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.vm_id = vm_id
        self.settings = settings
        self.status_store = status_store
        self.progress_store = progress_store
    def run(self):
        vc_session = VCloudSession(self.settings.username, self.settings.password, self.settings.organisation, self.settings.endpoint)
        vc_session.deboost(self.vm_id, self.status_store, self.progress_store)
    
if __name__ == "__main__":
    """Fire off main test if vcloudpy called directly"""
    import tests.test_memchange
    tests.test_memchange.test_main()