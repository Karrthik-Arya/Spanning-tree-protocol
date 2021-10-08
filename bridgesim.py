from bridge import *

class network():
    def __init__(self, n_bridges):
            self.n = n_bridges
            self.bridges = []
            self.lans = []
    def connect(self):
        for i in range(self.n):
            bridge = input()
            connections  = bridge[4:]
            connections = connections.split()
            connect_dict = {}
            lan_ports = []
            for connection in connections:
                connect_dict[connection] = 'DP'
                found = False
                for lan in self.lans:
                    if connection == lan.id:
                        lan_ports.append(lan)
                        found = True
                        break
                if not found:
                    lan = lan_unit(connection)
                    self.lans.append(lan)
                    lan_ports.append(lan)

            bridge_i = bridge_unit(i+1, connect_dict)
            self.bridges.append(bridge_i)
            for lan_port in lan_ports:
                lan_port.ports.append(bridge_i)

    def span_tree(self, trace):
        t = 0
        while True:
            roots = set()
            for bridge in self.bridges:
                roots.add(bridge.root_bridge)
            rec_messages = []
            for bridge in self.bridges:
                if bridge.state == 'root':
                    ports = bridge.ports.keys()
                    if trace == 1:
                        print( str(t)+" s B"+ str(bridge.id) + str([bridge.root_bridge, bridge.dist, bridge.id]))
                    for port in ports:
                        for lan in self.lans:
                            if port == lan.id:
                                lan_port = lan
                                break
                        lan_port.message = [bridge.root_bridge, bridge.dist, bridge.id]
                        for bridge_send in lan_port.ports:
                                if bridge_send.ports[lan_port.id] != "NP" and bridge_send.id != lan_port.message[2]:
                                    bridge_send.message = [lan_port.id] + lan.message
                                    #rec_messages.append( str(t+1)+" r B"+ str(bridge_send.id) + str([bridge.root_bridge, bridge.dist, bridge.id]))
                                    print(str(t+1)+" r B"+ str(bridge_send.id) + str([bridge.root_bridge, bridge.dist, bridge.id]))
                                    bridge_send.message_process()
                elif bridge.message != None:
                    ports = bridge.ports.keys()
                    if trace == 1:
                        print( str(t)+" s B"+ str(bridge.id) + str([bridge.root_bridge, bridge.dist, bridge.id]))
                    for port in ports:
                        if bridge.ports[port] == "DP":
                            for lan in self.lans:
                                if port == lan.id:
                                    lan_port = lan
                                    break
                            lan_port.message = [bridge.message[1], bridge.message[2]+1, bridge.id]
                            for bridge_send in lan_port.ports:
                                if bridge_send.ports[lan_port.id] != "NP" and bridge_send.id != lan_port.message[2]:
                                    bridge_send.message = [lan_port.id] + lan.message
                                    #rec_messages.append( str(t+1)+" r B"+ str(bridge_send.id) + str([bridge.message[0], bridge.message[1]+1, bridge.id]))
                                    print(str(t+1)+" r B"+ str(bridge_send.id) + str([bridge.message[0], bridge.message[1]+1, bridge.id]))
                                    bridge_send.message_process()
            
            t+=1
            #if trace ==1:
                #for message in rec_messages:
                   # print(message)
            if len(roots) == 1:
                break
            
    def print_network(self):
        for bridge in self.bridges:
            print(bridge.info())


trace = int(input())
n = input()
tree = network(int(n))
tree.connect()
tree.span_tree(trace)
tree.print_network()