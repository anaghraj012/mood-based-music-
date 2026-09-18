# Architecture

```mermaid
flowchart TD
 User --> CLI
 CLI --> Input[Image or Webcam Input]
 Input --> FaceDetector[FaceDetector]
 FaceDetector --> Processor[ImageProcessor]
 Processor --> Detector[EmotionDetector]
 Detector --> Classifier[EmotionClassifier]
 Classifier --> Result[Emotion + Confidence]
 Result --> Mapper[MoodMapper]
 Mapper --> Recommender[MusicRecommender]
 Recommender --> Player[MusicPlayer]
 CLI --> History[HistoryManager]
 Result -. analysis result .-> History
 Mapper -. mapped mood .-> History
 Recommender -. selected track .-> History
 Config[config.py] -. configuration .-> CLI
 Config -. configuration .-> FaceDetector
 Config -. configuration .-> Recommender
 Config -. configuration .-> Player
 Config -. paths .-> History
 Logger[logger.py] -. logging .-> CLI
 Logger -. logging .-> Detector
 Logger -. logging .-> Recommender
 Logger -. logging .-> Player
 Utils[utils.py] -. smoothing/output .-> CLI
 OpenCV[OpenCV Haar cascade] -.-> FaceDetector
 DeepFace[DeepFace pretrained analysis] -.-> Detector
 Pygame[Pygame mixer] -.-> Player
 Music[(music library)] -.-> Recommender
 Data[(data/emotions.json and data/history)] -.-> Mapper
 Data -.-> History
```

The CLI coordinates image and webcam workflows while the modules own separate responsibilities. Webcam mode applies frame skipping and temporal smoothing, uses the largest detected face as the primary listener for mood-change actions, and handles `q`, `p`, `m`, and `s` controls. Webcam playback is automatic on a smoothed mood change; image playback is optional with `--play`.
