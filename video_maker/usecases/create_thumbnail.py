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
        champion = self.__get_api_name(self.lol_data['mvp']['champion'])
        enemy = self.__get_api_name(self.lol_data['loser'])
        items = [self.__make_48_sprite(item) for item in self.lol_data['mvp']['items']]
        rune = self.__make_48_sprite(self.lol_data['mvp']['rune'])
        sumSpell1 = self.__make_48_sprite(self.lol_data['mvp']['spells'][0])
        sumSpell2 = self.__make_48_sprite(self.lol_data['mvp']['spells'][1])
        self.__create_html(
            k=self.lol_data['mvp']['k'], d=self.lol_data['mvp']['d'], a=self.lol_data['mvp']['a'],
            heroAPIName=champion, enemyAPIName=enemy,
            heroName=self.lol_data['mvp']['champion'], enemyName=self.lol_data['loser'], heroSkin="0",
            sumSpell1=sumSpell1, sumSpell2=sumSpell2,
            items=items, rune=rune,
            position=self.lol_data['mvp']['role'],
            region=self.lol_data['region'], patch=self.lol_data['patch']
        )
        html_path = os.path.abspath('assets/thumbnail.html')
        self.scrapper.driver.get('file://' + html_path)
        sleep(2)
        self.scrapper.driver.set_window_size(1280, 805)
        self.scrapper.driver.save_screenshot(self.__thumb_path)
        print('Thumbnail criada!')
        self.scrapper.driver.quit()

    def __make_48_sprite(self,
                         orig:str) -> str:
        parts = orig.split("-")
        parts[2] = "48"
        return f'{parts[0]}-{parts[1]}-{parts[2]}'
    
    def __get_api_name(self, name:str) -> str:
        premadeWords = {
            "K'Sante": "KSante",
            "Kai'Sa": "Kaisa",
            "LeBlanc": "Leblanc",
            "Wukong": "MonkeyKing"
        }
        api_name = ""
        if name in premadeWords:
            api_name = premadeWords[name]
        else:
            champion = name.replace(
                "'", "").lower().capitalize()
            champion = champion.replace(
                " ", "")
            api_name = champion
        return api_name

    def __create_html(self, 
                      k:str, d:str, a:str ,
                      heroAPIName:str, enemyAPIName:str,
                      heroName: str, enemyName: str, heroSkin: str,
                      sumSpell1:str, sumSpell2:str,
                      items:list[str], rune:str,
                      position:str,
                      region: str, patch: str):
        ITEMS_HTML = ''
        for item in items:
            ITEMS_HTML += f'<div class="item {item}"></div>'
        HTML = """

<!DOCTYPE html>
<html>
    <head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;800&display=swap" rel="stylesheet">
    <link data-react-helmet="true" rel="stylesheet" href="https://lolstatic-a.akamaihd.net/webfonts/live/css/fonts/beaufortforlol.css">
    <link rel="stylesheet" type="text/css" href="https://lolg-cdn.porofessor.gg/style.sprite.css?v=a917983e5f0d4c8bd0ef5aad89b31565">
    <style>
        * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: "Beaufort for LOL";
        }
        .back{
            background-image: url('https://ddragon.leagueoflegends.com/cdn/img/champion/splash/"""+ heroAPIName +"""_"""+ heroSkin +""".jpg');
        }
        .p1{
            background-image: url('http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/"""+ heroAPIName +""".png');
        }
        .p2{
            background-image: url('http://ddragon.leagueoflegends.com/cdn/13.21.1/img/champion/"""+ enemyAPIName +""".png');
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
        }
        .items .summoner{
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
        .rune{
            transform: scale(2);
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
        <div class="rune """+ rune +""""></div>
        <div class="match">
        <p class="mvp">"""+ heroName +"""</p>
        <p class="role">"""+ position +"""</p>
        </div>
        <div class="items">
            <div class="summoner """+ sumSpell1 +""""></div>
            <div class="summoner """+ sumSpell2 +""""></div>
            """+ ITEMS_HTML +"""
        </div>
        <div class="kda">
            <div class="stat">"""+ k +"""</div>
            <div class="stat">"""+ d +"""</div>
            <div class="stat">"""+ a +"""</div>
        </div>
        <div class="region">
        <p>"""+ region +"""</p>
        </div>
    </div>
    </div>
</body>
</html>
"""
        with open("./assets/thumbnail.html", "w") as f:
            f.write(HTML)
