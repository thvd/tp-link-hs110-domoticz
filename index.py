import socket
from struct import pack
import requests
import json

with open('config.json', 'r') as configFile:
    data = configFile.read()

# parse file
config = json.loads(data)

CMD = "{\"emeter\":{\"get_realtime\":{}}}"

IP = config['tplink_ip']
PORT = config['tplink_port']
DOMOTICZ_IP = config['domoticz_ip']
DOMOTICZ_PORT = config['domoticz_port']
DOMOTICZ_AMP_IDX = config['domoticz_ampere_idx']
DOMOTICZ_VOLT_IDX = config['domoticz_voltage_idx']
DOMOTICZ_WATT_IDX = config['domoticz_watt_idx']


# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
    key = 171
    result = bytearray(pack('>I', len(string)))
    for i in string:
        a = key ^ ord(i)
        key = a
        result.append(a)
    return result


def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ ord(chr(i))
        key = ord(chr(i))
        result += chr(a)
    return result


def call_domoticz(val_url):
    request = 'http://' + DOMOTICZ_IP + ':' + str(DOMOTICZ_PORT) + val_url
    # print request
    r = requests.get(request)  # , auth=HTTPBasicAuth(user, password)
    print("Status code:" + str(r.status_code))
    if r.status_code != 200:
        print("Error API Domoticz")


def post_value(idx, value):
    url = '/json.htm?type=command&param=udevice&idx=' + str(idx)
    url += '&nvalue=0&svalue='
    url += value
    call_domoticz(url)


def post_usage(voltage, amperage, watt):
    post_value(DOMOTICZ_AMP_IDX, '{0:0.3f}'.format(amperage))
    post_value(DOMOTICZ_VOLT_IDX, '{0:0.3f}'.format(voltage))
    post_value(DOMOTICZ_WATT_IDX, '{0:0.3f}'.format(watt))


try:
    sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_tcp.connect((IP, PORT))
    sock_tcp.send(encrypt(CMD))
    data = sock_tcp.recv(2048)
    sock_tcp.close()

    print("Sent:     ", CMD)
    resultJson = decrypt(data[4:])
    print("Received: ", resultJson)

    result = json.loads(resultJson)

    realtimeResult = result['emeter']['get_realtime']
    post_usage(realtimeResult['voltage_mv'] / 1000, realtimeResult['current_ma'] / 1000, realtimeResult['power_mw'] / 1000)

except socket.error:
    quit("Cound not connect to host " + IP + ":" + str(PORT))
