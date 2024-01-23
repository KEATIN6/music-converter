# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 10:13:26 2024

@author: KEATIN6
"""

# %%

from pydub import AudioSegment
import os

# %%

MUSIC_PATH = r"<music directory>"
OUTPUT_PATH = r"<output destination>"

# %%

class Song:
    def __init__(self, artist_folder, albumn_folder, song_file):
        self.artist_folder = artist_folder
        self.albumn_folder = albumn_folder
        self.song_file = song_file
        
    def get_path(self, directory):
        return os.path.join(
            directory, self.artist_folder, self.albumn_folder, self.song_file
        )
        
# %%

class MusicNavigator:
    def __init__(self, music_directory, output_directory):
        self.music_directory = music_directory
        self.output_directory = output_directory
    
    def _get_items(self, path):
        try:
            items = os.listdir(path)
            return [item for item in items if not item.startswith(".")]
        except NotADirectoryError:
            return None
        
    def _get_files_by_type(self, files, file_type):
        return [file for file in files if file.endswith(file_type)]
    
    def get_artists(self):
        return self._get_items(self.music_directory)
    
    def get_albums(self, artist_folder):
        full_artist_path = os.path.join(self.music_directory, artist_folder)
        items = self._get_items(full_artist_path)
        return [item for item in items if os.path.isdir(os.path.join(full_artist_path, item))]
    
    def get_songs(self, artist_folder, albumn_folder, file_type=None):
        full_albumn_path = os.path.join(
            self.music_directory, artist_folder, albumn_folder
        )
        if not os.path.isdir(full_albumn_path):
            return None
        songs = self._get_items(full_albumn_path)
        if not file_type:
            return songs
        return self._get_files_by_type(songs, file_type)
            
    def check_output_path_exists(self, artist_folder: str, 
                                 albumn_folder: str) -> bool:
        path_to_check_01 = os.path.join(self.output_directory, artist_folder)
        path_to_check_02 = os.path.join(path_to_check_01, albumn_folder)
        for path in [path_to_check_01, path_to_check_02]:
            if not os.path.exists(path):
                os.makedirs(path)
        return True
    
    def search_directory_by_type(self, file_type=".m4a"):
        song_list = []
        artists = self.get_artists()
        for index, artist in enumerate(artists):
            albums = self.get_albums(artists[index])
            for index, album in enumerate(albums):
                songs = self.get_songs(artist, album, file_type)
                for song in songs:
                    print(song)
                    song_list.append(Song(artist, album, song))
        print(f"Results Found: {len(song_list)}")
        return song_list

# %%

class MusicConverter(MusicNavigator):
    def __init__(self, music_directory, output_directory, file_type=None):
        super().__init__(music_directory, output_directory)
        self.music_directory = music_directory
        self.output_directory = output_directory
        if file_type:
            self.run(file_type)

    def convert_m4a_to_mp3(self, input_file, output_file) -> bool:
        if input_file.endswith('.m4a'):
            try:
                audio = AudioSegment.from_file(input_file, format="m4a")
                audio.export(output_file, format="mp3")
                return True
            except:
                pass
        return False

    def convert_all_songs(self, songs):
        for song in songs:
            self.check_output_path_exists(
                song.artist_folder, song.albumn_folder
            )
            print(song.song_file)
            input_file = song.get_path(MUSIC_PATH)
            output_file = song.get_path(OUTPUT_PATH).replace('.m4a', '.mp3')
            if self.convert_m4a_to_mp3(input_file, output_file):
                print("Converted to MP3")
        
    def run(self, file_type) -> bool:
        songs = self.search_directory_by_type(file_type)
        self.convert_all_songs(songs)
        return True

# %%

if __name__ == '__main__':
    converter = MusicConverter(MUSIC_PATH, OUTPUT_PATH, '.m4a')

# %%
