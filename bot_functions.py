from time import time, sleep
from vision import Vision
from tkinter import messagebox

class OPTCBot:
    window = None
    device = None

    def __init__(self, window, device) -> None:
        self.window = window
        self.device = device

    # Converts from point in window capture, to point inside the emulator
    def convert_position(self, points):
        new_x = points[0] * self.device.w // self.window.w
        new_y = points[1] * self.device.h // self.window.h
        return new_x, new_y

    def try_find_multiple(self, needles :tuple, swipe=False, click=False, confidence=0.8, timeout=30):
        start_time = time()
        visions = [Vision(needle) for needle in needles]
        while True:
            feed = self.window.get_screenshot()
            for vis in visions:
                points = vis.find(feed, confidence)
                if points:
                    res = self.convert_position(points[0])
                    if click:
                        sleep(0.5)
                        self.device.Click(res)
                        sleep(1)
                    return res
            if swipe:
                self.device.Swipe(self.device.w // 2, 1500, self.device.w // 2 - 50, 1500)
                sleep(0.4)
            if time() - start_time > timeout:
                # messagebox.showinfo("Error!", "Request timed out!")
                return None

    def try_find(self, needle :str, swipe=False, click=False, confidence=0.8, timeout=30):
        start_time = time()
        vis = Vision(needle)
        while True:
            feed = self.window.get_screenshot()
            points = vis.find(feed, confidence)
            if points:
                res = self.convert_position(points[0])
                if click:
                    sleep(0.5)
                    self.device.Click(res)
                    sleep(1)
                return res
            if swipe:
                self.device.Swipe(self.device.w // 2, 1500, self.device.w // 2 - 50, 1500)
                sleep(0.4)
            if time() - start_time > timeout:
                # messagebox.showinfo("Error!", "Request timed out!")
                return None
    
    def wait_needle_to_disappear(self, needle, click=False, confidence=0.8, timeout=30):
        res = self.try_find(needle, click=click, confidence=confidence, timeout=timeout)
        while res:
            res = self.try_find(needle, click=click, confidence=confidence, timeout=2)
    
    def run_map(self, triple_drops=False):
        res = self.try_find("support_captain.png", click=True)
        res = self.try_find("select.png", click=True)
        if triple_drops:
            res = self.try_find("triple_drops.png", click=True, confidence=0.9)
            res = self.try_find("yes.png", click=True)
        else:
            self.try_find("ok.png", click=True)
            self.try_find("yes.png", click=True, timeout=5)
        self.wait_needle_to_disappear("loading.png")
        self.try_find("auto.png", click=True)
        self.try_find("ok.png", click=True, timeout=150)
        search = ("level_up.png", "first_clear.png")
        self.try_find_multiple(search, click=True, timeout=10)
        self.wait_needle_to_disappear("ok.png", click=True)

    def select_highlighted(self):
        sleep(0.2)
        self.device.Click((self.device.w//2, 1500))
        sleep(0.5)

    def is_present(self, needle):
        feed = self.window.get_screenshot()
        vis = Vision(needle)
        res = vis.find(feed, 0.8)

        return len(res) > 0
    
    def are_present(self, needles :tuple):
        feed = self.window.get_screenshot()
        visions = [Vision(needle) for needle in needles]
        for vis in visions:
            res = vis.find(feed, 0.8)
            if len(res) > 0:
                return True
        return False

    def in_home(self):
        return self.is_present("bounty.png")
    