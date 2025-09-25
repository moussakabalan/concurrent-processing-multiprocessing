############################
#   Client.py - Basic TCP client to test multiprocessing-based server
#   Moussa Kabalan
#   7/23/25
############################

from socket import *
import sys

SERVER_PORT: int = 12340

## Main Function
def startClient():
    ## We must ask for server ip address to connect! (For testing, just use 'localhost'!)
    if len(sys.argv) != 2:
        print("IP address is missing from parameter! Please try again.")
        return

    SERVER_HOST = sys.argv[1]

    try:
        ## Initalize our connection to the server.
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((SERVER_HOST, SERVER_PORT))

        print("Successfully connected to server.")
    except Exception as err:
        print(f"An error occurred while connecting to server! Log: {err}")
        return

    try:
        #> Wait for welcome message
        Response = clientSocket.recv(1024).decode()
        print("Server response:", Response.strip())

        #> Using input to Pause and give the user the choice to disconnect
        input('Press ENTER to safely disconnect from the server.')

        clientSocket.send("DISCONNECT\n".encode())
        Response = clientSocket.recv(1024).decode()

        if Response.strip() == "200 OK":
            return
        else:
            print(Response, end='') #> Reponse code; unknown response?

    except Exception as err:
        print(f"An error occurred while receiving data! Log: {err}")
    finally:
        #> Close socket after one message (one-time server)
        clientSocket.close()
        print("Connection closed!")

if __name__ == "__main__":
    startClient()
#end