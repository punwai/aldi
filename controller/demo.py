from __future__ import absolute_import
from __future__ import print_function
import argparse
import json
import time
from http_client import HTTPClient

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


### Run
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseurl', metavar='URL', default='http://192.168.10.1',
                        help='the url of the vehicle')

    args = parser.parse_args()

    # Create the client to use for all requests.
    client = HTTPClient(args.baseurl,
                        pilot=True)

    client.land()
    skill = "final.main.ComLink"

    # client.takeoff()
    # time.sleep(2000)
    client.set_skill(skill)
    # client.save_image("./testimage.jpg")
    # time.sleep(1000)
    request = {
        'command': 'down',
        'time': 1000
    }
    # turn_and_find(client, skill)
    # client.send_custom_comms_receive_parsed(skill, request)


if __name__ == '__main__':
    main()
