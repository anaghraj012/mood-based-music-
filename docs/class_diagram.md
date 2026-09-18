# Class Diagram

```mermaid
classDiagram
 class FaceDetector {
  +detect_faces(frame)
  +draw_faces(frame, faces, labels)
 }
 class ImageProcessor {
  +load_image(path)
  +crop_face(image, box)
  +preprocess_face(face)
 }
 class EmotionDetector {
  +analyze(image) EmotionResult
 }
 class EmotionClassifier {
  +classify(raw_result) EmotionResult
 }
 class EmotionResult {
  +emotion: str
  +confidence: float
  +scores: dict
 }
 class MoodMapper {
  +map_emotion(emotion) str
 }
 class MusicRecommender {
  +discover(mood) list[Path]
  +recommend(mood) Path
 }
 class MusicPlayer {
  +play(path) bool
  +pause()
  +resume()
  +stop()
  +set_volume(volume)
  +is_playing() bool
 }
 class HistoryManager {
  +save_analysis(...)
  +load_history() list
  +get_recent(count) list
  +clear_history()
  +summary(entries) dict
 }
 EmotionDetector --> EmotionClassifier : uses
 EmotionClassifier ..> EmotionResult : creates
 MoodMapper ..> data/emotions.json : loads mapping
```

`config.py`, `logger.py`, and `utils.py` are supporting modules rather than classes. The classes use configuration values for paths, extensions, frame skipping, confidence, volume, and smoothing; `logger.py` supplies `get_logger()`, and `utils.py` supplies `stable_emotion()` and `print_analysis()`. OpenCV, DeepFace, and Pygame are external libraries used behind the application classes.
