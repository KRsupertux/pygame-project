import pygame
from moviepy.editor import VideoFileClip

# Pygame 초기화
pygame.init()

# 화면 설정
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("컷씬 예제")

# 동영상 파일 경로
video_path = r"C:\Users\shy01\OneDrive\바탕 화면\폰\DCIM\Camera\20241010_162215.mp4"

# 동영상 재생 함수
def play_cutscene(video_path, screen):
    # MoviePy로 비디오 클립 로드
    clip = VideoFileClip(video_path)
    clip = clip.resize((screen.get_width(), screen.get_height()))  # 화면 크기에 맞게 조정

    # Pygame으로 비디오 프레임 출력
    clock = pygame.time.Clock()
    for frame in clip.iter_frames(fps=30, with_times=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Pygame 표준 방식으로 화면에 이미지 표시
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # 축 변경 필요
        screen.blit(frame_surface, (0, 0))
        pygame.display.update()
        clock.tick(30)  # FPS에 맞춰 속도 조절

    clip.close()  # 클립 리소스 정리

# 메인 루프
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # 검은색 화면
        pygame.display.update()

        # 스페이스바로 컷씬 재생
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            play_cutscene(video_path, screen)

    pygame.quit()

if __name__ == "__main__":
    main()