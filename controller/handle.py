# echo-server.py

import socket
import json
import argparse
import time

from http_client import HTTPClient

HOST = "169.254.224.133"  # Standard loopback interface address (localhost)
PORT = 65436  # Port to listen on (non-privileged ports are > 1023)

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument('--baseurl', metavar='URL', default='http://192.168.10.1',
                    help='the url of the vehicle')

parser.add_argument('--skill-key', type=str,
                    help='the import path of the ComLink Skill already on the R1')

args = parser.parse_args()

# client = HTTPClient(args.baseurl,
#                     pilot=True)
# client.set_skill(skill)

# client = None

args.skill_key = "final.main.ComLink"

def turn_and_find(client, skill):
    request = {
        'command': 'spin',
    }
    client.send_custom_comms_receive_parsed(skill, request)
    while (True):
        request = {
            'command': 'getclosest',
        }
        response = client.send_custom_comms_receive_parsed(skill, request)
        response_json = json.loads(response)
        if ('position_cov' in response_json):
            position = response_json['position']
            distance_x = abs(position[0])
            distance_y = abs(position[1])
            # print(distance)
            if (distance_x < 3 and distance_y < 1):
                request = {
                    'command': 'stopspin',
                }
                client.send_custom_comms_receive_parsed(skill, request)
                request = {
                    'command': 'backward',
                    'time': 1000,
                }
                client.send_custom_comms_receive_parsed(skill, request)
                time.sleep(2)
                for _ in range(10):
                    try:
                        if (client.save_image("./selfie.jpg")):
                            break
                    except:
                        continue
                break

def preprocess_command(data):
    if data["command"] == "forward" or \
        data["command"] == "backward" or \
        data["command"] == "left" or \
        data["command"] == "right" or \
        data["command"] == "up" or \
        data["command"] == "down":
        data["time"] = 2000 * data["distance"]
        del data["distance"]
    return data

def handle_data(data, skill):
    client = HTTPClient(args.baseurl,
                    pilot=True)
    client.set_skill(skill)
    for command in data["response"]:
        cmd = preprocess_command(command)
        if cmd["command"] == 'turn_and_find':
            turn_and_find(client, skill)
            time.sleep(2)
            continue

        if cmd["command"] == 'take_off':
            print("Taking off")
            client.takeoff()
            time.sleep(3)
            continue

        if cmd["command"] == 'land':
            client.land()
            time.sleep(3)
            continue

        print("sending cmd:", cmd)
        client.send_custom_comms_receive_parsed(skill, cmd)
        time.sleep(2)

# We establish a port connection
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        data = None
        with conn:
            print(f"Connected by {addr}")
            # client.takeoff()
            while True:
                new_data = conn.recv(1024)
                if not new_data:
                    break
                data = new_data
                break
                # try:
        if conn:
            conn.close()

        print(data)
        if data:
            data = json.loads(data.decode('utf-8'))
            print(data)
            handle_data(data, args.skill_key)
                # except:
                    # continue
