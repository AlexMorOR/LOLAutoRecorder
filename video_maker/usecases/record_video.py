import os
import psutil
from time import sleep
import subprocess
import pyautogui
import pydirectinput
import requests
from entities.match_data import MatchData


class RecordVideo:
    def __init__(self, match_data: MatchData) -> None:
        self.__video_file_dir = r'C:\youtube\Joao\Videos'
        self.__replay_file_dir = r'C:\youtube\lol\replays'
        self.__match_data = match_data

    def record(self):
        # self.__show_mouse_position()
        print('Старт записи...')
        self.__run_game()
        sleep(50)
        # Настройка рендера и выбор игрока
        process = self.__get_process_id()
        print('Реплей запущен, id процесса = ' + str(process))
        sleep(5)
        # Запись игры
        duration = self.__duration_in_seconds()
        self.__start_stop_recording(True)
        self.__configure_render()
        sleep(5)
        self.__select_player()
        print('Продолжительность записи = ' + str(int(duration / 60)) + ':' + str(int(duration % 60)))
        sleep(duration + 10)
        self.__start_stop_recording(False)
        # Закрытие клиента
        self.__kill_process(id=process)
        print('Запись закончена.')
        sleep(15)
        return self.__select_video_file()

    def __run_game(self):
        file = os.listdir(self.__replay_file_dir)[0]
        subprocess.call(
            ['start', fr'{self.__replay_file_dir}\{file}'], shell=True)

    def __select_player(self):
        if self.__match_data['team1']['result'] == 'Victory':
            pydirectinput.keyDown('f1')
            pydirectinput.keyUp('f1')
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            pydirectinput.keyDown('f2')
            pydirectinput.keyUp('f2')
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])

    def __start_stop_recording(self, start:bool):
        url = "https://127.0.0.1:2999/replay/recording"
        recording_config = {
            "recording": start,
            "codec": "webm",
            "startTime": 0,
            "path": "C:\\youtube\\Joao\\Videos"
        }
        response = requests.post(url=url, json=recording_config, verify=False).json()
        print(response)


    def __get_process_id(self) -> int:
        url = "https://127.0.0.1:2999/replay/game"
        response = requests.get(url=url, verify=False).json()
        return response['processID']

    def __kill_process(self, id):
        psutil.Process(id).kill()

    def __configure_render(self):
        url = "https://127.0.0.1:2999/replay/render"
        render_config = {
            "interfaceAll":True,
            "interfaceAnnounce":True,
            "interfaceChat":True,
            "interfaceFrames":True,
            "interfaceKillCallouts":True,
            "interfaceMinimap":True,
            "interfaceNeutralTimers":False,
            "interfaceQuests":False,
            "interfaceReplay":False,
            "interfaceScore":True,
            "interfaceScoreboard":True,
            "interfaceTarget":True,
            "interfaceTimeline":False
        }
        response = requests.post(url=url, json=render_config, verify=False).json()

    def __duration_in_seconds(self) -> int:
        array = self.__match_data['duration'].split(':')
        return (int(array[0]) * 60) + int(array[1])

    def __show_mouse_position(self):
        while True:
            print(pyautogui.position())
            sleep(1)

    def __wait_end_of_recording(self):
        url = "https://127.0.0.1:2999/replay/recording"
        while(True):
            response = requests.get(url=url, verify=False).json()
            print(f'recording: {response["recording"]};\tcurrentTime: {response["currentTime"]};\tendTime: {response["endTime"]}');
            if(response["recording"]):
                sleep(10)
            else:
                return

    def get_last_video_file(self):
        self.__select_video_file()
    def __select_video_file(self):
        file = os.listdir(self.__video_file_dir)
        return file[0]

    def remove_video_file(self):
        files = os.listdir(self.__video_file_dir)
        for file in files:
            os.remove(os.path.join(self.__video_file_dir, file))
        #os.rename(os.path.join(self.__video_file_dir, file[0]), os.path.join(
        #    self.__video_file_dir, 'shorts', file[0]))
