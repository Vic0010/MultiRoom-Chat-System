# MultiRoom-Chat-System
Secure multi-room chat system using TCP socket programming with SSL/TLS encryption, supporting concurrent clients, private messaging, and file transfer.
# Multi-Room Secure Chat System with File Transfer using TCP Sockets

##Problem Definition

**Multi-Room Secure Chat System with File Transfer using TCP Sockets**

### Problem Statement

Modern communication systems require secure and scalable messaging platforms capable of handling multiple users simultaneously. Traditional chat applications must support multiple chat rooms, private communication between users, and secure file sharing while maintaining message order and system reliability.

The objective of this project is to design and implement a **secure multi-room chat system using low-level socket programming**. The system allows multiple clients to connect concurrently to a central server, join chat rooms, exchange messages, send private messages, and transfer files securely using **SSL/TLS encryption**.

The system guarantees **message ordering within each chat room**, supports **multiple concurrent clients**, and ensures all communication occurs through **TCP network sockets**.

---

# Objectives

* Implement a **client–server chat application using TCP sockets**
* Support **multiple concurrent clients** using threading or asynchronous handling
* Allow users to **create and join multiple chat rooms**
* Ensure **message ordering within each chat room**
* Enable **private messaging between users**
* Implement **secure communication using SSL/TLS encryption**
* Support **file transfer between clients through the server**
* Evaluate **system performance under multiple concurrent connections**

---

# System Architecture

The system follows a **Client–Server Architecture**.

## Components

### 1. Chat Server

The server is responsible for:

* Managing all client connections
* Maintaining chat rooms
* Routing messages between clients
* Managing file transfers
* Enforcing message ordering
* Handling SSL/TLS security

### 2. Clients

Clients interact with the server to:

* Connect securely to the server
* Join chat rooms
* Send and receive messages
* Send private messages
* Upload and download files

---

# Architecture Diagram

```
                +---------------------+
                |     Chat Server     |
                |---------------------|
                | Room Manager        |
                | Message Router      |
                | File Transfer Unit  |
                | SSL/TLS Security    |
                +----------+----------+
                           |
        ---------------------------------------------
        |             |            |                |
   +---------+   +---------+  +---------+    +---------+
   | Client1 |   | Client2 |  | Client3 |    | Client4 |
   +---------+   +---------+  +---------+    +---------+
        |             |            |               |
     Chat Room A   Chat Room A  Chat Room B   Private Msg
```

---

# Communication Flow

1. Client establishes a **secure TCP connection** with the server using SSL/TLS.
2. The client sends a **username** to identify itself.
3. The client can **create or join chat rooms**.
4. Messages sent by a client are routed by the server to all members of the same chat room.
5. Private messages are routed directly between two users.
6. Files are transferred through the server to the intended recipients.

---

#Protocol Design

The system uses a simple text-based protocol.

## Join Room

```
JOIN room_name
```

Example:

```
JOIN room1
```

---

## Chat Message

```
MSG room_name message_text
```

Example:

```
MSG room1 Hello everyone
```

---

## Private Message

```
PM username message_text
```

Example:

```
PM Rahul Hi
```

---

## File Transfer

```
FILE username filename filesize
```

---

# Key Design Decisions

The following design decisions were made to ensure the system meets the project requirements while maintaining simplicity and reliability.

| Component | Design Choice | Reason |
|----------|---------------|-------|
| Transport Protocol | TCP | Ensures reliable communication and ordered message delivery |
| Security | SSL/TLS | Provides encrypted communication between clients and server |
| Concurrency Model | Multi-threaded server | Allows the server to handle multiple clients simultaneously |
| Programming Language | Python | Simplifies socket programming and rapid development |
| Message Ordering | Server-controlled broadcasting | Ensures consistent ordering of messages within each chat room |
| File Transfer | Chunk-based transmission | Enables efficient transfer of file data over TCP connections |

---

# Expected System Behavior

When the system is running, multiple users should be able to connect to the chat server simultaneously and interact within chat rooms in real time.

Messages sent by a client within a chat room will be delivered to all other members of that room while preserving the order of messages. This ensures a consistent communication experience for all users.

Private messaging allows users to send direct messages to specific clients without broadcasting messages to the entire chat room.

The system also supports file transfer between users through the server. All communication between clients and the server is secured using **SSL/TLS encryption**, ensuring data confidentiality and integrity.

---

# Future Improvements

Although the current system focuses on core networking and security features, several improvements can enhance functionality and scalability in future versions.

Possible improvements include:

- Implementing a **user authentication and login system**
- Adding **persistent chat history using a database**
- Developing a **graphical user interface (GUI)** for easier interaction
- Supporting **media file transfers such as images and videos**
- Implementing **distributed server architecture** for improved scalability


## Error Handling and Stability

The system includes several mechanisms to improve stability and reliability.

- Client disconnections are detected and handled gracefully by removing the client from active lists and chat rooms.
- Invalid commands are ignored or result in appropriate error messages.
- Private messages to non-existent users return a "User not found" response.
- Users attempting to send messages without joining a room are prompted to join a room first.
- File transfer errors such as missing files are handled on the client side.
- The server uses multithreading to ensure that one client failure does not affect other active connections.

These mechanisms improve the robustness of the chat system and ensure stable operation under concurrent usage.

## Complete System Overview

```mermaid
graph TD

    C1[Client 1]
    C2[Client 2]
    C3[Client 3]
    C4[Client 4]

    SSL[SSL/TLS Secure Connection]

    Server[Secure Chat Server]

    Rooms[Chat Room Manager]
    File[File Transfer Module]
    PM[Private Messaging Module]

    Room1[Room 1]
    Room2[Room 2]

    C1 --> SSL
    C2 --> SSL
    C3 --> SSL
    C4 --> SSL

    SSL --> Server

    Server --> Rooms
    Server --> File
    Server --> PM

    Rooms --> Room1
    Rooms --> Room2

    Room1 --> C1
    Room1 --> C2

    Room2 --> C3
    Room2 --> C4
