import asyncio
import json
import random
import math
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class GameConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"game_{self.room_name}"
        print('connectedddd!!!!!!!!!!!!!!!!!!')
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        print('disconnecteeeeeed!!!!!!!!!')

    # Receive message from WebSocket
    async def receive(self, text_data):
        game_event = text_data
        # print(game_event)
        if game_event == 'startgame':
            # game_loop_task = asyncio.create_task(self.game_loop())
            await self.start_game()
        elif game_event == 'stopgame':
            await self.stop_game()
        elif game_event == 'pw':
            await self.move_p0_up('press')
        elif game_event == 'ps':
            await self.move_p0_down('press')
        elif game_event == 'pi':
            await self.move_p1_up('press')
        elif game_event == 'pk':
            await self.move_p1_down('press')
        elif game_event == 'rw':
            await self.move_p0_up('release')
        elif game_event == 'rs':
            await self.move_p0_down('release')
        elif game_event == 'ri':
            await self.move_p1_up('release')
        elif game_event == 'rk':
            await self.move_p1_down('release')

    async def game_loop(self):
        while game_state == 'running':
            await self.update_game()
            await asyncio.sleep(0.015625)  # 0.015625

    async def start_game(self):
        global game_state
        game_state = 'running'
        print("freferferer")
        game_loop_task = asyncio.create_task(self.game_loop())

    async def stop_game(self):
        """
        Stops the game
        """
        print('STOPPPPPPPPPPP!!!!!!!!!!!!')
        global game_state
        game_state = 'stopped'
        self.player1Score = 0
        self.player0Score = 0
        self.ballHitCounter = 1
        self.player0 = 200
        self.player1 = 200

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

    async def update_game(self):
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

        await self.update_ball_position()
        self.score = str(self.player0Score) + ' : ' + str(self.player1Score)
        self.ball_speed = math.sqrt(self.ballSpeedX ** 2 + self.ballSpeedY ** 2)
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "game_message",
                "ballX": self.ballX,
                "ballY": self.ballY,
                "ballSpeedX": self.ballSpeedX,
                "ballSpeedY": self.ballSpeedY,
                "score": self.score,
                "player0": self.player0,
                "player1": self.player1,
                "hit": self.hit,
                "ball_speed": self.ball_speed
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

    async def update_ball_position(self):
        self.ballX += self.ballSpeedX
        self.ballY += self.ballSpeedY
        if self.ballX < 0:
            print('player1 ' + str(self.player1Score))
            self.player1Score += 1
            print('GOLOOOOOOOOOOOOOOOOOOOO DO DIREITAAAAAAAA!!!!!!')
            self.ballHitCounter = 1
            self.ballSpeedX = -5
            self.ballSpeedY = random.uniform(-2, 2)
            self.ballX = 750
            self.ballY = random.uniform(20, 370)
            if self.player1Score == 5:
                await self.stop_game()
        elif self.ballX + self.ballSize > self.canvasWidth:
            print('player0 ' + str(self.player0Score))
            self.player0Score += 1
            print('GOLOOOOOOOOOOOOOOOOOOOO DO ESQUERDAAAAAAAA!!!!!!')
            self.ballHitCounter = 1
            self.ballSpeedX = 5
            self.ballSpeedY = random.uniform(-2, 2)
            self.ballX = 50
            self.ballY = random.uniform(20, 370)
            if self.player0Score == 5:
                await self.stop_game()
        elif self.ballY - self.ballSize < 0:
            self.ballY = self.ballSize
            self.ballSpeedY = abs(self.ballSpeedY)
            # self.ballHitCounter += 1
            # self.ballSpeedX *= 1 + (1 / self.ball_hit_counter) / 2.5
            # self.ballSPeedY *= 1 + (1 / self.ball_hit_counter) / 2.5
        elif self.ballY + self.ballSize > self.canvasHeight:
            self.ballY = self.canvasHeight - self.ballSize
            self.ballSpeedY = -abs(self.ballSpeedY)
            # self.ballHitCounter += 1
            # self.ballSpeedX *= 1 + (1 / self.ball_hit_counter) / 2.5
            # self.ballSPeedY *= 1 + (1 / self.ball_hit_counter) / 2.5
        # CHECK COLISION WITH PLAYER 0 PADDLE
        elif self.ballX - self.ballSize < self.paddleWidth and self.ballY > self.player0 and \
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
