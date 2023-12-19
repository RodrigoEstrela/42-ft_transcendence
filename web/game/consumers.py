import asyncio
import json
import random
import math
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class GameConsumer(AsyncWebsocketConsumer):

    connected_clients = {}
    game_state = {}
    game_tasks = {}

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"

        print(self.room_name)
        if self.room_name in self.connected_clients:
            self.game_instance = self.connected_clients[self.room_name]
        else:
            self.connected_clients[self.room_name] = GameInstance()
            self.game_state[self.room_name] = 'waiting'
            self.game_instance = self.connected_clients[self.room_name]

        print('connectedddd!!!!!!!!!!!!!!!!!!')
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print('disconnecteeeeeed!!!!!!!!!')

    # Receive message from WebSocket
    async def receive(self, text_data):
        # print(self.scope['user'])
        game_event = text_data
        # print(game_event)
        if game_event == 'startgame':
            await self.start_game()
        elif game_event == 'stopgame':
            await self.stop_game()
        elif game_event == 'pw':
            await self.game_instance.move_p0_up('press')
        elif game_event == 'ps':
            await self.game_instance.move_p0_down('press')
        elif game_event == 'pi':
            await self.game_instance.move_p1_up('press')
        elif game_event == 'pk':
            await self.game_instance.move_p1_down('press')
        elif game_event == 'rw':
            await self.game_instance.move_p0_up('release')
        elif game_event == 'rs':
            await self.game_instance.move_p0_down('release')
        elif game_event == 'ri':
            await self.game_instance.move_p1_up('release')
        elif game_event == 'rk':
            await self.game_instance.move_p1_down('release')

    async def game_loop(self):
        if self.game_state[self.room_name] == 'running':
            await self.print_countdown()
            for i in range(0, 5):
                print(i)
                await asyncio.sleep(1)
        while self.game_state[self.room_name] == 'running':
            await self.game_instance.update_game(self.game_state, self.room_name)
            await self.send_game_state_to_clients()
            await asyncio.sleep(0.015625)
        self.game_tasks.pop(self.room_name)

    async def print_countdown(self):
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "countdown_message",
                "ballX": self.game_instance.ballX,
                "ballY": self.game_instance.ballY,
                "ballSpeedX": self.game_instance.ballSpeedX,
                "ballSpeedY": self.game_instance.ballSpeedY,
                "score": self.game_instance.score,
                "player0": self.game_instance.player0,
                "player1": self.game_instance.player1,
                "hit": self.game_instance.hit,
                "ball_speed": self.game_instance.ball_speed
            }
        )

    async def countdown_message(self, event):
        # This method is called when the group receives a message
        await self.send(text_data=json.dumps({
            "type": "countdown_message",
            "ballX": event["ballX"],
            "ballY": event["ballY"],
            "ballSpeedX": event["ballSpeedX"],
            "ballSpeedY": event["ballSpeedY"],
            "score": event["score"],
            "player0": event["player0"],
            "player1": event["player1"],
            "hit": event["hit"],
            "ball_speed": event["ball_speed"]
        }))

    async def start_game(self):
        if self.game_state[self.room_name] == 'ready':
            self.game_state[self.room_name] = 'running'
        else:
            self.game_state[self.room_name] = 'ready'
        if self.room_name in self.connected_clients:
            self.game_instance = self.connected_clients[self.room_name]
        else:
            self.connected_clients[self.room_name] = GameInstance()
            self.game_instance = self.connected_clients[self.room_name]
        if self.room_name not in self.game_tasks:
            self.game_tasks[self.room_name] = asyncio.create_task(self.game_loop())

    async def stop_game(self):
        """
        Stops the game
        """
        print('STOPPPPPPPPPPP!!!!!!!!!!!!')
        self.game_state[self.room_name] = 'stopped'

    async def send_game_state_to_clients(self):
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "game_message",
                "ballX": self.game_instance.ballX,
                "ballY": self.game_instance.ballY,
                "ballSpeedX": self.game_instance.ballSpeedX,
                "ballSpeedY": self.game_instance.ballSpeedY,
                "score": self.game_instance.score,
                "player0": self.game_instance.player0,
                "player1": self.game_instance.player1,
                "hit": self.game_instance.hit,
                "ball_speed": self.game_instance.ball_speed
            }
        )

    async def game_message(self, event):
        # This method is called when the group receives a message
        await self.send(text_data=json.dumps({
            "type": "game_message",
            "ballX": event["ballX"],
            "ballY": event["ballY"],
            "ballSpeedX": event["ballSpeedX"],
            "ballSpeedY": event["ballSpeedY"],
            "score": event["score"],
            "player0": event["player0"],
            "player1": event["player1"],
            "hit": event["hit"],
            "ball_speed": event["ball_speed"]
        }))


class GameInstance:
    playersReady = 0
    ballSize = 5
    ballX = 50
    ballY = 50
    ballSpeedX = 5
    ballSpeedY = 2
    ballMaxSpeed = 40
    canvasWidth = 800
    canvasHeight = 400
    player0 = 200
    player1 = 200
    score = "2:4"
    paddleHeight = 110
    paddleWidth = 15
    player0Score = 0
    player1Score = 0
    ballHitCounter = 1
    hit = 0
    p0Moving = 0
    p1Moving = 0
    ball_speed = 0

    async def move_p0_up(self, state):
        if state == 'press':
            self.p0Moving = -1
        elif state == 'release':
            self.p0Moving = 0

    async def move_p0_down(self, state):
        if state == 'press':
            self.p0Moving = 1
        elif state == 'release':
            self.p0Moving = 0

    async def move_p1_up(self, state):
        if state == 'press':
            self.p1Moving = -1
        elif state == 'release':
            self.p1Moving = 0

    async def move_p1_down(self, state):
        if state == 'press':
            self.p1Moving = 1
        elif state == 'release':
            self.p1Moving = 0

    async def update_game(self, game_state, room_name):
        """
        Updates the game state
        """
        if self.p0Moving == 1:
            self.player0 += 10
        elif self.p0Moving == -1:
            self.player0 -= 10
        if self.p1Moving == 1:
            self.player1 += 10
        elif self.p1Moving == -1:
            self.player1 -= 10
        if self.player0 < 0:
            self.player0 = 0
        if self.player0 + self.paddleHeight > self.canvasHeight:
            self.player0 = self.canvasHeight - self.paddleHeight
        if self.player1 < 0:
            self.player1 = 0
        if self.player1 + self.paddleHeight > self.canvasHeight:
            self.player1 = self.canvasHeight - self.paddleHeight

        await self.update_ball_position(game_state, room_name)

        self.score = str(self.player0Score) + ' : ' + str(self.player1Score)

        self.ball_speed = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)

    async def update_ball_position(self, game_state, room_name):
        self.ballX += self.ballSpeedX
        self.ballY += self.ballSpeedY

        # CHECK COLISION WITH PLAYER 0 PADDLE
        if self.ballX - self.ballSize < self.paddleWidth and self.ballY > self.player0 and \
             self.ballY < self.player0 + self.paddleHeight:
            paddleHit = (self.ballY - self.player0) / self.paddleHeight
            deviate = (2 * ((paddleHit - 0.5) ** 2)) + 1
            if paddleHit < 0.5:
                deviate *= -1
            self.ballX = self.paddleWidth + self.ballSize
            self.ballSpeedX = abs(self.ballSpeedX)
            self.ballHitCounter += 1
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            self.ballSpeedX *= 1 + (1 / self.ballHitCounter) / 2
            self.ballSpeedY *= 1 + (1 / self.ballHitCounter) / 2
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            angle = math.pi / 14 * deviate
            magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
            # print('SPEED: ' + str(magnitude))
            normalizedSpeedX = self.ballSpeedX / magnitude
            normalizedSpeedY = self.ballSpeedY / magnitude
            self.ballSpeedX = normalizedSpeedX * math.cos(angle) - normalizedSpeedY * math.sin(angle)
            self.ballSpeedY = normalizedSpeedX * math.sin(angle) + normalizedSpeedY * math.cos(angle)
            self.ballSpeedX *= magnitude
            self.ballSpeedY *= magnitude
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
            # print('SPEED: ' + str(magnitude))
            # print("#############################")
            self.hit = 1

    # CHECK COLISION WITH PLAYER 1 PADDLE
        elif self.ballX + self.ballSize > self.canvasWidth - self.paddleWidth and \
             self.ballY > self.player1 and self.ballY < self.player1 + self.paddleHeight:
            paddleHit = (self.ballY - self.player1) / self.paddleHeight
            deviate = (2 * ((paddleHit - 0.5) ** 2)) + 1
            if paddleHit > 0.5:
                deviate *= -1
            self.ballX = self.canvasWidth - self.paddleWidth - self.ballSize
            self.ballSpeedX = -abs(self.ballSpeedX)
            self.ballHitCounter += 1
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            self.ballSpeedX *= 1 + (1 / self.ballHitCounter) / 2
            self.ballSpeedY *= 1 + (1 / self.ballHitCounter) / 2
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            angle = math.pi / 14 * deviate
            magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
            # print('SPEED: ' + str(magnitude))
            normalizedSpeedX = self.ballSpeedX / magnitude
            normalizedSpeedY = self.ballSpeedY / magnitude
            self.ballSpeedX = normalizedSpeedX * math.cos(angle) - normalizedSpeedY * math.sin(angle)
            self.ballSpeedY = normalizedSpeedX * math.sin(angle) + normalizedSpeedY * math.cos(angle)
            self.ballSpeedX *= magnitude
            self.ballSpeedY *= magnitude
            # print('ballSpeedX ' + str(self.ballSpeedX))
            # print('ballSpeedY ' + str(self.ballSpeedY))
            magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
            # print('SPEED: ' + str(magnitude))
            # print("#############################")
            self.hit = 1

        # GOLOS
        if self.ballX < 0:
            self.player1Score += 1
            print('GOLOOOOOOOOOOOOOOOOOOOO DO DIREITAAAAAAAA!!!!!!')
            self.ballHitCounter = 1
            self.ballSpeedX = -5
            self.ballSpeedY = random.uniform(-2, 2)
            self.ballX = 750
            self.ballY = random.uniform(20, 370)
            if self.player1Score == 5:
                self.player1Score = 0
                self.player0Score = 0
                self.player0 = 200 - self.paddleHeight / 2
                self.player1 = 200 - self.paddleHeight / 2
                game_state[room_name] = 'ola'
        elif self.ballX + self.ballSize > self.canvasWidth:
            self.player0Score += 1
            print('GOLOOOOOOOOOOOOOOOOOOOO DO ESQUERDAAAAAAAA!!!!!!')
            self.ballHitCounter = 1
            self.ballSpeedX = 5
            self.ballSpeedY = random.uniform(-2, 2)
            self.ballX = 50
            self.ballY = random.uniform(20, 370)
            if self.player0Score == 5:
                self.player1Score = 0
                self.player0Score = 0
                self.player0 = 200 - self.paddleHeight / 2
                self.player1 = 200 - self.paddleHeight / 2
                game_state[room_name] = 'ola'
        elif self.ballY - self.ballSize < 0:
            self.ballY = self.ballSize
            self.ballSpeedY = abs(self.ballSpeedY)
        elif self.ballY + self.ballSize > self.canvasHeight:
            self.ballY = self.canvasHeight - self.ballSize
            self.ballSpeedY = -abs(self.ballSpeedY)

        # # CHECK COLISION WITH PLAYER 0 PADDLE
        # elif self.ballX - self.ballSize < self.paddleWidth and self.ballY > self.player0 and \
        #         self.ballY < self.player0 + self.paddleHeight:
        #     paddleHit = (self.ballY - self.player0) / self.paddleHeight
        #     deviate = (2 * ((paddleHit - 0.5) ** 2)) + 1
        #     if paddleHit < 0.5:
        #         deviate *= -1
        #     self.ballX = self.paddleWidth + self.ballSize
        #     self.ballSpeedX = abs(self.ballSpeedX)
        #     self.ballHitCounter += 1
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     self.ballSpeedX *= 1 + (1 / self.ballHitCounter) / 2
        #     self.ballSpeedY *= 1 + (1 / self.ballHitCounter) / 2
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     angle = math.pi / 14 * deviate
        #     magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
        #     # print('SPEED: ' + str(magnitude))
        #     normalizedSpeedX = self.ballSpeedX / magnitude
        #     normalizedSpeedY = self.ballSpeedY / magnitude
        #     self.ballSpeedX = normalizedSpeedX * math.cos(angle) - normalizedSpeedY * math.sin(angle)
        #     self.ballSpeedY = normalizedSpeedX * math.sin(angle) + normalizedSpeedY * math.cos(angle)
        #     self.ballSpeedX *= magnitude
        #     self.ballSpeedY *= magnitude
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
        #     # print('SPEED: ' + str(magnitude))
        #     # print("#############################")
        #     self.hit = 1
        # # CHECK COLISION WITH PLAYER 1 PADDLE
        # elif self.ballX + self.ballSize > self.canvasWidth - self.paddleWidth and \
        #         self.ballY > self.player1 and self.ballY < self.player1 + self.paddleHeight:
        #     paddleHit = (self.ballY - self.player1) / self.paddleHeight
        #     deviate = (2 * ((paddleHit - 0.5) ** 2)) + 1
        #     if paddleHit > 0.5:
        #         deviate *= -1
        #     self.ballX = self.canvasWidth - self.paddleWidth - self.ballSize
        #     self.ballSpeedX = -abs(self.ballSpeedX)
        #     self.ballHitCounter += 1
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     self.ballSpeedX *= 1 + (1 / self.ballHitCounter) / 2
        #     self.ballSpeedY *= 1 + (1 / self.ballHitCounter) / 2
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     angle = math.pi / 14 * deviate
        #     magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
        #     # print('SPEED: ' + str(magnitude))
        #     normalizedSpeedX = self.ballSpeedX / magnitude
        #     normalizedSpeedY = self.ballSpeedY / magnitude
        #     self.ballSpeedX = normalizedSpeedX * math.cos(angle) - normalizedSpeedY * math.sin(angle)
        #     self.ballSpeedY = normalizedSpeedX * math.sin(angle) + normalizedSpeedY * math.cos(angle)
        #     self.ballSpeedX *= magnitude
        #     self.ballSpeedY *= magnitude
        #     # print('ballSpeedX ' + str(self.ballSpeedX))
        #     # print('ballSpeedY ' + str(self.ballSpeedY))
        #     magnitude = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
        #     # print('SPEED: ' + str(magnitude))
        #     # print("#############################")
        #     self.hit = 1
