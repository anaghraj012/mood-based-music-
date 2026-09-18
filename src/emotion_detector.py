"""DeepFace adapter. The rest of the application does not depend on DeepFace APIs."""
from .emotion_classifier import EmotionClassifier, EmotionResult
from .logger import get_logger

logger = get_logger(__name__)


class EmotionDetector:
    def __init__(self, classifier: EmotionClassifier | None = None):
        self.classifier = classifier or EmotionClassifier()
        self._deepface = None

    def _load_backend(self):
        if self._deepface is None:
            from deepface import DeepFace
            self._deepface = DeepFace
        return self._deepface

    def analyze(self, image) -> EmotionResult:
        try:
            result = self._load_backend().analyze(image, actions=["emotion"], enforce_detection=False)
            if isinstance(result, list):
                result = result[0]
            raw = {"emotion": result.get("dominant_emotion"), "scores": result.get("emotion", {})}
            return self.classifier.classify(raw)
        except Exception as exc:
            logger.exception("DeepFace analysis failed: %s", exc)
            raise RuntimeError("Emotion analysis failed. Check the image and model dependencies.") from exc
