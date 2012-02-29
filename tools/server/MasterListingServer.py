'''
Created on Feb 23, 2012

@author: Tizen
'''
import argparse,select,socket,sys,threading,time

class ListenServer:
    '''
    Binds to host and listens on port for incoming connections.
    Creates a threaded instant of ClientManager to observe connected client
    threads. When a connection is made to the listen port, it is used to
    instance Client class as a thread.    
    '''
    def __init__(self,host,port):
        '''
        Initializes variables used by class methods.
        '''
        self.host = host
        self.port = port
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.cmanage = None
    
    def run(self):
        '''
        Primary class method. Initializes listen socket, creates client manager
        and checks for newly connected clients. Once a new client is detected,
        creates new instance of Client class and adds it to client thread list,
        which is actively watched by client manager.
        '''
        self.start_listen()
        print('[LISTEN] %d' % (self.port,))
        self.cmanage = ClientManager(self.threads)
        self.cmanage.start()
        while 1:
            inputready,outputready,exceptready = select.select([self.server],[],[])
            for s in inputready:
                c = Client(self.server.accept())
                c.start()
                self.threads.append(c)
        self.handle_close()

    def start_listen(self):
        '''
        Attempts to bind to self.host and listen on self.port.
        If this fails, it tries to do so in an orderly manner.
        '''
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(self.backlog)
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print('Could not open socket: %s' % (message,))
            sys.exit(1)
            
    def handle_close(self):
        '''
        Tries to clean up active threads when told to shut down.
        '''
        self.server.close()
        for c in self.threads:
            c.running = 0
        self.cmanage.running = 0
            
class ClientManager(threading.Thread):
    '''
    Threaded class which is sent a list of client sockets.
    Client list is watched for protocol events and responds accordingly. 
    '''
    def __init__(self,clients):
        '''
        Initializes class variables
        '''
        threading.Thread.__init__(self)
        self.clients = clients
        self.running = 0
    
    def run(self):
        '''
        Cycles through clients, kicks them over to tick_clients
        '''
        self.running = 1
        while self.running:
            self.tick_clients()
            time.sleep(0.01) # Keep the while loop from hogging all of the CPU
            
    def tick_clients(self):
        '''
        Checks for disconnected clients and removes them from the active list.
        Checks remaining clients for pending data to be read as commands.
        Pops the oldest command and sends it to handle_command
        '''
        torem = []
        for c in self.clients:
            if not c.running: torem.append(c)
        for c in torem:
            self.clients.remove(c)
        for c in self.clients:
            if not len(c.readme): continue
            cmd = c.readme.pop(0)
            self.handle_command(c,cmd)
    
    def handle_command(self,c,cmd):
        '''
        Decides how to handle individual commands, according to defined protocol.
        For more information: https://github.com/Zer0-/Udon/wiki/Master-Listing-Server
        '''
        if cmd.split()[0] == 'HELLO':
            '''
            Receives listen port and version information from client
            TODO: Validate port and ensure that version is a proper client version.
            Currently it assumes the client will send valid parameters.
            '''
            if len(cmd.split()) == 3:
                c.lport = cmd.split()[1]
                c.version = cmd.split()[2]
                c.valid = 1
                c.send('WELCOME')
            else:
                c.send('MALFORMED')        
        elif cmd == 'CLIENTS':
            '''
            Request for a count of potential peers.
            A peer qualifies if it is
                a) Valid (sent proper HELLO information)
                b) Matches versions
            '''
            if not c.valid: return
            valids = []
            for check in self.clients:
                if check == c: continue
                if check.valid and check.version == c.version:
                    valids.append(check)
            c.send('CLIENTS %d' % (len(valids),))
        elif cmd == 'CLIENT':
            '''
            Sent by client when it expects to receive a CLIENT response with peer information.
            This checks for valid peers and then returns the "youngest" match.
            
            TODO: Change wording of "youngest" to "oldest", since the oldest match is actually
            what is returned, you tard Tizen.
            '''
            valids = []
            for check in self.clients:
                if check == c: continue
                if check.valid and check.version == c.version:
                    valids.append(check)
            if len(valids) > 0:
                youngest = (time.time()+1,None)
                for check in valids:
                    if check.birth <= youngest:
                        youngest = (check.birth,check)
                match = youngest[1]
                c.send('CLIENT %s %s' % (match.address[0],match.lport))
                c.valid = 0
                match.valid = 0
                print('    [MATCHED] %s => %s:%s' % (c.address[0],match.address[0],match.lport))
        else:
            '''
            Every other command that isn't accounted for gets printed to stdout, for debugging purposes.
            '''
            print('[CLICMD] %s' % (cmd,))

            
class Client(threading.Thread):
    '''
    Threaded class for handling individual client connections.
    '''
    def __init__(self,(client,address)):
        '''
        Initialize class variables.
        '''
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.readme = []
        self.running = 0
        self.valid = 0
        self.version = None
        self.lport = None
        self.birth = time.time()
    
    def run(self):
        '''
        Triggers handle_connect and attempts to receive data from the socket.
        If receive fails, it is because the socket was closed and triggers handle_close.
        '''
        self.running = 1
        self.handle_connect()
        while self.running:
            try:
                data = self.client.recv(self.size)
                self.handle_recv(data)
            except socket.error:
                self.handle_close()
            time.sleep(0.01)
            
    def handle_connect(self):
        '''
        Initiates protocol by sending "OK" to client after connection established.
        '''
        print('[CONNECT] %s' % (self.address[0],))
        self.send('OK')
    
    def handle_close(self):
        '''
        Displays disconnect, shuts down socket and flags thread for closure.
        '''
        print('[DISCON] %s' % (self.address[0],))
        self.client.close()
        self.running = 0
        
    def handle_recv(self,data):
        '''
        Breaks apart individual receives and partitions
        them in to the client's command buffer.
        '''        
        for cmd in data.strip().split('\n'):
            self.readme.append(cmd.strip())
    
    def send(self,data):
        '''
        Appends protocol terminator and uses actual socket send to write data.
        '''
        self.client.send('%s\n' % (data,))

def main(bind,port):
    '''
    I'm only commenting this for appearance sake.
    If you actually need an explanation of this function:
    http://learnpythonthehardway.org/    
    '''
    ListenServer(bind,port).run()

if __name__ == '__main__':
    '''
    Utilizes argparse to make command-line running of the app more intuitive.
    '''
    parser = argparse.ArgumentParser(description='Master Listing Server')
    parser.add_argument('-bind',default='',type=str,help='address to bind to')
    parser.add_argument('-port',default=44777,type=int,help='port to listen on')
    args = parser.parse_args()
    main(args.bind,args.port)