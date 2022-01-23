from enum import Enum, unique


@unique
class Event(Enum):
    BELL_PRESS_DETECTED = "sdm.devices.events.DoorbellChime.Chime"
    PERSON_DETECTED = "sdm.devices.events.CameraPerson.Person"
    VIDEO_CLIP_GENERATED = "sdm.devices.events.CameraClipPreview.ClipPreview"
    ANIMAL_DETECTED = ""
