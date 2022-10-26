def eeg_events():
    """
    Generates an events.json file with description of eeg events' dataset
    :return: JSON sidecar with dataset description
    """
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
            "Description": "Offset position of an object, always away from the fixation point",
            "Units": "Degrees, clockwise, 12PM as a zero position"
        },
    }
    return json


def behavioral(task):
    """
    Generates an _beh.json file with description of behavioral events' dataset
    :param task: Name of the task. For this dataset: distractor or nodistractor
    :return: JSON sidecar with dataset description
    """
    json = {
        'TaskName': task,
        'TaskDescription': 'The participant is required to lock their gaze on the fixation point every time it is on '
                           'the screen. On each trial, two objects are presented one after the other, each rotated in '
                           'some way. After seeing these objects, a participant hears a cue (eiter One - "Eins", '
                           'or Two - "Zwei"). The cue indicates which object orientation is to be remembered. In '
                           'tasks with distractor, an irrelevant item is displayed on the screen before the memory '
                           'test. In the memory test, the participant sees an object in the center of the screen and '
                           'is required to match the item and the rotation for the cued object. The participant can '
                           'change the item by pressing DOWN, and rotate the item freely, pressing LEFT ('
                           'counter-clockwise) and RIGHT (clockwise). The participant then confirms the item and '
                           'its orientation by pressing UP. After confirmation, a feedback appears, telling how '
                           'accurate the participants response has been. After some time, the task times out and the '
                           'participant sees a feedback telling to respond faster. After that, the new trial starts.',
        'InstitutionName': 'Max Planck Institute for Human Development',
        'InstitutionAddress': 'Lentzeallee 94, 14195 Berlin, Germany',
        'block_number': {
            'Description': 'Every experiment session is divided into 10 blocks. The number indicates, which block '
                           'the current trial belongs to.',
            'Units': 'Integer from 1 to 10'
        },
        'trial': {
            'Description': 'Number of the trial. One trial is one full cycle from showing the first object to showing '
                           'the trial feedback.',
            'Units': 'Integer from 1 to 576'
        },
        'object_1_name': {
            'Description': 'Filename of an object shown first in the trial.'
        },
        'object_1_id': {
            'Description': 'ID of an object shown first in the trial. There are 9 objects altogether, for every '
                           'participant 3 of them are picked pseudo-randomly for the whole experiment, '
                           'the ID indicates the ID of an object in this picked subgroup.',
            'Units': 'Integer from 1 to 3'
        },
        'object_1_rot': {
            'Description': 'Rotation of an object shown first in the trial. There are 16 fixed equidistantly '
                           'distributed rotations, as if in 16 segments of a circle.',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'object_2_name': {
            'Description': 'Filename of an object shown second in the trial.'
        },
        'object_2_id': {
            'Description': 'ID of an object shown first in the trial. There are 9 objects altogether, for every '
                           'participant 3 of them are picked pseudo-randomly for the whole experiment, '
                           'the ID indicates the ID of an object in this picked subgroup.',
            'Units': 'Integer from 1 to 3'
        },
        'object_2_rot': {
            'Description': 'Rotation of an object shown first in the trial. There are 16 fixed equidistantly '
                           'distributed rotations, as if in 16 segments of a circle.',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'retro_cue': {
            'Description': 'Audial cue, telling a participant, which object and orientation to remember',
            'Levels': {
                '1': 'Eins - One. The participant should remember the first object.',
                '2': 'Zwei - Two. The participant should remember the second object.'
            },
        },
        'object_cue_id': {
            'Description': 'ID of an object cued, either ID of the first shown or of the second shown object, '
                           'depending on the cue.',
            'Units': 'Integer from 1 to 3'
        },
        'object_cue_rot': {
            'Description': 'Rotation of an object cued, either rotation of the first shown or of the second shown '
                           'object, depending on the cue.',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'object_test_id': {
            'Description': 'ID of an object which appeared on the screen first during memory test. Also picked '
                           'pseudo-randomly. There are 9 objects altogether, for every participant 3 of them are '
                           'picked pseudo-randomly for the whole experiment, the ID indicates the ID of an object in '
                           'this picked subgroup.',
            'Units': 'Integer from 1 to 3',
        },
        'object_test_rot': {
            'Description': 'Rotation, in which the first appeared object spawned on the screen during memory test. '
                           'Picked pseudo-randomly.',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'rt_resp_abstract_first_key': {
            'Description': 'Onset of the first button press by a participant. Has no value if the participant '
                           'confirmed the item and its rotation without adjusting.',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'rt_resp_abstract': {
            'Description': 'Total respond time from memory test beginning until confirmation???',
            'Units': 'Seconds'
        },
        'acc_ori_abstract': {
            'Description': 'Accuracy of confirmed object orientation',
            'Units': 'Percent'
        },
        'final_rot_abstract': {
            'Description': 'Object rotation confirmed by a participant',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'onset_object_1': {
            'Description': 'Time stamp when the first object in the trial is presented to the participant',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'onset_object_2': {
            'Description': 'Time stamp when the second item in the trial is presented to the participant',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'onset_retrocue': {
            'Description': 'Time stamp when the audio cue is played for the participant',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'onset_test': {
            'Description': 'Time stamp when the memory test starts',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'onset_feedback': {
            'Description': 'Time stamp when the feedback is presented to the participant',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'trigger_object_1': {
            'Description': 'ID of the trigger corresponding to the first presented object and its rotation',
            'Units': 'Integer from 1 to 3'
        },
        'trigger_object_2': {
            'Description': 'ID of the trigger corresponding to the second presented object and its rotation',
            'Units': 'Integer from 1 to 3'
        },
        'trigger_retrocue_1': {
            'Description': 'ID of the trigger corresponding to the audio cue',
            'Levels': '',
        },
        'trigger_object_abstract': {
            'Description': '??????'
        },
        'object_null_1': {
            'Description': 'Whether the FIXATE message appeared after the first shown object',
            'Levels': {
                0: 'No FIXATE message. Gaze of participant is locked on the fixation point.',
                1: 'FIXATE message. Gaze of participant is not locked on the fixation point.'
            }
        },
        'object_null_2': {
            'Description': 'Whether the FIXATE message appeared after the second shown object',
            'Levels': {
                0: 'No FIXATE message. Gaze of participant is locked on the fixation point.',
                1: 'FIXATE message. Gaze of participant is not locked on the fixation point.'
            }
        },
        'threshold_fix': {
            'Description': 'Threshold for a FIXATE message to appeared, sensitivity for gaze position',
            'Units': 'Pixels???',
        },
        'object1scpos': {
            'Description': 'Position of the first shown object on the screen. The object is always a fixed distance '
                           'away from the fixation point. There are 16 fixed equidistantly distributed positions, '
                           'as if in 16 segments of a circle. The positions are coded with 12PM as a zero, '
                           'clockwise direction',
            'Units': ' Integer from 1 to 16'
        },
        'object2scpos': {
            'Description': 'Position of the second shown object on the screen. The object is always a fixed distance '
                           'away from the fixation point. There are 16 fixed equidistantly distributed positions, '
                           'as if in 16 segments of a circle. The positions are coded with 12PM as a zero, '
                           'clockwise direction',
            'Units': ' Integer from 1 to 16'
        },
        'distractors': {
            'Description': 'Task version with or without use of distractor objects.',
            'Levels': {
                0: 'No distractors used.',
                1: 'Distractors used. They will be presented before the memory test.'
            }
        },
        'distractor_name': {
            'Description': 'Filename of an object shown as a distractor before the memory test.'
        },
        'distractor_id': {
            'Description': 'ID of an object shown as a distractor before the memory test. There are 9 objects '
                           'altogether, for every participant 3 of them are picked pseudo-randomly for the whole '
                           'experiment, the ID indicates the ID of an object in this picked subgroup.',
            'Units': 'Integer from 1 to 3'
        },
        'distractor_rot': {
            'Description': 'Rotation of an object shown as a distractor before the memory test. There are 16 fixed '
                           'equidistantly distributed rotations, as if in 16 segments of a circle.',
            'Units': 'Degrees, clockwise, 12PM as a zero position'
        },
        'onset_distractor': {
            'Description': 'Time stamp when the distractor item is presented to the participant',
            'Units': 'Seconds from the beginning of the experiment'
        },
        'acc_trial_id_abstract': {
            'Description': 'Whether the confirmed object is the same object that was to be memorized.',
            'Levels': {
                0: 'Incorrect object.',
                1: 'Correct object.'
            }
        },
        'final_id_abstract': {
            'Description': 'How many objects the participant observed (by pressing the DOWN button) before making a '
                           'decision',
            'Units': 'Integer, bigger than or equal to 1',
        },
    }
    return json
