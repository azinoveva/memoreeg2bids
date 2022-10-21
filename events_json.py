def create():
    json = {
        "StimulusPresentation": {
            "OperatingSystem": "Windows 10 - Version 1903",
            "SoftwareName": "MATLAB",
            "SoftwareRRID": "",
            "SoftwareVersion": "",
            "Code": "",
        },
        "onset": {
            "Description": "Onset of the event",
            "Units": "Seconds"
        },
        "duration": {
            "Description": "Duration of the event",
            "Units": "Seconds"
        },
        "sample": {
            "Description": "Onset of the event according to the sampling scheme of the recorded modality."
        },
        "trial": {
            "Description": 'The TTL trigger value (=EEG marker value) associated with an event. Positions of encoding '
                           'items have been recorded as separate events and are therefore incorporated in every event '
                           'via the script (markers S201 - S217 in the source data; only contain information about '
                           'position of an item shown beforehand). Positions for one item are encoded with numbers '
                           'from 1 to 16 where 1 represents 12PM direction, and every next position is 22.5 degrees '
                           'further in the clockwise direction',
            "Levels": {
                "1:16": "Orientations for encoding item 1",
                "21:36": "Orientations for encoding item 2",
                "41:56": "Orientations for encoding item 3",
                "101:116": "Orientations for distractor item 1",
                "121:136": "Orientations for distractor item 2",
                "141:156": "Orientations for distractor item 3",
                "221": "Retrocue One - participant is instructed to remember position of the first shown object",
                "222": "Retrocue Two - participant is instructed to remember position of the second shown object",
                "240": "Participant response: left arrow press (rotate item counter-clockwise)",
                "241": "Participant response: right arrow press (rotate item clockwise)",
                "242": "Participant response: down arrow press (switch item)",
                "243": "Participant response: up arrow press (accept item and orientation)",
                "244": "Feedback screen",
                "245": "Beginning or end of the task"
            }
        },
        "value": {
            "Description": "",
        },
        "event": {
            "Description": "Short description of marked event",
            "Levels": {
                "begin/end": "Beginning or end of one experiment session",
                "encoding-1": "Encoding item #1 is shown",
                "encoding-2": "Encoding item #2 is shown",
                "encoding-3": "Encoding item #3 is shown",
                "distractor-1": "Distractor item #1 is shown",
                "distractor-2": "Distractor item #2 is shown",
                "distractor-3": "Distractor item #3 is shown",
                "retrocue-1": "Participant hears a cue to remember the first shown encoding item",
                "retrocue-2": "Participant hears a cue to remember the second shown encoding item",
                "down": "Participant presses ARROW DOWN to change the item's ID",
                "left": "Participant presses ARROW LEFT to rotate the item counter-clockwise",
                "right": "Participant presses ARROW RIGHT to rotate the item clockwise",
                "up": "Participant presses ARROW UP to accept the item and the orientation",
                "feedback": "Participant receives feedback with correctness of the choice"
            }
        },
        "rotation": {
            "Description": "Rotation of the object, with reference to vertical axis",
            "Units": "Degrees, clockwise, beginning from upright position"
        },
        "position": {
            "Description": "Offset position of an object, always X units away from the fixation point",
            "Units": "Degrees, clockwise, beginning with 12PM position"
        },
    }
    return json
