

class AddEndingScreenOnYoutube:
    def __init__(self, video_id):
        self.__video_id = video_id

    def AddEndingFromLastVideo(self):
        f"https://studio.youtube.com/video/{self.__video_id}/edit"
        "$('#endscreen-editor-link').dispatchEvent(new MouseEvent('click'))"
        "$('.card').dispatchEvent(new MouseEvent('click'))"
        "$('#save-button').dispatchEvent(new MouseEvent('click'))"
        return 1