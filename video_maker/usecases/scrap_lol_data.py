import os
from time import sleep
from selenium.webdriver.common.by import By
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData, Player
from usecases.data import save


class ScrapLolData(DataScrapper):
    def __init__(self) -> None:
        super().__init__()
        # URL
        self.__replay_file_dir = r'C:\youtube\lol\replays'
        self.__url = 'https://www.leagueofgraphs.com/replays/with-high-kda/grandmaster/sr-ranked'
        self.__champions_xpath_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "relative", " " ))]//img'
        self.__match_table_selector = '//*[contains(concat( " ", @class, " " ), concat( " ", "matchTable", " " ))]'
        self.__items_xpath_selector = '//td[contains(concat( " ", @class, " " ), concat( " ", "itemsColumn", " " ))]'
        self.__region_xpath = '//*[(@id = "mainContent")]//a'
        self.__watch_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replay_watch_button", " " ))]'
        self.__download_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "replayDownloadButton", " " ))]'
        self.match_data: MatchData = {
            "team1": {
                "players": []
            },
            "team2": {
                "players": []
            }
        }

    def get_match_data_and_download_replay(self) -> None:
        print('Acessando site e salvando informações...')
        self.driver.get(self.__url)
        table = self.driver.find_element(by=By.XPATH, value=self.__match_table_selector)
        
        # Identify and extract text inside <a> tags with class 'subname' from the context of the table
        subname_texts = [e.text for e in self.driver.find_elements(by=By.XPATH, value=f'{self.__match_table_selector}//a[contains(concat(" ", @class, " "), concat( " ", "subname", " " ))]')]
        
        # Removing subname texts from table's text
        table_text = table.text
        for subname_text in subname_texts:
            table_text = table_text.replace('\n' + subname_text + '\n', '\n')
        
        text_list = table_text.split('\n')
        self.match_data['team1']['result'] = text_list[0].split(' ')[0]
        self.match_data['team2']['result'] = text_list[0].split(' ')[-1]
        duration = text_list[0].split(' ')[3][1:-1]
        self.match_data['duration'] = duration
        patch = text_list[-1].split(' ')[1][1:-1]
        self.match_data['patch'] = patch
        elements = self.driver.find_elements(
            by=By.XPATH, value=self.__champions_xpath_selector)
        elements[0].get_dom_attribute('title')
        (champions, spells, runes) = self.__get_champions_names(elements=elements)

        # Exctract items and spells
        items_elements = self.driver.find_elements(
            by=By.XPATH, value=f'{self.__match_table_selector}{self.__items_xpath_selector}')
        items = []
        for item in items_elements:
            raw_items = item.find_elements(by=By.CLASS_NAME, value="requireTooltip")
            item_classes = []
            for raw_item in raw_items:
                item_classes.append(raw_item.get_dom_attribute("class").split(" ")[1])
            items.append(item_classes)

        self.match_data['team1']['players'] = self.__create_team_one(
            text_list=text_list, champions=champions, items=items, spells=spells, runes=runes)
        self.match_data['team2']['players'] = self.__create_team_two(
            text_list=text_list, champions=champions, items=items, spells=spells, runes=runes)
        mvp_data = self.__get_mvp_data(self.match_data)
        self.match_data['mvp'] = self.match_data[mvp_data['team']
                                                 ]['players'][mvp_data['player_index']]
        self.match_data['mvp']['role'] = mvp_data['player_role']
        self.match_data['loser'] = self.match_data[mvp_data['loser_team']
                                                   ]['players'][mvp_data['player_index']]['champion']
        self.match_data['player_role'] = mvp_data['player_role']
        self.match_data['player_index'] = str(
            int(mvp_data['player_index']) + 1)
        region_link = self.driver.find_element(
            by=By.XPATH, value=self.__region_xpath)
        link_array = region_link.get_property('href').split('/')
        self.match_data['region'] = link_array[4].upper()
        # Save Data
        save(self.match_data)
        print('Informações salvas')
        print('Iniciando download da partida')
        self.__remove_match()
        self.__download_match()
        self.quit()

    def __get_champions_names(self, elements: list) -> (list[str], list[str], list[str]):
        champions = []
        spells = []
        rune = []
        for i in range(0, 40):
            if elements[i].get_dom_attribute('title') is not None:
                champions.append(elements[i].get_dom_attribute('title'))
            elif "perk" in elements[i].get_dom_attribute('class'):
                rune.append(elements[i].get_dom_attribute('class').split(" ")[0])
            else:
                spells.append(elements[i].get_dom_attribute('class').split(" ")[1])
        spells = [[spells[i], spells[i+1]] for i in range(0, len(spells), 2)]
        return (champions, spells, rune)

    def __create_player(self, name: str, kda: str, rank: str, champion: str, items: list, spells: list, rune:str) -> Player:
        kdas = kda.split(' / ')
        return {
            "name": name,
            "k": kdas[0], "d": kdas[1], "a": kdas[2],
            "rank": rank,
            "champion": champion,
            "items": items,
            "spells": spells,
            "rune": rune
        }

    def __create_team_one(self, text_list: list, champions: list, items: list, spells: list, runes:str) -> list[Player]:
        team_one = []
        team_one.append(self.__create_player(
            name=text_list[1], kda=text_list[3], rank=text_list[2], champion=champions[0], items=items[0], spells=spells[0], rune=runes[0]))
        team_one.append(self.__create_player(
            name=text_list[9], kda=text_list[11], rank=text_list[10], champion=champions[2], items=items[2], spells=spells[2], rune=runes[2]))
        team_one.append(self.__create_player(
            name=text_list[17], kda=text_list[19], rank=text_list[18], champion=champions[4], items=items[4], spells=spells[4], rune=runes[4]))
        team_one.append(self.__create_player(
            name=text_list[25], kda=text_list[27], rank=text_list[26], champion=champions[6], items=items[6], spells=spells[6], rune=runes[6]))
        team_one.append(self.__create_player(
            name=text_list[33], kda=text_list[35], rank=text_list[34], champion=champions[8], items=items[8], spells=spells[8], rune=runes[8]))
        return team_one

    def __create_team_two(self, text_list: list, champions: list, items: list, spells: list, runes:str) -> list[Player]:
        team_two = []
        team_two.append(self.__create_player(
            name=text_list[7], kda=text_list[5], rank=text_list[8], champion=champions[1], items=items[1], spells=spells[1], rune=runes[1]))
        team_two.append(self.__create_player(
            name=text_list[15], kda=text_list[13], rank=text_list[16], champion=champions[3], items=items[3], spells=spells[3], rune=runes[3]))
        team_two.append(self.__create_player(
            name=text_list[23], kda=text_list[21], rank=text_list[24], champion=champions[5], items=items[5], spells=spells[5], rune=runes[5]))
        team_two.append(self.__create_player(
            name=text_list[31], kda=text_list[29], rank=text_list[32], champion=champions[7], items=items[7], spells=spells[7], rune=runes[7]))
        team_two.append(self.__create_player(
            name=text_list[39], kda=text_list[37], rank=text_list[40], champion=champions[9], items=items[9], spells=spells[9], rune=runes[9]))
        return team_two

    def __get_mvp_data(self, match_data):
        team = ''
        kdas = []
        if match_data['team1']['result'] == 'Victory':
            for player in match_data['team1']['players']:
                team = 'team1'
                loser_team = 'team2'
                kdas.append(int(player['k'].split(' ')[0]))
        else:
            for player in match_data['team2']['players']:
                team = 'team2'
                loser_team = 'team1'
                kdas.append(int(player['k'].split(' ')[0]))
        player_index = kdas.index(max(kdas))
        roles = ['Top', 'Jungle', 'Mid', 'ADC', 'Support']
        return {
            "team": team,
            "player_index": player_index,
            "loser_team": loser_team,
            "player_role": roles[player_index]
        }

    def __download_match(self):
        watch_button = self.driver.find_element(
            by=By.XPATH, value=self.__watch_xpath)
        download_button = self.driver.find_element(
            by=By.XPATH, value=self.__download_xpath)
        self.driver.execute_script("arguments[0].click();", watch_button)
        sleep(1)
        self.driver.execute_script("arguments[0].click();", download_button)
        sleep(2)

    def __remove_match(self):
        file = os.listdir(self.__replay_file_dir)
        if file:
            os.remove(os.path.join(self.__replay_file_dir, file[0]))
