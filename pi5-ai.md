# What the Pi 5 can do for this rover

Written 8 Nov 2026, while the motherboard meter test is still waiting. This note does not change the stage tests in `plan.md`. Stages 11 to 14 still have to pass with no website.

The brain is a Raspberry Pi 5 with 8 GB of memory and no AI chip. The camera is the USB webcam already in the parts list. The ESP32 keeps the motors, servos, and lights. If the Pi sends no motor command for 300 ms, the ESP32 stops the tracks.

## The rule that decides everything else

Seeing and talking can take longer than 300 ms. That is safe only when they run beside the drive program, not inside it. The drive program keeps talking to the ESP32 the whole time. A slow camera look, or a few seconds of listening, must not be what stops the motor commands.

## What passes the written tests, on the Pi, with no internet

| Stage | Job | Tool on the Pi | How it is used |
|---|---|---|---|
| 11 | Box a person, and name a cup, a chair, and other ordinary things | YOLO11n, the fast NCNN copy, 640 pixels wide | Two or three looks a second while driving. The CPU-only Pi 5 does about 7 looks a second when this model has the chip mostly to itself (135.7 ms, measured 27 Jan 2026). |
| 11 | Box a face | YuNet | Only when a person is already in view. At 640×480 a face box takes about 51 ms on a Pi 5. |
| 12 | Greet you by name, and call a stranger "a person" | SFace | One showing, a few saved face samples from that showing. Naming one face takes about 23 ms. The match has to be strict, or it will use your name for someone else. |
| 13 | Name a room it was shown | Compare a new picture with the pictures saved for each room | Every couple of seconds. There is no indoor GPS. Darkness and moved furniture will miss, and those misses go in the calibration table. |
| 14 | Say a short line in English, then the same line in Arabic | Piper | English voice `en_US lessac`, medium. Arabic voice `ar_JO kareem`, medium. A short line on a Pi 5 is under a second. |
| 14 | Hear a short sentence and answer in that language | Whisper, the multilingual **base** model, through whisper.cpp | After a gamepad button, not all the time. About 3 seconds on a Pi 5 for the published estimate. The English-only Whisper file cannot hear Arabic. |
| 15 | All of the above while driving | The same tools | The drive program stays separate. |

YOLO already knows person, cup, chair, couch, bed, bottle, dining table, tv, laptop, book, and potted plant. It does not know "face". That is why the face box is a second, smaller model.

## Hearing and speaking

Start with Whisper base, multilingual. The tiny model is faster (about 1.5 s) and often mishears Arabic. The small model hears better and takes about 8.5 s, so it is only for a parked retry when base is wrong. Those three times are the openHAB estimates for a Pi 5. The write-up does not say how long the test clip was, so treat them as a guide.

The answer is a filled-in sentence from what the camera last decided: "I see a cup", "This is the kitchen", "Hello, name". The gamepad button picks the moment to listen. Whisper's language guess picks the Piper voice. If the guess is unsure, the robot stays quiet.

A chat model is not required for the tests. Qwen2.5 1.5B can say freer sentences later, at about 8 to 11 words a second, and it uses about 1 GB. It runs only when the camera loop is paused and the rover is parked. An 8B chat model uses about 5 GB and about 1 to 2 words a second. It crowds out the camera. It stays off this robot.

## While it is driving, and when it is not

While the tracks are moving, the Pi does objects, faces, and the room match. It can speak a line it already knows. It does not listen the whole time, and it does not run a chat model. Motor noise and a full CPU make always-on listening fail.

When you press the talk button, listening runs, then one spoken answer. The drive program is still sending. If you are moving, the answer waits until the listen finishes. It does not stop the heartbeat.

## What the network can add, and what it must not replace

House Wi-Fi and a paid speech or vision service can hear noisy Arabic more reliably, talk beyond the command list, and describe an object or a room the robot was never shown. They send pictures and voice off the rover. If the Wi-Fi drops, the local path above is the one that still has to pass stages 11 to 14. Those stages say no website.

## What does not fit

- A medium or large YOLO. Those fall to about 2 looks a second and take almost the whole CPU.
- Whisper medium, at about 17 seconds and about 2 GB, during a drive.
- An 8B chat model at the same time as the camera.
- Always listening while the tracks are moving.
- Trusting one face photo in the dark, or a room name after the furniture moves. The plan already expects those misses.

## Power and the camera

A busy Pi draws more from the XL4016. If the Pi shows a lightning bolt or reboots during a vision test, the buck is not holding 5.10 V under that load. The fix is the supply, not a higher voltage setting.

The webcam part number did not match a published specification. Stage 10 shows the real picture. The models want a 640-wide image even if the camera can do more. If that webcam has no microphone, stage 14 needs a separate one. The motors are loud, so the mic wants to be near the person, not down by the tracks.

## Sources

- YOLO11n on a Pi 5, NCNN, 135.7 ms and 7.37 fps single-thread, image size 640. Kadir Mert Abatay, RPi YOLO Benchmark, 27 Jan 2026.
- YuNet 50.8 ms and SFace 23.4 ms at 640×480 on a Pi 5 8 GB, OpenCV 4.10, median of 100 runs. Swallow Incubate, Cortex-A76 face benchmark.
- Whisper tiny 1.5 s, base 3 s, small 8.5 s, medium 17 s, approximate, on a Pi 5. openHAB Whisper binding. Clip length not stated. Memory from whisper.cpp: base about 388 MB, small about 852 MB.
- Piper on a Pi 5, a short sentence under 1 second. Arabic voice `ar_JO kareem` is in the Piper voice list. English voice used here is `en_US lessac`.
- Qwen2.5 1.5B on a Pi 5, about 10 tokens/s and about 1 GB at Q4. Several 2026 Pi 5 measurements. Llama-class 8B at Q4 is about 5 GB and about 1 to 2 tokens/s.
