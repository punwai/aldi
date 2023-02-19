from vehicle.skills.base_skill import Skill
import json
import numpy as np
import time

class ComLink(Skill):

    def __init__(self):
        super(ComLink, self).__init__()
        self.current_function = self.spin
        self.start_time = 0
        self.command_length = 0

    def update(self, api):
        api.phone.disable_movement_commands()
        self.current_function(api)

    def move_up(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([0,0,3], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

    def move_down(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([0,0,-3], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)


    def move_forward(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([3,0,0], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

    def move_backward(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([-3,0,0], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

    def move_left(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([0,3,0], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

    def move_right(self, api):
        current_time = int(time.time() * 1000)
        if (current_time - self.start_time < self.command_length):
            api.movement.set_desired_vel_body(np.array([0,-3,0], dtype=np.float), 0.5)
        else:
            api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

    def spin(self, api):
        api.movement.set_heading_rate(0.5)

    def stop_spin(self, api):
        api.movement.set_heading_rate(0)

    def handle_rpc(self, api, message):
        data = json.loads(message)
        command = data['command']
        api.movement.set_desired_vel_body(np.array([0,0,0], dtype=np.float), 0.5)

        if (command == "up"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_up
            self.command_length = data['time']
            response = {"response": "moveup"}
            return json.dumps(response)

        elif (command == "down"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_down
            self.command_length = data['time']
            response = {"response": "movedown"}
            return json.dumps(response)

        elif (command == "forward"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_forward
            self.command_length = data['time']
            response = {"response": "moveforward"}
            return json.dumps(response)

        elif (command == "backward"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_backward
            self.command_length = data['time']
            response = {"response": "movebackward"}
            return json.dumps(response)

        elif (command == "left"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_left
            self.command_length = data['time']
            response = {"response": "moveleft"}
            return json.dumps(response)

        elif (command == "right"):
            self.start_time = int(time.time() * 1000)
            self.current_function = self.move_right
            self.command_length = data['time']
            response = {"response": "moveright"}
            return json.dumps(response)

        elif (command == "spin"):
            self.current_function = self.spin
            response = {"response": "spin"}
            return json.dumps(response)

        elif (command == "stopspin"):
            self.current_function = self.stop_spin
            response = {"response": "stopspin"}
            return json.dumps(response)
    
        elif (command == "getclosest"):
            closest_track = api.subject.get_closest_track(np.array([0,0,0], dtype=np.float))
            if (closest_track):
                track_obj = {
                    "id": closest_track.track_id,
                    "position": (closest_track.position).tolist(),
                    "position_cov": (closest_track.position_cov).tolist(),
                    "velocity": (closest_track.velocity).tolist(),
                    "velocity_cov": (closest_track.velocity_cov).tolist()
                 }
                return json.dumps(track_obj)
            response = {"response": "noobjects"}
            return json.dumps(response)
    
        elif (command == "takephoto"):
            api.camera.save_recording_mode("PHOTO_DEFAULT")
            api.camera.press_shutter_button()
            response = {"response": "taking photo"}
            return json.dumps(response)
    
        elif (command == "photoformat"):
            return str(api.camera.get_photo_format())
    
        elif (command == "moveforphoto"):
            closest_track = api.subject.get_closest_track(np.array([0,0,0], dtype=np.float))
            if (closest_track):
                position = closest_track.position
                api.movement.set_desired_vel_body(np.array([0,0,15], dtype=np.float), 0.75)
                api.focus.set_custom_subject(position)
        
        elif (command == "recordingmode"):
            return str(api.camera.get_recording_mode())
        elif (command == "isphoto"):
            return str(api.camera.is_photo_mode())
        elif (command == "isrecording"):
            return str(api.camera.is_recording())

        response = {"response": "invalidcommand"}
        return json.dumps(response)
