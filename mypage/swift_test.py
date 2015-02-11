from swiftclient import client
import authen


def get_token():
    storageURL, authtoken = client.get_auth(authen.auth_url + ':35357/v2.0',
                                              authen.username,
                                              authen.password,
                                              tenant_name = authen.tenant_name,
                                              auth_version = 2)
    return storageURL, authtoken

storageURL, authtoken = get_token()

def account_info():
    headers, containers = client.get_account(url = storageURL,
                                             token = authtoken)
    return headers, containers

def container_info(container):
    headers, objects = client.get_container(url = storageURL,
                                            token = authtoken,
                                            container = container)
    return headers, objects


def object_info(container,obj):
    headers = client.head_object(url = storageURL,
                                         token = authtoken,
                                         container = container,
                                         name = obj)
    return headers
    
    
def create_container(container):
    return client.put_container(url = storageURL,
                                token = authtoken,
                                container = container)

def del_object(container,obj):
    return client.delete_object(url = storageURL,
                                token = authtoken,
                                container = container,
                                name = obj)
    
def del_container(container):
    headers, objs = container_info(container)
    if len(objs) != 0:
        for i in objs:
            del_object(container,i['name'])
    return client.delete_container(url = storageURL,
                                   token = authtoken,
                                   container = container)

def upload_object(container, obj_name, object_file):
    headers = {}
    size = object_file.size
    headers['X-Object-Meta-Orig-Filename'] = object_file.name
    return client.put_object(url = storageURL,
                             token = authtoken,
                             container = container,
                             name = obj_name,
                             contents = object_file,
                             headers = headers)
    
def download_object(container, objectname):
    url = get_temp_url(container, objectname)
    return url
