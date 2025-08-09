# Bombarman
[![GitHub contributors](https://img.shields.io/github/contributors/jeetpatel1113/Bombarman?color=red)](https://github.com/jeetpatel1113/Bombarman/graphs/contributors)
[![GitHub stars](https://badgen.net/github/stars/jeetpatel1113/Bombarman)](https://github.com/jeetpatel1113/Bombarman/stargazers)
![Licence](https://img.shields.io/badge/Licence-MIT-green)

Multiplayer game build by [Brendokim](https://www.google.com/search?q=https://github.com/brendokim), [Jeet](https://www.google.com/search?q=https://github.com/jeetpatel1113), [Leo](https://www.google.com/search?q=https://github.com/ljbds66), [Sam](https://www.google.com/search?q=https://github.com/SamShowkati) as a part of CMPT 371 Project, Group no. 22.

Bombarman is a multiplayer game 🎮 that combines classic arcade action with networking capabilities, allowing players to compete ⚔️ in a destructive arena. The goal is to strategically place bombs 💣 to destroy blocks and eliminate opponents.

The project is developed in Python 💻 and uses Pygame for graphics and sockets for network communication. It's a great example of a simple but engaging multiplayer game built from the ground up.

## Table of Contents
1. [Installation](#installation)
2. [Application Features](#application-features)
3. [Licence](#licence)
4. [Acknowledgements](#acknowledgements)

## Installation
1. Make sure you have the following libraries in python:
     - json
     - pygame
     - socket
     - sys
     - threading
     - time

    If not, run the following code in your terminal:

    
        pip install pygame
        pip install json
        pip install socket
        pip install sys
        pip install threading
        pip install time
    
2. Clone the repository using the following command-
    ```bash
    git clone git@github.com:jeetpatel1113/Bombarman.git
    ```
3. In server.py, change SERVER_IP to your IPv4 address.
   ```vscode
   SERVER_IP = 'your-IPv4 address'
   SERVER_PORT = 5555
   ```
4. (Server host only) Forward TCP port 5555 on your router to your machine's IPv4 address so clients outside your network can connect.
5. From the main directory ( .\..\Bombarman> ), run the following code to start your server:
   ```
   python -m Networking.server
   ```
6. In client.py, change SERVER_IP to the server host's public IP address.
   ```vscode
   SERVER_IP = 'server-public-IP'
   SERVER_PORT = 5555
   ```
   For the server host, change SERVER_IP to your IPv4 address.
7. From the main directory (.\..\Bombarman> ), run the following code to start your client:
   ```
   python -m Networking.client
   ```
8. Wait for atleast 2 clients to join the server to start the game.
9. Make sure you enjoy playing. 🙂

## Application Features

<img width="1595" height="1021" alt="image" src="https://github.com/user-attachments/assets/b572a24c-0702-4f94-b1c6-4b9ec929996e" />

It is a multiplayer game, super fun and competitive game. 🎉🎉🎉

Basically you have to blow up other members in the team.🔥🔥🔥

This project of ours shows **Networking, Socket Programming, Locking of Objects and Sharing Medium** in the same board.🛜 We used **TCP** to transfer messages back and forth 🤝, since every key is highly important.ℹ️

We tried ourselves, and trust me, no better feeling than making and playing your own game. Here is a video of our accomplishment. Hope you enjoy.📽️
[Bombarman - SFU CMPT371 Group 22 Final Project Demo](https://www.youtube.com/watch?v=kovifcCMMUI&ab_channel=brendonKim)

[![Watch the video](https://img.youtube.com/vi/kovifcCMMUI/maxresdefault.jpg)](https://www.youtube.com/watch?v=kovifcCMMUI)


## Licence
Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.

## Acknowledgements
Resources:
     
- [Pygame](https://www.pygame.org/docs/)
- [Socket Programming](https://docs.python.org/3/library/socket.html)
- [Threading](https://docs.python.org/3/library/threading.html)
- [Time](https://docs.python.org/3/library/time.html)
- CMPT 371 - Data Communications and Networking, [Simon Fraser University](https://www.sfu.ca/)
