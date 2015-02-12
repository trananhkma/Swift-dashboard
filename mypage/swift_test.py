from swiftclient import client
import authen
import requests
import hmac
import string
import random
import urlparse
from hashlib import sha1
from time import time


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
    headers_s = object_info(container, objectname)
    
    filename = headers_s['x-object-meta-orig-filename']
    base_path = '/home/trananhkma/Desktop/'
    etc = filename.split('.')[-1]
    path =  base_path +  objectname + '.' + etc
    
    url = storageURL + '/' + container + '/' + objectname
    r = requests.get(url, headers={'X-Auth-Token': authtoken}, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

def download_object2(container, objectname):
    headers , data = client.get_object(url = storageURL,
                                       token = authtoken,
                                       container = container,
                                       name = objectname)
    base_path = '/home/trananhkma/Desktop/'
    filename = headers['x-object-meta-orig-filename']
    etc = filename.split('.')[-1]
    path =  base_path +  objectname + '.' + etc
    with open(path, 'wb') as f:
        f.write(data)

def get_temp_key():
    headers_s, containers = account_info()
    key = headers_s.get('x-account-meta-temp-url-key')
    
    if not key:
        chars = string.ascii_lowercase + string.digits
        key = ''.join(random.choice(chars) for x in range(32))
        headers = {'x-account-meta-temp-url-key': key}
        client.post_account(storageURL, authtoken, headers)
    return key


def get_temp_url(container, objectname):
    key = get_temp_key()
    if not key:
        return None
    expires = 600
    expires += int(time())
    url_parts = urlparse.urlparse(storageURL)
    path = "%s/%s/%s" % (url_parts.path, container, objectname)
    base = "%s://%s" % (url_parts.scheme, url_parts.netloc)
    hmac_body = 'GET\n%s\n%s' % (expires, path)
    sig = hmac.new(key, hmac_body.encode("utf-8"), sha1).hexdigest()
    url = '%s%s?temp_url_sig=%s&temp_url_expires=%s' % (
        base, path, sig, expires)
    return url