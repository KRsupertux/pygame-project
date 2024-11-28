from scene import Cutscene, ScenePlayer

if __name__ == "__main__":
    # 동영상, 오디오 및 자막 설정
    video_path = "data/testvideo.mp4"
    audio_path = "data/testsound.mp3"
    subtitles = [
        "이것은 첫 번째 자막입니다.",
        "두 번째 자막이 나옵니다.",
        "세 번째 자막입니다."
    ]

    # 컷씬 생성
    cutscene = Cutscene(video_path, audio_path, subtitles, 1400, 800)

    # 씬 플레이어 생성 및 실행
    scene_player = ScenePlayer(1400, 800)
    scene_player.run(cutscene)