import os
from time import sleep
from entities.data_scrapper import DataScrapper
from entities.match_data import MatchData


class CreateThumbnail:
    def __init__(self, data_scrapper: DataScrapper, data: MatchData) -> None:
        self.scrapper = data_scrapper
        self.lol_data = data
        self.__thumb_path = r'C:\youtube\lol\thumb\thumb.png'

    def create_thumbnail(self):
        print('Criando thumbnail...')
        champion = self.lol_data['mvp']['champion'].replace(
            "'", "").capitalize()
        champion = self.lol_data['mvp']['champion'].replace(
            " ", "")
        self.__create_html(
            kda=self.lol_data['mvp']['kda'],
            imgUrl=f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champion}_0.jpg',
            mvp=self.lol_data['mvp']['champion'],
            vs=self.lol_data['loser'],
            region=self.lol_data['region'],
            patch=self.lol_data['patch']
        )
        html_path = os.path.abspath('assets/thumbnail.html')
        self.scrapper.driver.get('file://' + html_path)
        sleep(2)
        self.scrapper.driver.set_window_size(1280, 805)
        self.scrapper.driver.save_screenshot(self.__thumb_path)
        print('Thumbnail criada!')
        self.scrapper.driver.quit()

    def __create_html(self, 
                      k:str, d:str, a:str ,
                      heroName: str, enemyName: str, heroSkin: str,
                      sumSpell1:str, sumSpell2:str,
                      item1:str, item2:str, item3:str, item4:str, item5:str, item6:str,
                      position:str,
                      region: str, patch: str):
        HTML = """
<!DOCTYPE html>
<html>
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;800&display=swap" rel="stylesheet">
    <link data-react-helmet="true" rel="stylesheet" href="https://lolstatic-a.akamaihd.net/webfonts/live/css/fonts/beaufortforlol.css">
    <style>
        * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Beaufort for LOL";
        }
        .back{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"""+ heroName +"""_"""+ heroSkin +""".jpg');
        }
        .p1{
            background-image: url('http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/"""+ heroName +""".png');
        }
        .p2{
            background-image: url('http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/"""+ enemyName +""".png');
        }
        .ss1{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/spell/"""+ sumSpell1 +""".png');
        }
        .ss2{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/spell/"""+ sumSpell2 +""".png');
        }
        .item1{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item1 +""".png');
        }
        .item2{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item2 +""".png');
        }
        .item3{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item3 +""".png');
        }
        .item4{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item4 +""".png');
        }
        .item5{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item5 +""".png');
        }
        .item6{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/13.21.1/img/item/"""+ item6 +""".png');
        }
        .container {
        background-size: cover;
        width: 1280px;
        height: 720px;
        display: flex;
        align-items: center;
        }
        .frame {
        width: 500px;
        height: 600px;
        margin-left: 50px;
        background: linear-gradient(#000000c8, #0000001e);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        font-weight: 800;
        border-radius: 60px;
        }
        .match {
        display: flex;
        flex-direction: column;
        align-items: center;
        color: white;
        font-size: 3rem;
        }
        .mvp {
        font-size: 5rem;
        text-transform: uppercase;
        }
        .role {
        font-size: 2rem;
        text-transform: uppercase;
        }
        .region {
        background-color: aquamarine;
        color: #444;
        padding: .5rem 1.5rem;
        border-radius: 2rem;
        font-size: 2rem;
        }
        .vs{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        font-size: 60px;
        color: #F0E6D2;
        width: 80%;
        }
        .items{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        font-size: 60px;
        color: #F0E6D2;
        width: 90%;
        }
        .items .item{
            width: 50px;
            height: 50px;
            background-size: 50px;
        }
        .items .summoner{
            width: 50px;
            height: 50px;
            background-size: 50px;
            border-radius: 50%;
        }
        .kda {
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-around;
        font-size: 60px;
        color: #F0E6D2;
        width: 50%;
        }
        .kda .stat{
            width: 70px;
            height: 70px;
            background-size: 50px;
            border-radius: 50%;
            border: 1px solid #F0E6D2;
            font-size: 45px;
            background-color: #000000AA;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .heroe-icon{
            border-radius: 50%; 
            height: 100px;
            width: 100px;
            background-size: 110px;
            background-position: center;
        }
    </style>
    </head>
<body>
    <div class="container back">
    <div class="frame">
        <div class="vs">
            <div class="heroe-icon p1"></div>
            <div>
            <p>VS</p>
            </div>
            <div class="heroe-icon p2"></div>
        </div>
        <div class="match">
        <p class="mvp">"""+ heroName +"""</p>
        <p class="role">"""+ position +"""</p>
        </div>
        <div class="items">
            <div class="summoner ss1"></div>
            <div class="summoner ss2"></div>
            <div class="item item1"></div>
            <div class="item item2"></div>
            <div class="item item3"></div>
            <div class="item item4"></div>
            <div class="item item5"></div>
            <div class="item item6"></div>
        </div>
        <div class="kda">
            <div class="stat">"""+ k +"""</div>
            <div class="stat">"""+ d +"""</div>
            <div class="stat">"""+ a +"""</div>
        </div>
        <div class="region">
        <p>KR</p>
        </div>
    </div>
    </div>
</body>
</html>
"""
        with open("./assets/thumbnail.html", "w") as f:
            f.write(HTML)
