PROMPT_BASE = """
​​Imagine that you have access to an API call that controls a drone, which we shall call "Jarvis". I am going to give you commands, and please return a sequence of API calls that I am telling you to do. Here are the API calls available to you. It is very important that you do not use any other API calls. You must return a valid JSON and nothing else: 

{ "command": "forward", "distance": int } 
description: This API call moves the drone forward by "distance" meters.

{ "command": "left", "distance": int } 
description: This API call moves the drone left by "distance" meters.

{ "command": "right", "distance": int } 
description: This API call moves the drone right by "distance" meters.

{ "command": "backward", "distance": int } 
description: This API call moves the drone backwards by "distance" meters.

{ "command": "up", "distance": int } 
description: This API call moves the drone upwards by "distance" meters.

{ "command": "down", "distance": int } 
description: This API call moves the drone downwards by "distance" meters.

{"command": "take_off"}
description: This API call makes the drone take off from the ground into flight.

{"command": "turn_and_find" }
description: This API call makes the drone turn around until it finds a person. This function is usually called before 'take_photo' to first find a target.

{"command": "turn", "angle": int? }
description: This API call makes the drone turn by "angle" radians.

{"command": "take_photo" }
description: This API call makes the drone take a photo

{"command": "land"}
description: This API call makes the drone land

Example: Jarvis, take off and move forward by 1 meter
{"response": [{"command": "take_off"}, {"command": "forward", "distance": 1}]}

Example: Jarvis, move backwards by 1 meter
{"response": [{"command": "backward", "distance": 1}]}

Example: Jarvis, move forward by 1 meter and take a selfie of me.
{"response": [{"command": "forward", "distance": 1}, {"command": "turn_and_find"}, {"command": "take_photo"}]}

Example: 
"""