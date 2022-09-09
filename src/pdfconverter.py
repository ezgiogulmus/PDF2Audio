from PyPDF2 import PdfReader
from gtts import gTTS
import glob
import os

class ListenPDFs:
    def __init__(self, file_path, first_page=1, last_page=-1, language="en"):
        """
        file_path: path to PDF file
        page_number: starting page, default is 1 to start from the beginning
        """
        self.file_path = file_path
        self.reader = PdfReader(self.file_path)

        if last_page == -1:
            self.last_page = len(self.reader.pages)
        else:
            self.last_page = last_page
        self.current_page = first_page-1
        self.lang = language
    
    def get_text(self):
        text_path = f"{self.file_path.rsplit('.', 1)[0]}.txt"
        while self.current_page < self.last_page:
            with open(text_path, "a+") as file:
                    file.write(self.reader.pages[self.current_page].extract_text())
            self.current_page += 1
        return text_path

    def save_mp3(self, text_path, lang="en"):
        mp3_path = f"{self.file_path.rsplit('.', 1)[0]}.mp3"
        with open(text_path, "r") as file:
            text = file.read()
        tts = gTTS(text=text, lang=lang)
        tts.save(mp3_path)
        return mp3_path

def empty_folder(file_path):
    files = glob.glob(file_path)
    for f in os.listdir(file_path):
        os.remove(f"{file_path}{f}")
