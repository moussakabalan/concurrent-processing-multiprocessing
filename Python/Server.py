############################
#   Server.py - Concurrent TCP Server using multiprocessing to handle clients
#   Moussa Kabalan
#   7/23/25
############################

from socket import *
from multiprocessing import Process
import sys

SERVER_HOST: str = "" #> IP address of host. (localhost or 0.0.0.0/0 is default!)
SERVER_PORT: int = 12340

ACTIVE_CLIENTS: list[Process] = [] #> Track active connections with Clients

## Local-Function to handle individual client request
def _handleClient(connectionSocket, clientAddr):
    print(f"Child has connected to client: {clientAddr[0]}:{clientAddr[1]}")

    try:
        #> Send welcome message to the client
        connectionSocket.send("Hello Client!\n".encode())

        while True:
            try:
                Data = connectionSocket.recv(1024)
                if Data is None: break

                Message = Data.decode().strip()

                if Message == "DISCONNECT":
                    connectionSocket.send("200 OK\n".encode())
                    break
                else:
                    connectionSocket.send("400 BAD REQUEST\n".encode())
            except Exception as err:
                print(f"[Child] recv/send error: {err}")
                break
    except Exception as err:
        print(f"[Child] error: {err}")
    finally:
        try:
            connectionSocket.shutdown(SHUT_RDWR)
        except Exception:
            pass

        #> Close the connection and wrap up
        connectionSocket.close()
        print(f"Child has disconnected from client: {clientAddr[0]}:{clientAddr[1]}")

## Main Function
def startServer():
    try:
        ## Create our TCP socket to accept requests
        serverSocket = socket(AF_INET, SOCK_STREAM)
        serverSocket.bind((SERVER_HOST, SERVER_PORT))
        serverSocket.listen(10) #> Begin listening (up to 10 connections at once)

        print(f"Server is ready to accept clients on port {SERVER_PORT}...")
    except Exception as err:
        print(f"An error has occurred while starting up! Log: {err}")
        sys.exit()

    def Exit():
        print("\nShutting down Server...")

        try:
            serverSocket.close()
        except Exception:
            pass

        for Client in ACTIVE_CLIENTS:
            if Client.is_alive():
                Client.terminate()

        for Client in ACTIVE_CLIENTS:
            try:
                Client.join(timeout=2)
            except Exception:
                pass

        sys.exit(0)

    ## While-loop to continue taking connections + requests from clients
    try:
        while True:
            try: #> Try-Except wrapper to safe guard from any possible error; primarily if the client forcibly closed the connection
                connectionSocket, clientAddr = serverSocket.accept() #> Wait for connection from clients
                print(f"New connection from {clientAddr[0]}:{clientAddr[1]}")

                #> Spawn new process to handle client. We clone the parent to make a Child process.
                Client = Process(target=_handleClient, args=(connectionSocket, clientAddr))
                Client.start()

                ACTIVE_CLIENTS.append(Client)
                print(f"Total active clients connected so far: {len(ACTIVE_CLIENTS)}")

                #> Parent process doesn't need to use this socket anymore. So we can close it for Parent process!
                connectionSocket.close()
            except Exception as err:
                print(f"Unexpected error: {err}")
                break
    finally:
        Exit()

if __name__ == "__main__":
    startServer()
#end