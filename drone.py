from socket import *
from EventLoop import EventLoop
import msvcrt


class Drone():
    def __init__(self):
        self.ip = "192.168.4.153"
        self.port = 8090
        self.sock = socket(AF_INET, SOCK_DGRAM)    #udp socket
        self.data = [102, 128, 128, 0, 128, 0, 128, 153]
        self.sock.sendto(b'Bv', (self.ip, self.port))


    def connect(self):
        #self.sock.sendto(b'Bv', (self.ip, 8080))
        
        byteData = b''
        for i in range(8):
            byteData += self.data[i].to_bytes(1, "little")
            
        self.sock.sendto(byteData, (self.ip, self.port))
        yield

        #self.sock.sendto(b'Bw', (self.ip, self.port))


    def checkOdd(self):
        byte = self.data[1]
        for i in range(2, 6):
            byte ^= self.data[i]

        return self.getRightData(byte & 255)


    def getRightData(self, byte):
        if byte == 102 or byte == 153:
            byte += 1

        return byte


    def getInput(self):
        if not msvcrt.kbhit():
            return
            
        inp = msvcrt.getch().decode()

        if inp == 'a':
            pass

        elif inp == 's':
            self.data[3] = 0

        elif inp == 'd':
            pass

        elif inp == 'w':
            self.data[3] = 255

        self.data[6] = self.checkOdd()
        yield



def main():
    drone = Drone()
    while True:
        loop.add_task(drone.connect())
        loop.add_task(drone.getInput())
        yield
        
    yield


if __name__ == "__main__":
    loop = EventLoop()
    loop.run(main())
