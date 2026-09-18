# Use Cases

```mermaid
flowchart LR
 User((User)) --> Image[Start image analysis]
 User --> Webcam[Start webcam analysis]
 User --> View[View emotion and confidence]
 User --> Mood[View mapped mood]
 User --> Music[View recommendation]
 User --> Play[Play image recommendation with --play]
 User --> Auto[Receive automatic webcam playback on mood change]
 User --> Controls[Use webcam controls]
 Controls --> Pause[Pause/resume with p]
 Controls --> Mute[Mute/unmute with m]
 Controls --> Save[Save capture with s]
 Controls --> Quit[Quit with q]
 User --> Capture[Save webcam capture]
 User --> History[View history]
 User --> Summary[View session summary]
```

Image analysis accepts a local image path. Webcam analysis continuously displays detected faces, emotion, confidence, and mood in the OpenCV window. The largest detected face is used as the primary listener for mood-change recommendation and playback; a saved capture records the current analyzed faces.
