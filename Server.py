import socket
import threading
import dframe as df
from threading import Thread
from dframe import *

lock = threading.Lock()

def client_thread(connection):
    try:
        data = connection.recv(1024)     #receiving voter details            #2
        print(f"Received voter data: {data.decode()}")

        #verify voter details
        log = (data.decode()).split(' ')
        log[0] = int(log[0])
        
        if(df.verify(log[0],log[1])):                                #3 Authenticate
            if(df.isEligible(log[0])):
                print('Voter Logged in... ID:'+str(log[0]))
                connection.send("Authenticate".encode())
            else:
                print('Vote Already Cast by ID:'+str(log[0]))
                connection.send("VoteCasted".encode())
                connection.close()
                return
        else:
            print('Invalid Voter')
            connection.send("InvalidVoter".encode())
            connection.close()
            return

        data = connection.recv(1024)                                    #4 Get Vote
        vote = data.decode()
        print("Vote Received from ID: "+str(log[0])+"  Vote: "+vote)
        
        lock.acquire()
        #update Database
        if(df.vote_update(vote,log[0])):
            print("Vote Casted Sucessfully by voter ID = "+str(log[0]))
            connection.send("Successful".encode())
        else:
            print("Vote Update Failed by voter ID = "+str(log[0]))
            connection.send("Vote Update Failed".encode())
                                                                        #5
        lock.release()
        connection.close()
        
    except Exception as e:
        print(f"Error in client thread: {e}")
        connection.close()

def voting_Server():
    serversocket = socket.socket()
    host = socket.gethostname()
    port = 4001

    ThreadCount = 0

    try :
        serversocket.bind((host, port))
    except socket.error as e :
        print(str(e))
    print("Waiting for the connection")

    serversocket.listen(10)

    print( "Listening on " + str(host) + ":" + str(port))

    while True :
        client, address = serversocket.accept()

        print('Connected to :', address)

        client.send("Connection Established".encode())   ### 1
        t = Thread(target = client_thread,args = (client,))
        t.start()
        ThreadCount+=1
        # break

    serversocket.close()

if __name__ == '__main__':
    voting_Server()