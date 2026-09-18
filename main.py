"""Command-line entry point for mood-based music recommendation."""
import argparse
import sys
from collections import deque
from pathlib import Path

import cv2

from src import __version__
from src.config import CAPTURE_DIR, DEFAULT_VOLUME, FRAME_SKIP, MIN_CONFIDENCE, SMOOTHING_WINDOW, WEBCAM_INDEX
from src.emotion_detector import EmotionDetector
from src.face_detector import FaceDetector
from src.history_manager import HistoryManager
from src.image_processor import ImageProcessor
from src.logger import get_logger
from src.mood_mapper import MoodMapper
from src.music_player import MusicPlayer
from src.music_recommender import MusicRecommender
from src.utils import print_analysis, stable_emotion

logger = get_logger(__name__)


def analyze_faces(image, source: str, detector, face_detector, processor, mapper, recommender, history, player, play=False):
    faces = face_detector.detect_faces(image)
    print(f"Faces Found  : {len(faces)}")
    if not faces:
        print("No face detected. Try a clearer, front-facing image.")
        return []
    analyses = []
    for index, box in enumerate(faces, 1):
        face = processor.crop_face(image, box)
        result = detector.analyze(processor.preprocess_face(face))
        if result.confidence < MIN_CONFIDENCE:
            print(f"\nFace {index}: Emotion uncertain ({result.confidence:.1%} confidence)")
            continue
        mood = mapper.map_emotion(result.emotion)
        recommendation = recommender.recommend(mood)
        print_analysis(index, result, mood, recommendation)
        track = str(recommendation) if recommendation else None
        history.save_analysis(source, result.emotion, result.confidence, mood, track)
        if play and recommendation:
            print("Status       : Playing" if player.play(recommendation) else "Status       : Playback unavailable")
        analyses.append((box, result, mood))
    return analyses


def run_image(path: str, play: bool):
    processor = ImageProcessor()
    detector, mapper = EmotionDetector(), MoodMapper()
    recommender, player, history = MusicRecommender(), MusicPlayer(), HistoryManager()
    image = processor.load_image(path)
    face_detector = FaceDetector()
    print("=========================================")
    print("MOOD-BASED MUSIC RECOMMENDER")
    print("=========================================")
    print("Input Source : Image")
    analyze_faces(image, "image", detector, face_detector, processor, mapper, recommender, history, player, play)
    player.stop()


def run_webcam(play: bool):
    detector, face_detector, processor = EmotionDetector(), FaceDetector(), ImageProcessor()
    mapper, recommender, player, history = MoodMapper(), MusicRecommender(), MusicPlayer(), HistoryManager()
    capture = cv2.VideoCapture(WEBCAM_INDEX)
    if not capture.isOpened():
        print("ERROR: Could not open webcam. Check that the camera is connected and available.")
        return 1
    print("Webcam mode: q quit | p pause/resume analysis | m mute/unmute | s save capture")
    frame_number, paused, muted = 0, False, False
    recent = deque(maxlen=SMOOTHING_WINDOW)
    latest = []
    current_mood = None
    current_track = None
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                print("ERROR: Could not read a frame from the webcam.")
                break
            frame_number += 1
            if not paused and frame_number % max(1, FRAME_SKIP) == 0:
                faces = face_detector.detect_faces(frame)
                latest = []
                for box in faces:
                    result = detector.analyze(processor.preprocess_face(processor.crop_face(frame, box)))
                    recent.append(result.emotion)
                    display_emotion = stable_emotion(recent)
                    if result.confidence >= MIN_CONFIDENCE:
                        mood = mapper.map_emotion(display_emotion)
                        latest.append((box, display_emotion, result.confidence, mood))
                if latest:
                    _, emotion, confidence, mood = max(
                        latest,
                        key=lambda item: item[0][2] * item[0][3],
                    )
                    if mood != current_mood:
                        current_mood = mood
                        current_track = recommender.recommend(mood)
                        track_name = current_track.name if current_track else "No local track found"
                        print(
                            f"Webcam analysis | Emotion: {emotion.title()} | "
                            f"Confidence: {confidence:.1%} | Mood: {mood.title()} | "
                            f"Recommendation: {track_name}"
                        )
                        history.save_analysis(
                            "webcam",
                            emotion,
                            confidence,
                            mood,
                            str(current_track) if current_track else None,
                        )
                        if current_track and not muted:
                            status = "Playing" if player.play(current_track) else "Playback unavailable"
                            print(f"Playback: {status}")
                labels = [
                    f"{emotion.title()} {confidence:.0%} {mood.title()}"
                    for _, emotion, confidence, mood in latest
                ]
                face_detector.draw_faces(frame, [item[0] for item in latest], labels)
            else:
                face_detector.draw_faces(
                    frame,
                    [item[0] for item in latest],
                    [f"{item[1].title()} {item[2]:.0%} {item[3].title()}" for item in latest],
                )
            cv2.imshow("Mood Detection | q quit", frame)
            key = cv2.waitKeyEx(1) & 0xFF
            key = chr(key).lower() if key else ""
            if key == "q":
                break
            if key == "p":
                paused = not paused
                print(f"Analysis: {'paused' if paused else 'resumed'}")
            elif key == "m":
                muted = not muted
                player.set_volume(0 if muted else DEFAULT_VOLUME)
                print(f"Music: {'muted' if muted else 'unmuted'}")
            elif key == "s":
                CAPTURE_DIR.mkdir(parents=True, exist_ok=True)
                output = CAPTURE_DIR / f"capture_{cv2.getTickCount()}.jpg"
                cv2.imwrite(str(output), frame)
                print(f"Saved capture: {output}")
                for _, emotion, confidence, mood in latest:
                    recommendation = recommender.recommend(mood)
                    history.save_analysis("webcam", emotion, confidence, mood, str(recommendation) if recommendation else None)
                    if play and recommendation and not muted:
                        player.play(recommendation)
    finally:
        capture.release()
        cv2.destroyAllWindows()
        player.stop()
    return 0


def show_summary(history):
    summary = history.summary()
    print(f"Analyses: {summary['analyses']}")
    print(f"Most frequent emotion: {summary['most_frequent_emotion'] or 'None'}")
    print(f"Average confidence: {summary['average_confidence']:.1%}")
    print(f"Most frequent mood: {summary['most_frequent_mood'] or 'None'}")


def build_parser():
    parser = argparse.ArgumentParser(description="Analyze facial emotion and recommend local music.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--image", help="Analyze a local image")
    mode.add_argument("--webcam", action="store_true", help="Analyze a live webcam feed")
    mode.add_argument("--history", action="store_true", help="Show recent analysis history")
    mode.add_argument("--summary", action="store_true", help="Show analysis session summary")
    mode.add_argument("--version", action="version", version=f"Mood-Based Music Recommender v{__version__}")
    parser.add_argument("--play", action="store_true", help="Play the recommended local track")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        if args.image:
            run_image(args.image, args.play)
        elif args.webcam:
            return run_webcam(args.play)
        else:
            history = HistoryManager()
            if args.history:
                for item in history.get_recent():
                    print(item)
            else:
                show_summary(history)
        return 0
    except (FileNotFoundError, ValueError, RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}")
        logger.error("Application error: %s", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
