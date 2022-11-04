"""
Following code manages annotations for mpib_memoreeg BIDS dataset and contains editable text information in form of
JSON, README, etc. This file is NECESSARY to successfully execute source2bids.py.

This code is licensed under MIT (https://opensource.org/licenses/MIT)

Copyright 2022 Juan Linde-Domingo, Aleksandra Zinoveva

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json


def eeg_events():
    """
    Generates an events.json file with description of eeg events' dataset
    :return: JSON sidecar with dataset description
    """
    contents = {
        "StimulusPresentation": {
            "OperatingSystem": "Windows 10 Enterprise V.1803",
            "SoftwareName": "MATLAB R2018a",
            "SoftwareRRID": "SCR_001622",
            "SoftwareVersion": "9.4.0.813654",
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
    return contents


def behavioral(task):
    """
    Generates an _beh.json file with description of behavioral events' dataset
    :param task: Name of the task. For this dataset: distractor or nodistractor
    :return: JSON sidecar with dataset description
    """
    contents = {
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
        'StimulusPresentation': {
            'OperatingSystem': 'Windows 10 Enterprise V.1803',
            'SoftwareName': 'MATLAB R2018a',
            'SoftwareRRID': 'SCR_001622',
            'SoftwareVersion': '9.4.0.813654',
        },
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
        },
        'trigger_object_abstract': {
            'Description': 'ID of the trigger corresponding to the object appearing first in the memory test'
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
            'Units': 'Pixels',
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

    return contents


def participants():
    """
    Generates a participants.json file with description of participants.tsv file.
    :return: JSON sidecar with dataset description
    """
    contents = {
        "participant_id": {
            "Description": "Unique participant identifier."
        },
        "age": {
            "Description": "Age of a participant.",
            "Units": "years"
        },
        "hand": {
            "Description": "Handedness of a participant, reported by the participant.",
            "Levels": {
                "R": "Right-handed",
                "L": "Left-handed",
            }
        },
        "sex": {
            "Description": "Gender of a participant, reported by the participant.",
            "Levels": {
                "F": "Female",
                "M": "Male"
            }
        },
        "stimuli_set": {
            "Description": "An ID for the set of task stimuli used with a given participant. There are 9 objects "
                           "altogether, for every participant 3 of them are picked pseudo-randomly for the whole "
                           "experiment, the number indicates the pseudo-random seed of this subgroup.",
            "Units": "Integer from 1 to 3"
        },
        "distractor": {
            "Description": "Presence of a distractor stimulus with a given participant.",
            "Levels": {
                1: "Distractors have been used. Task name: distractor",
                0: "No distractor has been used. Task name: nodistractor"

            }
        },
        "distractor_set": {
            "Description": "An ID for the set of distractor stimuli used with a given participant (if distractors "
                           "used in the task). There are 9 objects altogether, for every participant 3 of them are "
                           "picked pseudo-randomly for the whole experiment, the number indicates the pseudo-random "
                           "seed of this subgroup.",
            "Units": "Integer from 1 to 3"
        }
    }
    return contents


def dataset_description():
    """
    Generates a dataset_description JSON
    :return: JSON sidecar with dataset description
    """
    contents = {
        "Name": "mpib_memoreeg",  # REQUIRED
        "BIDSVersion": "1.8.0",  # REQUIRED
        "DatasetType": "raw",
        "License": "PDDL",
        "Authors": [
            "Juan Linde-Domingo",
            "Bernhard Spitzer"
        ],
        "Acknowledgements": "We thank Anouk Bielefeldt, Anna Faschinger, Aleksandra Zinoveva and Jann Wäscher for "
                            "help with participant management and data collection.",
        "HowToAcknowledge": "Please cite. The reference will be here soon!",
        "EthicsApproval": [
            "The study was approved by the ethics committee of the Max Planck Institute for Human Development, Berlin, "
            "Germany."
        ],
        "ReferencesAndLinks": [
            "Reference One",
            "Reference Two",
            "Reference Three"
        ],
        "DatasetDOI": "Will come with the acknowledgement."
    }

    return contents


def bidsignore():
    """
    Generates contents of .bidsignore file
    """
    contents = """
"""
    return contents


def readme():
    """
    Generates contents of README.md file
    """
    contents = """# README: mpib_memoreeg DATASET (BIDS)
    
This dataset contains raw data of the MemorEEG experiment conducted at the Max Planck Institute for Human 
Development (MPIB Berlin). 

The data is organized in Brain Imaging Data Structure format (BIDS, https://bids.neuroimaging.io/).
    
Relevant information can be also found here:
    
- Preprint: TBA
    
Source data is currently available on the file server of MPIB Berlin only. 

### Contact

[Juan Linde-Domingo](mailto:lindedomingo@mpib-berlin.de)

## License

If you use this dataset in your work, please consider citing it
as well as the references describing it.

This data is made available under the Public Domain Dedication and License v1.0
whose full text can be found at: http://opendatacommons.org/licenses/pddl/1.0/
See also the human-readable summary at:
https://opendatacommons.org/licenses/pddl/summary/

Please see the [LICENSE.txt](./LICENSE.txt) file for details.

## Overview

- [ ] Project name (if relevant)

- [ ] Year(s) that the project ran

If no `scans.tsv` is included, this could at least cover when the data acquisition
starter and ended. Local time of day is particularly relevant to subject state.

- [ ] Brief overview of the tasks in the experiment

A paragraph giving an overview of the experiment. This should include the
goals or purpose and a discussion about how the experiment tries to achieve
these goals.

- [ ] Description of the contents of the dataset

An easy thing to add is the output of the bids-validator that describes what type of
data and the number of subject one can expect to find in the dataset.

- [ ] Independent variables

A brief discussion of condition variables (sometimes called contrasts
or independent variables) that were varied across the experiment.

- [ ] Dependent variables

A brief discussion of the response variables (sometimes called the
dependent variables) that were measured and or calculated to assess
the effects of varying the condition variables. This might also include
questionnaires administered to assess behavioral aspects of the experiment.

- [ ] Control variables

A brief discussion of the control variables --- that is what aspects
were explicitly controlled in this experiment. The control variables might
include subject pool, environmental conditions, set up, or other things
that were explicitly controlled.

- [ ] Quality assessment of the data

Provide a short summary of the quality of the data ideally with descriptive statistics if relevant
and with a link to more comprehensive description (like with MRIQC) if possible.

## Methods

### Equipment

An experiment is performed in a shielded room with a participant resting on a chin rest to minimize head movements. 
The lights are turned out and the cabin is closed during the experiment. Connection to the participant is maintained 
via an intercom. 

#### Eye Tracking
- [SR Research Eyelink 1000 Plus Camera](https://www.sr-research.com/eyelink-1000-plus/)
- [SR Research Head Support](https://www.sr-research.com/eyelink-1000-plus/)

#### EEG
- [Brain Products BrainAmp DC](https://brainvision.com/products/brainamp-dc/)
- [Brain Products BrainAmp ExG](https://brainvision.com/products/brainamp-exg/)
- [Brain Products PowerPack](https://brainvision.com/products/powerpack/)
- Brain Products actiCap Control Box
- Brain Products Splitter Box aC-eb32
- EASYCAP 64Ch Standard Cap with actiCap holders

### Setup

After arrival, every new participant receives a set of documents to familiarize themselves with following topics:

1. Study information and consent for data collection and processing (example [here](./sourcedata/irb_data_protection/EV_MemorEEG.docx))
2. Extract from MPIB Hygiene Protocol (full version [here](./sourcedata/irb_data_protection/MPIB_HygieneProtocol_V1.3%20-%20German.pdf))

Directly after, the preparation of an EEG-setup takes place. The participant is provided full information on preparation 
and is given an opportunity to ask questions at any time.

After the preparation is complete, the participant makes themselves familiar with task instructions and completes a 
short test version of their assigned task. Only after the participant feels comfortable with the task, the session 
(and the recording) can begin. Usually this takes 2-3 test runs of 10 trials each.

### Task organization

Every participant is assigned a task type:

- Task with distractor (marked as *task-distractor* in subject files)
- Task without distractor (marked as *task-nodistractor* in subject files)

In tasks with distractor, an irrelevant item is displayed on the screen before the memory test. One participant 
always completes one task of one type only. 

The task is divided into 10 blocks (each block is 10% of the complete task). After every task, the participant is 
offered a chance to make a pause (open the cabin door, switch the lights on, have a water etc.). Whether to accept, 
and for how long, is determined mostly by the participant's readiness in each individual case. 

### Additional data acquired

Collected eye tracking data can be found in the [sourcedata/eyetracking](./sourcedata/eyetracking) folder.

### Missing data

- sub-20: EEG data missing (technical error, no EEG data recorded)

## Acknowledgements

> Appelhoff et al., (2019). MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating 
their analysis. Journal of Open Source Software, 4(44), 1896, https://doi.org/10.21105/joss.01896 

> Brodeur, M. B., Guérard, K., Bouras, M. (2014). Bank of Standardized Stimuli (BOSS) Phase II: 930 New Normative 
Photos. PLOS ONE 9(9): e106953. https://doi.org/10.1371/journal.pone.0106953

> Gorgolewski, K., Auer, T., Calhoun, V. et al. The brain imaging data structure, a format for organizing and 
describing outputs of neuroimaging experiments. Sci Data 3, 160044 (2016). https://doi.org/10.1038/sdata.2016.44 """
    return contents


def changes():
    """
    Generates contents of CHANGES file
    """
    contents = """0.01 2022-11-02
    - Initial release
    """
    return contents


def write(text, path):
    """
    A huge amount of different JSON sidecars are created through the dataset conversion process. This function is
    therefore arbitrary but nice to have for the sake of readability.
    :param text: JSON structure to write into a file.
    :param path: Path of the file to write into (filename and extension included).
    :return: None
    """
    with open(path, 'w', encoding="utf-8") as output:
        json.dump(text, output, ensure_ascii=False, indent=4)
        output.write("\n")
