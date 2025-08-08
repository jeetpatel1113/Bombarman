# Bombarman
[![GitHub contributors](https://img.shields.io/github/contributors/jeetpatel1113/Bombarman?color=red)](https://github.com/jeetpatel1113/Bombarman/graphs/contributors)
[![GitHub stars](https://badgen.net/github/stars/jeetpatel1113/Bombarman)](https://github.com/jeetpatel1113/Bombarman/stargazers)
![Licence](https://img.shields.io/badge/Licence-MIT-green)

Multiplayer game build by [Brendokim](https://www.google.com/search?q=https://github.com/brendokim), [Jeet](https://www.google.com/search?q=https://github.com/jeetpatel1113), [Leo](https://www.google.com/search?q=https://github.com/ljbds66), [Sam](https://www.google.com/search?q=https://github.com/SamShowkati) as a part of CMPT 371 Project, Group no. 22.

Bombarman is a multiplayer game that combines classic arcade action with networking capabilities, allowing players to compete in a destructive arena. The goal is to strategically place bombs to destroy blocks and eliminate opponents.

The project is developed in Python and uses Pygame for graphics and sockets for network communication. It's a great example of a simple but engaging multiplayer game built from the ground up.

## Table of Contents
1. [Contant](#Contant)
2. [Things we used](#things-we-used)
3. [Application Features](#application-features)
4. [Licence](#licence)
5. [Acknowledgements](#acknowledgements)

## Contant 
To setup the project locally, follow the instructions below-

### Installation
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
3. Change server's SERVER_IP and SERVER_PORT to your IPv4 address.
   ```vscode
   SERVER_IP = 'localhost' // Change your localhost to your IPv4 address.
   SERVER_PORT = 5555
   ```
4. From server's directory Bombarman ( .\..\Bombarman> ), run the following code to start your server:
   ```
   python -m Networking.server
   ```
5. Now, your server has started, use the server's address in client and make sure it is on the same port on different machine.
6. From client's directory Bombarman (.\..\Bombarman> ), run the following code to start your client:
   ```
   python -m Networking.client
   ```
7. Wait for atleast 2 clients to join the server to start the game.
8. Make sure you enjoy playing. 🙂

   
