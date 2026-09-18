# Project Statement

## Project Title
Mood-Based Music Recommendation Using Facial Emotion Recognition

## Student Information
- Student Name: Anuj Gupta
- Registration Number: 24BAI10152
- Course: Computer Vision
- Institution: VIT Bhopal University
- Academic Year: 2026

## Problem Statement
Selecting music manually according to a current mood is inconvenient. This project explores a local, computer-vision-assisted workflow that estimates facial emotion and uses it to recommend music.

## Objectives
Detect faces, estimate emotion and confidence, map emotion to a broader mood, recommend and optionally play local audio, and preserve analysis history.

## Functional Requirements

1. Detect one or more faces from an input image or webcam frame.
2. Crop and preprocess each detected face for emotion analysis.
3. Classify facial emotion using the supported DeepFace emotion categories.
4. Display the detected emotion and the confidence returned by the model.
5. Map the classified emotion to a broader application mood using configurable data.
6. Recommend a supported local audio track for the mapped mood.
7. Play the recommended local track automatically in webcam mode when the smoothed mood changes, and optionally in image mode with `--play`.
8. Store successful analyses, including source, emotion, confidence, mood, and recommendation, in JSON history.
9. Display recent history and calculate a session summary from recorded analyses.
10. Provide command-line execution for image analysis, webcam analysis, history, summary, and version information.

## Non-Functional Requirements

1. **Usability:** Provide clear CLI commands, webcam controls, readable output, and understandable error messages.
2. **Reliability:** Handle missing images, invalid image data, unavailable cameras, missing faces, missing music, and model-analysis failures without an uncontrolled traceback.
3. **Maintainability:** Keep configuration, detection, preprocessing, emotion analysis, mood mapping, recommendation, playback, and history in separate modules.
4. **Portability:** Resolve project paths relative to the repository so the project can be cloned to another directory.
5. **Performance:** Use configurable frame skipping and a short smoothing window so DeepFace inference is not performed on every webcam frame.
6. **Reproducibility:** Declare the Python dependencies and their tested versions in `requirements.txt` and keep the emotion-to-mood mapping in `data/emotions.json`.
7. **Modularity:** Hide external DeepFace and Pygame interfaces behind application-level classes so the CLI coordinates rather than implements every operation.
8. **Graceful error handling:** Report common configuration, input, camera, model, and audio problems through friendly messages and continue or exit cleanly where appropriate.

## Technology and Methodology

The system is implemented in Python. OpenCV Haar-cascade face detection locates faces in either a local image or a live webcam frame. Each detected face is cropped and preprocessed before being passed to DeepFace for pretrained facial emotion analysis. The application does not train its own emotion model or claim a project-specific training dataset.

The implemented pipeline is:

`Image/Webcam Input -> Face Detection -> Face Preprocessing -> DeepFace Emotion Analysis -> Emotion and Confidence -> Mood Mapping -> Music Recommendation -> Playback -> History`

The model result supplies an emotion and confidence value. The emotion is mapped to a broader mood using the configurable mapping in `data/emotions.json`. The recommender selects local audio from the configured mood folder when available, or from the existing compatibility library when the primary music directory has no supported audio. Webcam mode automatically plays a selected track when the smoothed mood changes; image mode plays its recommendation only when `--play` is supplied. Successful analyses are stored in JSON history, and pytest tests cover the deterministic application components.

## Limitations and Future Scope
Lighting, occlusion, camera quality, multiple faces, cultural and contextual limitations of emotion recognition, model-resource downloads, and CPU inference speed can affect results. Facial emotion recognition is probabilistic and should not be treated as a definitive measurement of a person’s internal emotional state. Future work could add personalized playlists, richer recommendations, improved temporal smoothing, and mobile deployment.
