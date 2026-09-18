# Workflow

```mermaid
flowchart TD
 Input[Image or Webcam Input] --> Detect[Face Detection]
 Detect --> Process[Face Preprocessing]
 Process --> Emotion[DeepFace Emotion Analysis]
 Emotion --> Confidence[Emotion and Confidence]
 Confidence --> Mood[Mood Mapping]
 Mood --> Recommendation[Music Recommendation]
 Recommendation --> Playback[Playback]
 Confidence --> History[History Management]
 Mood --> History
 Recommendation --> History

 subgraph ImageMode[Image mode]
  ImageInput[Load image] --> ImageDetect[Detect each face]
  ImageDetect --> ImageAnalyze[Analyze each face]
  ImageAnalyze --> ImageOutput[Print emotion, confidence, mood, recommendation]
  ImageOutput --> ImagePlay{--play supplied?}
  ImagePlay -->|yes| ImagePlayback[Play selected track]
 end

 subgraph WebcamMode[Webcam mode]
  Camera[Read frame] --> Skip[Analyze every FRAME_SKIP frame]
  Skip --> Smooth[Temporal smoothing]
  Smooth --> Primary[Largest face is primary listener]
  Primary --> Change{Mood changed?}
  Change -->|yes| Auto[Recommend and automatically play]
  Camera --> Controls[Focused-window q/p/m/s controls]
  Controls --> Pause[p pauses/resumes analysis]
  Controls --> Mute[m mutes/unmutes music]
  Controls --> Save[s saves frame and current analyses]
  Controls --> Quit[q exits]
 end

 Input --> Detect
 Detect --> Process
 Process --> Emotion
 Emotion --> Confidence
 Mood --> Recommendation
```

The shared pipeline is face detection -> preprocessing -> emotion analysis -> confidence -> mood mapping -> recommendation -> playback -> history. Image mode processes a provided file once. Webcam mode continues in a loop, displays labels in the OpenCV window, skips frames according to `FRAME_SKIP`, smooths recent emotions, and triggers the primary recommendation/playback only when the mapped mood changes.
