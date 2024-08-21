from _thread import *
import socket
import pickle
import pygame
import random

ball = pygame.Rect(250, 250, 10, 10)
ball.center = 300, 250
ballvelx = 2
ballvely = 2

p1_score = 0
p2_score = 0

clock = pygame.time.Clock()


def ball_move(ball, p1, p2):
    global ballvelx, ballvely, p1_score, p2_score

    ball.x += ballvelx
    ball.y += ballvely

    if ball.left <= 0:
        #ballvelx *= -1
        p2_score += 1
        ball.center = 250, 250
        #print(random.choice([-1, 1]))
        ballvelx *= random.choice([-1, 1])

    if ball.right >= 500:
        #ballvelx *= -1
        p1_score += 1
        ball.center = 250, 250
        ballvelx *= random.choice([-1, 1])
    # if ball.colliderect(p1) or ball.colliderect(p2):
    #    ballvelx *= -1

    if ballvelx < 0:  # ball moving towards left
        if ball.y >= p1.y and ball.y <= p1.y + 100:  # ball.y within range of y of paddle
            if ball.x <= p1.x + 15:
                ballvelx *= -1
                middle_y = p1.y + 50
                diff_y = middle_y - ball.y
                reduction = 25
                y_vel = diff_y / reduction
                print(y_vel)
                ballvely = -1 * y_vel

    else:
        if ball.y >= p2.y and ball.y <= p2.y + 100:  # ball.y within range of y of paddle
            if ball.x + 10 >= p2.x:
                ballvelx *= -1
                middle_y = p2.y + 50
                diff_y = middle_y - ball.y
                reduction = 25
                y_vel = diff_y / reduction
                print(y_vel)
                ballvely = -1 * y_vel

    if ball.bottom >= 500 or ball.top <= 0:
        ballvely *= -1
        #ball.y = 500


ip = "192.168.1.8"
port = 5555
currentPlayer = 0
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_socket.bind((ip, port))
except:
    server_socket.bind((ip, port+1))

server_socket.listen()

pos_list = [(0, 0), (485, 0)]


def threaded_client(conn, player):
    global currentPlayer, ball, p1_score, p2_score
    x = pos_list[player]
    if player == 0:
        conn.sendall(pickle.dumps([x, 0]))  # Initial
    else:
        conn.sendall(pickle.dumps([x, 1]))
        # sendall sends all data
        # conn.send(pickle.dumps(x))
    reply = ''

    while True:  # Receiving Block
        clock.tick(120)
        # print(conn.recv(2048))
        data = conn.recv(2048*16)  # current player client is being sent
        #print("data", pickle.loads(data))

        if not data:  # Constantly sending data every second
            break  # no data break
            print("LOST CONNECTION")
        else:
            pos_list[player] = pickle.loads(data)

            p1 = pygame.Rect(pos_list[0][0], pos_list[0][1], 15, 100)
            p2 = pygame.Rect(pos_list[1][0], pos_list[1][1], 15, 100)
            # print("p1, p2", p1, p2)

            ball_move(ball, p1, p2)

            print("Receiving", pickle.loads(data))
            if player == 0:  # Sending other players data
                # print(currentPlayer)
                if currentPlayer == 1:
                    reply = [pos_list[1], [p1_score, p2_score], ball]
                else:
                    reply = [pos_list[1], [p1_score, p2_score], ball]
            else:
                reply = [pos_list[0], [p1_score, p2_score], ball]
            print("Sending", reply)
        conn.sendall(pickle.dumps(reply))  # p2 play
        print(p1_score, p2_score)
        # send all sends all of the data
    print("client disconnected")
    conn.close()


while True:
    conn, addr = server_socket.accept()
    print("Connection from", addr)
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
