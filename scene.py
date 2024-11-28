import pygame
from moviepy import VideoFileClip
import time

# Pygame 초기화
pygame.init()

class Cutscene:
    def __init__(self, video_path, audio_path, subtitles, screen_width, screen_height):
        self.video_path = video_path
        self.audio_path = audio_path
        self.subtitles = subtitles
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(pygame.font.match_font("malgun gothic"), 48)  # 맑은고딕, 크기 48
        self.text_color = (255, 0, 0)  # 빨간색
        self.subtitle_interval = 1.0  # 단어가 나타나는 시간 간격 (초)
        self.subtitle_display_time = 3.0  # 한 문장이 다 출력된 후 대기 시간 (초)
        self.is_played = False  # 영상이 한번 재생되었는지 체크하는 변수

    def play(self, screen):
        if self.is_played:
            # 이미 영상이 한 번 실행된 경우에는 화면을 검은색으로 설정
            screen.fill((0, 0, 0))  # 검은 화면으로 설정
            pygame.display.update()
            return  # 더 이상 동작하지 않음

        # MoviePy로 비디오 클립 로드
        clip = VideoFileClip(self.video_path)
        clip = clip.resized((self.screen_width, self.screen_height))  # 화면 크기 조정

        # Pygame Mixer로 오디오 재생
        pygame.mixer.init()  # Mixer 초기화
