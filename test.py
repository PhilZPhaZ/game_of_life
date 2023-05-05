import threading

class GameWindow:
    def __init__(self):
        self.run = threading.Event()
        
    def auto_update(self):
        while self.run.is_set():
            print('OK')
    
    def stop(self):
        self.run.clear()
    
    def start(self):
        self.run.start()