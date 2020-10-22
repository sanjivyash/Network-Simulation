# CS-224M Assignment-1
This project is an attempt to simulate the spanning tree protocol.

## Executing the Program
To run the program, use the command:
```
./execute $input-file-path $output-file-path
```
from the root directory.

## Utility Classes
In the file ```code/utils.py``` lie two Python classes:

### Bridge
In this class, we have modelled a bridge in an ethernet network. It has the following methods:

```python
class Bridge:
    def __init__(self, name, idx, flag):
        '''
        DESC: create and initialise a bridge
        ARGS: 
            name (str): provide a name to the bridge like B1 or B2
            idx (int): provide a base id to the bridge to run the protocol
            flag (bool): indicates whether to output the trace
        RETURN: None
        '''
        self.name = name
        self.id = idx

        self.connections = set() # store all LAN objects connected
        self.root = self # root bridge according to this bridge
        self.dist = 0 # distance from self.root
        
        self.rp = None # root port if any
        self.dp = set() # set of all designated ports
        self.next = None # next bridge on path to root, if any

        self.mutate = False # state of object has changed or not
        self.forward = False # to forward config message or not
        self.table = {} # store host | forwarding port 
        
        self.flag = flag
        self.trace = [] # stores trace messages if flag is true

    def connect(self, lan):
        '''
        DESC: connect a lan/port to this  bridge 
        ARGS: 
            lan (LAN): LAN object to be connected to the bridge
        RETURN: None
        '''

    def send(self, t):
        '''
        DESC: send config messages to all connected LANs
        ARGS: 
            t (int): relative time at which this send was called
        RETURN: None
        '''
        # only send message if root yourself or if self.forward is true

    def receive(self, msg, lan, t):
        '''
        DESC: receive config messages forwarded by connected LANs
        ARGS:
            msg (tuple): the config message received
            lan (LAN): LAN from which message was received
            t (int): relative time at which message was received
        RETURN: None
        '''
        # drop the packet if sender port inactive
        # self.forward set to true only if root updated
        # self.mutate set to true only if some state variable altered

    def active(self, lan):
        '''
        DESC: specify whether a port is active after the protocol is run
        ARGS:
            lan (LAN): the port which is to be checked
        RETURN:
            (bool): True iff port is active
        '''

    def transmit(self, sender, header, t):
        '''
        DESC: forward received packet from LAN to receiver
        ARGS:
            sender (str): the host which sent the packet
            header (tuple): contains source and destination address
            t (int): relative time at which packet was forwarded 
        RETURN: None
        '''
        # do not send the packet back to sender

    def __repr__(self):
        '''
        DESC: dunder function to represent a bridge
        ARGS:
            self
        RETURN:
            (str): bridge name represents the object itself
        '''
```

### Port/LAN
In this class, we have modelled a LAN in an ethernet network. It has the following methods:

```python
class LAN:
    def __init__(self, name):
        '''
        DESC: create and initialise a bridge
        ARGS: 
            name (str): provide a name to the bridge like A or B
        RETURRN: None
        '''
        self.name = name
        self.connections = set() # store all bridgee objects connected
        self.hosts = set() # store all hosts on the network

    def connect(self, bridge):
        '''
        DESC: connect a lan/port to this  bridge 
        ARGS: 
            bridge (Bridge): Bridge object to be connected to the port
        RETURN: None
        '''

    def network(self, host):
        '''
        DESC: identify all hosts on the network
        ARGS:
            host (str): host to be connected
        RETURN: None
        '''

    def forward(self, message, t):
        '''
        DESC: receive config messages forwarded by connected LANs
        ARGS:
            message (tuple): the config message received
            t (int): relative time at which message was received
        RETURN: None
        '''
        # forward to all bridges except sender

    def transmit(self, sender, header, t):
        '''
        DESC: forward received packet from LAN to receiver
        ARGS:
            sender (Bridge or None): the bridge, if any, which sent the packet
            header (tuple): contains source and destination address
            t (int): relative time at which packet was forwarded
        RETURN: None 
        '''
        # forward to all bridges except sender

    def __repr__(self):
        '''
        DESC: dunder function to represent a LAN
        ARGS:
            self
        RETURN:
            (str): port name represents the object itself
        '''
```

## Algorithm
The protocol has been implemented to closey simulate the actual process:
- In the beginning, every bridge considers itself as the root (reflected by the initialisation of the class), and hence all bridges send the configuration messages.
- The bridges which realise that they are not roots stop generating configuration messages. For such bridges, send is activated only when ```self.forward = True```, i.e., when they receive a config message atleast as good as theirs.
- The LANs simply forward the received message to all bridges except receiver.
- The bridges change a port to NP if they receive a message which has a smaller distance from root bridge or has a smaller root bridge as the sender. 
- The simulation stops only when all bridges have ```self.mutate = False```, i.e., none of the bridges changed their dtate during the cycle.

The management of tables also follows the actual process closely:
- If destination not in bridge table, the packet is forwarded to all active ports except sender.
- If destination is in bridge table, the packet is forwarded to the port as directed by the table.
- The LANs simply forward the packet to all bridges except sender.
- If a bridge receives a message, it updates its table with the sender as the forwarding port for origin host of the packet.
