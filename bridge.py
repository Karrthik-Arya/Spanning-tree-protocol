import numpy as np
import time
class bridge_unit():
    def __init__(self, id, connections):
        self.id = id
        self.state = "root"
        self.root_bridge = id
        self.root_sender_bridge = id
        self.dist = 0
        self.ports = connections
        self.message = None
    
    def info(self):
        str_connections = ''
        for connection_key in sorted(self.ports):
            str_connections += connection_key + '-' + self.ports[connection_key] + ' ' 
        return 'B' + str(self.id) +':' +str_connections + '   B'+ str(self.root_bridge) + ' - ' + str(self.dist)
    def message_process(self):
        if self.message:
            print("at B"+str(self.id) )
            print(self.message)
            print([self.state, self.root_bridge, self.dist, self.root_sender_bridge])
            if self.state == "root" and self.message[1] < self.id:
                self.state = "not root"
                self.root_bridge = self.message[1]
                self.dist = self.message[2] +1
                self.ports[self.message[0]] = 'RP'
                self.root_sender_bridge = self.message[3]
                print(str(self.id) + " I did run")
            elif self.message[1]<self.root_bridge:
                self.root_bridge = self.message[1]
                self.root_sender_bridge = self.message[3]
                self.dist = self.message[2] +1
                for port in self.ports:
                    if self.ports[port] == 'RP':
                        self.ports[port] = 'NP'
                self.ports[self.message[0]] = 'RP'
                 
                print(str(self.id) + " I1")
            elif self.message[1] == self.root_bridge and self.message[2]+1<self.dist:
                for port in self.ports:
                    if self.ports[port] == 'RP':
                        self.ports[port] = 'NP'
                self.ports[self.message[0]] = 'RP'
                self.root_sender_bridge = self.message[3]
                self.dist = self.message[2]+1
                 
                print(str(self.id) + " I2")
            elif self.message[1] == self.root_bridge and self.message[2]+1 == self.dist and self.message[3] < self.root_sender_bridge:
                
                for port in self.ports:
                    if self.ports[port] == 'RP':
                        self.ports[port] = 'NP'
                self.ports[self.message[0]] = 'RP'
                 
                print(str(self.id) + " I3")
            elif self.message[1] == self.root_bridge and self.message[2] < self.dist:
                self.ports[self.message[0]] = 'NP'
                print(str(self.id) + " I5")
                 
            elif self.message[1] == self.root_bridge and self.message[2] == self.dist and self.message[3]<self.id:
                self.ports[self.message[0]] = 'NP'
                print(str(self.id) + " I6")
            elif self.message[1:] == [self.root_bridge, self.dist - 1, self.root_sender_bridge]:
                for port in self.ports:
                    if self.ports[port] == 'RP':
                        if ord(self.message[0]) < ord(port):
                            self.ports[port] = 'NP'
                            self.ports[self.message[0]] = 'RP'
                             
                            print(str(self.id) + " I4")
                            break
                 
                
                     
                
                


class lan_unit():
    def __init__(self,id):
        self.id =id
        self.ports = []
        self.message = None
    def info(self):
        s = ''
        for port in self.ports:
            s += 'B' + str(port) +'-'+port.ports[self.id]+'; '
        return str(self.id)+':'+s



