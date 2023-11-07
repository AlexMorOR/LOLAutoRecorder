import httplib2
import os
import random
import time

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from video_maker.entities.match_data import MatchData


class UploadYoutube:
    def __init__(self, match_data: MatchData, video_file_name: str) -> None:
        self.__thumb_file = r'C:\youtube\lol\thumb\thumb.png'
        self.__file = fr'C:\youtube\Joao\Videos\{video_file_name}'
        self.__match_data = match_data

        self.__category = "20"
        self.__keywords = [f"{match_data['mvp']['champion']}", f"{match_data['player_role']}", 
                           "challenger",
                           "leagueoflegends", "lol", "guide", "replay", "high kda",
                           f"{match_data['region']}"]
        httplib2.RETRIES = 1
        self.__MAX_RETRIES = 10
        self.__RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)
        self.__RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
        self.__CLIENT_SECRETS_FILE = "./credentials/client_secrets.json"
        self.__YOUTUBE_UPLOAD_SCOPE = [
            "https://www.googleapis.com/auth/youtube.upload",
            "https://www.googleapis.com/auth/youtube"]
        self.__YOUTUBE_API_SERVICE_NAME = "youtube"
        self.__YOUTUBE_API_VERSION = "v3"
        self.__VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")
        self.__MISSING_CLIENT_SECRETS_MESSAGE = f"""
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

          {os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          self.__CLIENT_SECRETS_FILE))}

        with information from the API Console
        https://console.developers.google.com/

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """

    def upload_video(self): #====================================== UPLOAD VIDEO
        try:
            self.__initialize_upload()
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")

    def __upload_thumbnail(self, youtube, video_id): #============= UPLOAD THUMBNAIL
        print('Fazendo upload da thumbnail')
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=self.__thumb_file
        ).execute()

    def __build_video_data(self): #================================ BUILD VIDEO DATA
        print("Building video data...")

        match_data = self.__match_data
        playlists = self.__playlists #Need update in each desc.
        playlist_ids = self.__playlist_ids

        

        self.__title_en = (
            f"{match_data['mvp']['champion']} vs {match_data['loser']} - {match_data['player_role']} - {match_data['mvp']['rank']} - League of Legends")
        self.__description_en = f"""
{match_data['mvp']['champion']} {match_data['player_role']} played by {match_data['mvp']['name']} at #{match_data['region']}{match_data['mvp']['rank']}

Watch how the professionals play, learn and become better!
Today we are watching how the {match_data['mvp']['champion']} {match_data['mvp']['rank']} plays in the League of Legends! Don't miss this amazing match.

Playlist {playlists[0]} - https://www.youtube.com/playlist?list={playlist_ids[0]}
Playlist {playlists[1]} - https://www.youtube.com/playlist?list={playlist_ids[1]}

Watch now to experience the intense action of a League of Legends pro league replay! This guide provides valuable insights for all aspiring challengers, with high KDA plays and impressive strategies. Immerse yourself in the world of League of Legends and improve your skills to climb the ranks. Don't miss out on this epic gameplay!

Data provided by https://leagueofgraphs.com
    """
        
        # Localized title and description in Russian
        self.__title_ru = (
            f"{match_data['mvp']['champion']} против {match_data['loser']} - {match_data['player_role']} - {match_data['mvp']['rank']} - League of Legends"
        )
        self.__description_ru = f"""
{match_data['mvp']['champion']} {match_data['player_role']} в исполнении {match_data['mvp']['name']} в регионе #{match_data['region']}{match_data['mvp']['rank']}

Смотрите, как играют профессионалы, учитесь и становитесь лучше!
Сегодня мы наблюдаем за игрой {match_data['mvp']['champion']} {match_data['mvp']['rank']} в League of Legends! Не пропустите это замечательное соревнование.

Плейлист {playlists[0]} - https://www.youtube.com/playlist?list={playlist_ids[0]}
Плейлист {playlists[1]} - https://www.youtube.com/playlist?list={playlist_ids[1]}

Посмотрите видео прямо сейчас, чтобы ощутить напряженные действия повтора профессиональной лиги League of Legends! Это руководство содержит ценную информацию для всех честолюбивых игроков, а также предлагает игры с высокими показателями KDA и впечатляющие стратегии. Погрузитесь в мир League of Legends и улучшите свои навыки, чтобы подняться по карьерной лестнице. Не пропустите этот эпический игровой процесс!

Данные предоставлены https://leagueofgraphs.com
        """

        self.__title_de = (
            f"{match_data['mvp']['champion']} vs {match_data['loser']} - {match_data['player_role']} - {match_data['mvp']['rank']} - League of Legends"
        )
        self.__description_de = f"""
{match_data['mvp']['champion']} {match_data['player_role']} gespielt von {match_data['mvp']['name']} in der Region #{match_data['region']}{match_data['mvp']['rank']}

Sehen Sie, wie die Profis spielen, lernen Sie dazu und werden Sie besser!
Heute beobachten wir, wie der {match_data['mvp']['champion']} {match_data['mvp']['rank']} in League of Legends spielt! Verpassen Sie nicht dieses beeindruckende Match.

Wiedergabeliste {playlists[0]} - https://www.youtube.com/playlist?list={playlist_ids[0]}
Wiedergabeliste {playlists[1]} - https://www.youtube.com/playlist?list={playlist_ids[1]}

Schauen Sie sich jetzt an, um die intensive Action einer League of Legends-Profiliga-Wiederholung zu erleben! Dieser Leitfaden bietet wertvolle Einblicke für alle aufstrebenden Herausforderer, mit Spielen mit hohem KDA und beeindruckenden Strategien. Tauchen Sie ein in die Welt von League of Legends und verbessern Sie Ihre Fähigkeiten, um in der Rangliste aufzusteigen. Lassen Sie sich dieses epische Gameplay nicht entgehen!

Daten bereitgestellt von https://leagueofgraphs.com
        """

        self.__title_pt = (
            f"{match_data['mvp']['champion']} vs {match_data['loser']} - {match_data['player_role']} - {match_data['mvp']['rank']} - League of Legends"
        )
        self.__description_pt = f"""
{match_data['mvp']['champion']} {match_data['player_role']} jogado por {match_data['mvp']['name']} no #{match_data['region']}{match_data['mvp']['rank']}

Veja como os profissionais jogam, aprenda e se torne melhor!
Hoje estamos assistindo como o {match_data['mvp']['champion']} {match_data['mvp']['rank']} joga no League of Legends! Não perca esta partida incrível.

Lista de reprodução {playlists[0]} - https://www.youtube.com/playlist?list={playlist_ids[0]}
Lista de reprodução {playlists[1]} - https://www.youtube.com/playlist?list={playlist_ids[1]}

Assista agora para experimentar a ação intensa de um replay da liga profissional de League of Legends! Este guia fornece informações valiosas para todos os aspirantes a desafiantes, com jogadas de alto KDA e estratégias impressionantes. Mergulhe no mundo de League of Legends e melhore suas habilidades para subir na classificação. Não perca esta jogabilidade épica!

Dados fornecidos por https://leagueofgraphs.com
        """

        self.__title_tr = (
            f"{match_data['mvp']['champion']} vs {match_data['loser']} - {match_data['player_role']} - {match_data['mvp']['rank']} - League of Legends"
        )
        self.__description_tr = f"""
{match_data['mvp']['champion']} {match_data['player_role']}, {match_data['mvp']['name']} tarafından #{match_data['region']}{match_data['mvp']['rank']} olarak oynandı

Profesyonellerin nasıl oynadığını izleyin, öğrenin ve daha iyi olun!
Bugün League of Legends'ta {match_data['mvp']['champion']} {match_data['mvp']['rank']} nasıl oynadığını izliyoruz! Bu müthiş maçı kaçırmayın.

Çalma listesi {playlists[0]} - https://www.youtube.com/playlist?list={playlist_ids[0]}
Çalma listesi {playlists[1]} - https://www.youtube.com/playlist?list={playlist_ids[1]}

League of Legends profesyonel lig tekrarının yoğun aksiyonunu deneyimlemek için hemen izleyin! Bu kılavuz, yüksek KDA oyunları ve etkileyici stratejilerle tüm istekli meydan okuyucular için değerli bilgiler sağlar. Kendinizi League of Legends dünyasına bırakın ve sıralamalarda yükselmek için becerilerinizi geliştirin. Bu destansı oynanışı kaçırmayın!

Veriler https://leagueofgraphs.com tarafından sağlanmıştır.
        """

        return {
            "file": self.__file,
            "title": self.__title_en,
            "description": self.__description_en,
            "category": self.__category,
            "keywords": self.__keywords,
            "privacyStatus": self.__VALID_PRIVACY_STATUSES[0],
            "localizations": {
                "en": {
                    "title": self.__title_en,
                    "description": self.__description_en
                },
                "ru": {
                    "title": self.__title_ru,
                    "description": self.__description_ru
                },
                "de": {
                    "title": self.__title_de,
                    "description": self.__description_de
                },
                "pt": {
                    "title": self.__title_pt,
                    "description": self.__description_pt
                },
                "tr": {
                    "title": self.__title_tr,
                    "description": self.__description_tr
                },
                
            }
        }

    def __get_authenticated_service(self): #============================== GET YOUTUBE SERVICE
        flow = flow_from_clientsecrets(self.__CLIENT_SECRETS_FILE,
                                       scope=self.__YOUTUBE_UPLOAD_SCOPE,
                                       message=self.__MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("./credentials/storage-oauth2.json")
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage)

        return build(self.__YOUTUBE_API_SERVICE_NAME, self.__YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))

    def __initialize_upload(self): #============================== INITIALIZE UPLOAD
        print('Starting upload video...')
        youtube = self.__get_authenticated_service()
        self.__playlists = [self.__match_data['player_role'], self.__match_data['mvp']['rank']]
        self.__playlist_ids = []
        for playlist in self.__playlists:
            print(f'Getting or creating playlist "{playlist}"')
            # Check if the Champion playlist exists and get its ID. If not, create it.
            self.__playlist_ids.append(self.__get_or_create_playlist(youtube, playlist))

        options = self.__build_video_data()
        tags = options['keywords'] if options['keywords'] else None

        body = dict(
            snippet=dict(
                title=options['title'],
                description=options['description'],
                tags=tags,
                categoryId=options['category'],
                defaultLanguage='en'
            ),
            status=dict(
                privacyStatus=options['privacyStatus']
            ),
            localizations=options['localizations']
        )

        # Call the API's videos.insert method to create and upload the video.
        insert_request = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(
                options['file'], chunksize=-1, resumable=True)
        )

        video_id = self.__resumable_upload(insert_request)
        self.__upload_thumbnail(youtube, video_id)

        for playlist_id in self.__playlist_ids:
            # If we have a playlist ID, add the video to the playlist.
            if playlist_id:
                self.__add_video_to_playlist(youtube, video_id, playlist_id)
            else:
                print("Failed to find or create playlist.")

    def __resumable_upload(self, insert_request):
        response = None
        error = None
        retry = 0
        while response is None:
            try:
                print("Uploading file...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(
                            f"Video id {response['id']} was successfully uploaded.")
                        return response['id']
                    else:
                        exit(
                            f"The upload failed with an unexpected response: {response}")
            except HttpError as e:
                if e.resp.status in self.__RETRIABLE_STATUS_CODES:
                    error = f"A retriable HTTP error {e.resp.status} occurred:\n{e.content}"
                else:
                    raise
            except self.__RETRIABLE_EXCEPTIONS as e:
                error = f"A retriable error occurred: {e}"

            if error is not None:
                print(error)
                retry += 1
                if retry > self.__MAX_RETRIES:
                    exit("No longer attempting to retry.")

                max_sleep = 2 ** retry
                sleep_seconds = random.random() * max_sleep
                print(f"Sleeping {sleep_seconds} seconds and then retrying...")
                time.sleep(sleep_seconds)

    def __get_or_create_playlist(self, youtube, playlist_name):
        # Step 1: Search for the playlist by name to see if it already exists
        playlists = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=25
        ).execute()

        for playlist in playlists.get('items', []):
            if playlist['snippet']['title'] == playlist_name:
                return playlist['id']

        # Step 2: If the playlist does not exist, create it
        playlist_body = {
            'snippet': {
                'title': playlist_name,
                'description': playlist_name
            },
            'status': {
                'privacyStatus': 'public'  # or 'private' or 'unlisted'
            }
        }

        try:
            created_playlist = youtube.playlists().insert(
                part='snippet,status',
                body=playlist_body
            ).execute()

            return created_playlist['id']
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return None

    def __add_video_to_playlist(self, youtube, video_id, playlist_id):
        # Step 3: Add the uploaded video to the playlist
        add_video_request = youtube.playlistItems().insert(
            part="snippet",
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        ).execute()
