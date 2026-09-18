# Component Diagram

```mermaid
flowchart TB
 CLI[main.py CLI orchestration]
 Input[Image and webcam input]
 Detection[src/face_detector.py FaceDetector]
 Processing[src/image_processor.py ImageProcessor]
 Emotion[src/emotion_detector.py EmotionDetector]
 Classifier[src/emotion_classifier.py EmotionClassifier and EmotionResult]
 Mood[src/mood_mapper.py MoodMapper]
 Recommendation[src/music_recommender.py MusicRecommender]
 Playback[src/music_player.py MusicPlayer]
 History[src/history_manager.py HistoryManager]
 Config[src/config.py configuration]
 Logger[src/logger.py logging]
 Utils[src/utils.py smoothing and output]
 OpenCV[OpenCV Haar cascade]
 DeepFace[DeepFace pretrained emotion analysis]
 Pygame[Pygame mixer]
 Mapping[(data/emotions.json)]
 Records[(data/history/analysis_history.json)]
 Captures[(data/captures)]
 Music[(music/ or project/music/ compatibility fallback)]

 CLI --> Input
 Input --> Detection --> Processing --> Emotion --> Classifier --> Mood
 Mood --> Recommendation --> Playback
 Classifier --> History
 Mood --> History
 Recommendation --> History
 Detection -. uses .-> OpenCV
 Emotion -. uses .-> DeepFace
 Playback -. uses .-> Pygame
 Mood -. loads .-> Mapping
 History --> Records
 CLI --> Captures
 Recommendation -. discovers .-> Music
 Config -. configures .-> CLI
 Config -. configures .-> Detection
 Config -. configures .-> Recommendation
 Config -. configures .-> Playback
 Config -. configures .-> History
 Logger -. receives errors .-> CLI
 Logger -. receives errors .-> Emotion
 Logger -. receives errors .-> Recommendation
 Logger -. receives errors .-> Playback
 Utils -. supports .-> CLI
```

Image mode loads one image and optionally plays its recommendation with `--play`. Webcam mode reads frames continuously, skips frames according to `FRAME_SKIP`, smooths recent emotion predictions, uses the largest face as the primary listener for mood-change actions, and processes `q`, `p`, `m`, and `s` controls in the focused OpenCV window. Webcam playback is automatic when a new smoothed mood is selected.
