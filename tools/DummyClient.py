'''
Created on Feb 23, 2012

@author: Tizen
'''
import argparse,select,socket,threading,time,asyncore

class ListenServer(threading.Thread):
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host = host
        self.port = 0
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.running = 0
        self.fail = 0
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host,self.port))
            self.server.listen(self.backlog)
            print('[LISTEN] %d' % (self.server.getsockname()[1],))
        except socket.error, (value,message):
            if self.server:
                self.server.close()
            print('[NOLIST] %s' % (message,))
            self.fail = 1
            
    def listenport(self):
        return self.server.getsockname()[1]
            
    def run(self):
        self.running = 1
        while self.running:
            inputready,outputready,exceptready = select.select([self.server],[],[])
            for s in inputready:
                c = RemoteClient(self.server.accept())
                c.start()
                self.threads.append(c)
            self.tick_clients()
            time.sleep(0.01)                                        
        self.handle_close()
    
    def tick_clients(self):
        torem = []
        for c in self.threads:
            if not c.running: torem.append(c)
        for c in torem:
            self.threads.remove(c)
        for c in self.threads:
            if not len(c.readme): continue
            cmd = c.readme.pop(0)
            print('[REMCMD] %s: %s' % (c.address,cmd,))            

    def handle_close(self):
        self.server.close()
        for c in self.threads:
            c.running = 0
            
class RemoteClient(threading.Thread):
    def __init__(self,(client,address)):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.size = 1024
        self.readme = []
        self.running = 0
        self.valid = 0
        self.version = None
        self.lport = None
    
    def run(self):
        self.running = 1
        self.handle_connect()
        while self.running:
            data = self.client.recv(self.size)
            if data:
                self.handle_recv(data)
            else:
                self.handle_close()
            time.sleep(0.01)
            
    def handle_connect(self):
        print('[REMCON] %s' % (self.address,))
        self.send('OK')
    
    def handle_close(self):
        print('[REMDIS] %s' % (self.address,))
        self.client.close()
        self.running = 0
        
    def handle_recv(self,data):
        print('[REMRCV] %s: %s' % (self.address,data,))
        for cmd in data.split('\n'):
            self.readme.append(cmd.strip())
    
    def send(self,data):
        print('[REMSND] %s: %s' % (self.address,data,))
        self.client.send('%s\n' % (data,))
        
class MLSClient(asyncore.dispatcher):
    def __init__(self,bind,ip,port):
        asyncore.dispatcher.__init__(self)
        self.buffer = []
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect((ip,port))
        self.bind = bind
        self.listener = None
        self.retry = 0
        self.valid = 0
        self.dead = 0
        self.readme = []

    def handle_connect(self):
        self.listener = ListenServer(self.bind)
        if self.listener.fail:
            print('[LSFAIL]')
            self.close()
        else:
            print('[MLSCON]')
    
    def handle_read(self):
        data = self.recv(1024)
        if data.strip():
            for cmd in data.strip().split('\n'):
                self.readme.append(cmd.strip())
                
    def writable(self):
        return (len(self.buffer) > 0)            

    def handle_write(self):
        out = self.buffer.pop(0)
        self.send('%s\n' % (out,))
        print('[MLSOUT] %s' % (out,))
        
    def handle_close(self):
        print('[MLSBYE]')
        self.close()
        self.dead = 1
        
class MLSManager(threading.Thread):
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client = client
        self.running = 0
    
    def run(self):
        client = self.client
        self.running = 1
        while self.running and not client.dead:
            if len(client.readme) > 0:
                self.handle_command(client.readme.pop(0))
            if client.valid and client.retry > 0 and client.retry <= time.time():
                self.send('CLIENTS')
                client.retry = 0            
            time.sleep(0.01)
            
    def send(self,data):
        self.client.send('%s\n' % (data,))
        #print('[MLSSND] %s (%d)' % (data,len(self.client.buffer)))
            
    def handle_command(self,cmd):
        if cmd == 'OK':
            self.send('HELLO %s %s' % (self.client.listener.listenport(),'DEV_VERSION'))
        elif cmd == 'WELCOME':
            self.client.valid = 1
            self.send('CLIENTS')
        elif cmd.split()[0] == 'CLIENTS' and len(cmd.split()) == 2:
            amnt = cmd.split()[1]
            self.client.retry = 0
            if int(amnt) < 1:
                self.client.retry = time.time()+5
            else:
                self.send('CLIENT')
        elif cmd.split()[0] == 'CLIENT' and len(cmd.split()) == 3:
            print('[WINNER] %s:%s' % (cmd.split()[1],cmd.split()[2]))
        else:
            print('[MLSREC] %s' % (cmd,))


def main(bind,ip,port):
    client = MLSClient(bind,ip,port)
    MLSManager(client).start()
    asyncore.loop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MLS Dummy Client')
    parser.add_argument('-ip',default='mobfinite.ath.cx',type=str,help='master listing address')
    parser.add_argument('-port',default=44777,type=int,help='master listing port')
    parser.add_argument('-bind',default='',type=str,help='local ip to bind listen port')
    args = parser.parse_args()
    main(args.bind,args.ip,args.port)