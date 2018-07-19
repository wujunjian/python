from hashlib import md5

def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

client_id = 'dappbrowser';
key = 'ebS@p1wNyHN9WlR7';
url = 'https://cmpush-api.ksmobile.net/api/openpush/devices_push';
device_list = '98b2d0e9061af4d6';
device_type = 'mi_aid';
payload = '{"content":"test","type":"test_message"}';


param = { 
    'client_id' : client_id,
    'device_list' : device_list,
    'device_type' : device_type,
    'payload' : payload
};
print(param)

keys=sorted(param)
mstr=''
for k in keys:
    mstr+=param[k]

mstr+=key
print(mstr)
sign = make_md5(mstr)
print(sign)
param['sign'] = sign
print(param)
