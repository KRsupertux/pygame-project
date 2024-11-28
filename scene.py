import pygame
from moviepy import VideoFileClip
import time

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 1400, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("컷씬")

# 자막 출력 시간 설정
subtitle_interval = 1.0  # 단어가 나타나는 시간 간격 (초)
subtitle_display_time = 3.0  # 한 문장이 다 출력된 후 대기 시간 (초)

# 글꼴 설정
font_path = pygame.font.match_font("malgun gothic")
font = pygame.font.Font(font_path, 48)  # 맑은고딕, 크기 48
text_color = (255, 0, 0)  # 빨간색

# 동영상 및 오디오 및 자막 재생 함수
def play_cutscene(video_path, audio_path, screen, subtitles):
    # MoviePy로 비디오 클립 로드
    clip = VideoFileClip(video_path)
    clip = clip.resized((screen.get_width(), screen.get_height()))  # 화면 크기 조정

    # Pygame Mixer로 오디오 재생
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play()

    # Pygame 화면에 프레임 렌더링
    clock = pygame.time.Clock()
    start_time = time.time()
    subtitle_index = 0  # 현재 표시할 자막 인덱스
    word_index = 0  # 현재 표시할 단어 인덱스
    last_word_time = start_time  # 마지막 단어 출력 시간
    last_sentence_end_time = 0  # 문장이 완료된 시간
    waiting_for_next_sentence = False # 문장 표시 여부

    for frame in clip.iter_frames(fps=30, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Q 키가 눌리면 종료
                    pygame.mixer.music.stop()
                    screen.fill((0, 0, 0))  # 검은 화면으로 설정
                    pygame.display.update()
                    return

        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # 축 변경
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()

        #자막 생성
        if subtitle_index < len(subtitles):
            current_subtitle = subtitles[subtitle_index]
            words = current_subtitle.split()  # 현재 자막을 단어로 나누기

            if waiting_for_next_sentence:
                # 5초 대기 시간
                if time.time() - last_sentence_end_time >= subtitle_display_time:
                    subtitle_index += 1  # 다음 자막으로 이동
                    word_index = 0  # 단어 인덱스 초기화
                    waiting_for_next_sentence = False
            else:
                # 단어 출력
                if time.time() - last_word_time >= subtitle_interval:
                    word_index += 1
                    last_word_time = time.time()

                # 문장이 완료되었는지 확인
                if word_index > len(words):
                    waiting_for_next_sentence = True
                    last_sentence_end_time = time.time()

            # 현재까지의 자막 텍스트 생성
            current_text = " ".join(words[:word_index])
            text_surface = font.render(current_text, True, text_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height - 50))
            screen.blit(text_surface, text_rect)

        # 화면 업데이트
        pygame.display.update()
        clock.tick(30)  # FPS 유지

    pygame.mixer.music.stop()
    clip.close()
# 메인 루프
def scene_play(video_path, audio_path, subtitles):
    running = True
    # 동영상, 오디오 파일 경로
    video_path = video_path
    audio_path = audio_path
    subtitles = subtitles

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # 검은색 화면
        pygame.display.update()

        # 스페이스바로 컷씬 재생
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            play_cutscene(video_path, audio_path, screen, subtitles)
    pygame.quit()