from msvcrt import getch

class Controller():
    def __init__(self):
        self.running = True
        self.pressEvents = {}
        self.releaseEvents = {}
        self.lastKey = ""


    def run(self):
        ch = getch().decode()

        if self.lastKey != ch and self.lastKey:
            callback = self.releaseEvents.get(self.lastKey, None)
            if callback is not None:
                callback(self.lastKey)

        callback = self.pressEvents.get(ch, None)
        if callback is not None:
            callback()

        self.lastKey = ch

        yield


    def onPress(self, key, callback):
        self.pressEvents[key] = callback

    def onRelease(self, key, callback):
        self.releaseEvents[key] = callback
