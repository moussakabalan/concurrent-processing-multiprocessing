# ⚙️ Concurrent TCP Server using Python: `multiprocessing`

A demo on a concurrent TCP server that **spawns a child process per client** using Python’s `multiprocessing.Process`.  
Includes clean shutdown, per-client request handling, and safe socket lifecycle management.

> Current protocol supports: `DISCONNECT` (Read below!).  
> The server responds with `200 OK` for supported commands and `400 BAD REQUEST` otherwise.

---

## 🛠️ Technologies Used
- **Language:** Python 3.x  
- **Libraries:** `socket`, `multiprocessing`, `sys`
- **Environment:** Developed using VS Code on Windows (compatible with any OS that supports Python)

---

## 📂 Project Structure
| File | Description |
|------|-------------|
| `Python/Server.py` | Concurrent TCP server. Listens for connections, forks a process per client, and cleans up on shutdown. |
| `Python/Client.py` | Test client to connect and send commands. |

---

## 📦 Prerequisites
- Python 3.x installed  
- *(Optional)* CPython interpreter for your operating system  

---

## 🚀 How to Run

### 1. Start the Server
Open a terminal and run:
```bash
# (Windows)
py Python/Server.py
```
You should see:
```bash
Server is ready to receive requests on port 12340...
```
### 2. Start the Client
In a separate terminal:
```bash
# (Windows)
py Python/Client.py <server_ip>
```
> Use localhost as <server_ip> if running on the same device.

You should see:
```bash
Hello Client!
```
### 3) Send commands
```bash
DISCONNECT
```
Server replies:
```
200 OK
```
Any other input:
```
400 BAD REQUEST
```

You can open **multiple terminals** and connect several clients at once—each is handled by its own child process.

---

## 🧩 Protocol (Current)
For the sake of the Demo, we have only one command supported by the Server.

`DISCONNECT` -> `200 OK` and the server closes the client connection.

Anything else → `400 BAD REQUEST`.


---

## 🖼️ Demo

<img width="2532" height="1464" alt="image" src="https://github.com/user-attachments/assets/bcf48ebf-376a-42d8-a679-8a2439319048" />

*Original Project Dated 07/23/25*
