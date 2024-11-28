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

    def play(self, screen):
        # MoviePy로 비디오 클립 로드
        clip = VideoFileClip(self.video_path)
        clip = clip.resized((self.screen_width, self.screen_height))  # 화면 크기 조정

        # Pygame Mixer로 오디오 재생
        pygame.mixer.init()  # Mixer 초기화
        pygame.mixer.music.load(self.audio_path)
        pygame.mixer.music.play()

        # 자막 출력 관련 변수들
        subtitle_index = 0
        word_index = 0
        last_word_time = time.time()
        last_sentence_end_time = 0
        waiting_for_next_sentence = False

        # Pygame 화면에 프레임 렌더링
        clock = pygame.time.Clock()
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

            # 비디오 프레임을 Pygame 화면에 렌더링
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # 축 변경
            screen.blit(frame_surface, (0, 0))

            # 자막 생성
            if subtitle_index < len(self.subtitles):
                current_subtitle = self.subtitles[subtitle_index]
                words = current_subtitle.split()  # 현재 자막을 단어로 나누기

                if waiting_for_next_sentence:
                    # 5초 대기 시간
                    if time.time() - last_sentence_end_time >= self.subtitle_display_time:
                        subtitle_index += 1  # 다음 자막으로 이동
                        word_index = 0  # 단어 인덱스 초기화
                        waiting_for_next_sentence = False
                else:
                    # 단어 출력
                    if time.time() - last_word_time >= self.subtitle_interval:
                        word_index += 1
                        last_word_time = time.time()

                    # 문장이 완료되었는지 확인
                    if word_index > len(words):
                        waiting_for_next_sentence = True
                        last_sentence_end_time = time.time()

                # 현재까지의 자막 텍스트 생성
                current_text = " ".join(words[:word_index])
                text_surface = self.font.render(current_text, True, self.text_color)
                text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.screen_height - 50))  # 화면 하단에 자막 위치
                screen.blit(text_surface, text_rect)

            # 화면 업데이트
            pygame.display.update()
            clock.tick(30)  # FPS 유지

        pygame.mixer.music.stop()
        clip.close()


class ScenePlayer:
    def __init__(self, screen_width=1400, screen_height=800):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("컷씬")

    def run(self, cutscene):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # 검은색 화면
            pygame.display.update()

            # 스페이스바로 컷씬 재생
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                cutscene.play(self.screen)

        pygame.quit()
