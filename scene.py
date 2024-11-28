import pygame
from moviepy import VideoFileClip
import threading
import time

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("컷씬 예제")

# 동영상 파일 경로
video_path = r"C:\Users\shy01\Downloads\WW2_ Battle Of Stalingrad (Intense Footage).mp4"
audio_path = r"C:\Users\shy01\Downloads\WW2_ Battle Of Stalingrad (Intense Footage).mp3"


# 동영상 및 오디오 재생 함수
def play_cutscene_with_audio(video_path, audio_path, screen):
    # MoviePy로 비디오 클립 로드
    clip = VideoFileClip(video_path)
    clip = clip.resized((screen.get_width(), screen.get_height()))  # 화면 크기 조정

    # Pygame Mixer로 오디오 재생
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # Pygame 화면에 프레임 렌더링
    clock = pygame.time.Clock()
    start_time = time.time()

    for frame in clip.iter_frames(fps=30, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                return

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # 축 변경
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        elapsed_time = time.time() - start_time
        if elapsed_time < clip.duration:
            clock.tick(30)
        else:
            break

    pygame.mixer.music.stop()
    clip.close()
