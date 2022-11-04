"""
Following code formats collected EEG and behavioral data for every subject into BIDS-compatible format. This file
is NECESSARY to successfully execute source2bids.py.

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
# Import necessary packages
import os.path as op
import mne
import shutil
import json
import textfiles
import pandas as pd
from mne_bids import BIDSPath, write_raw_bids

# Default sourcedata path and BIDS path.
DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "../sourcedata")
BIDS_ROOT = op.join(op.dirname(op.realpath(__file__)), "..")


class Subject:
    """
    Class represents key data parameters for a single participant and allows for easier formatting.
    """
    # Stimulus matrix determines how stimulus IDs are assigned during the trials. E.g., STIM_MAT[1,2] contains
    # filename for 3rd stimulus in the 2nd subset (python iteration from 0).
    # I also needed to reverse-engineer this one, so I'll protect it at all costs :)
    _STIM_MAT = [['01_lighthouse.jpg', '02_radio03a.jpg', '02_table03.jpg'],
                 ['01_candelabra.jpg', '01_outdoorchair.jpg', '02_crown.jpg'],
                 ['01_lamppost01.jpg', '01_nightstand.jpg', '02_gazeboredone.jpg']]

    @property
    def STIM_MAT(self):
        return self._STIM_MAT

    def __init__(self, subject_id, age, sex, hand, stimuli, distractors, data_path=DATA_PATH):
        """
        Construct Subject class instance with given data
        :param int subject_id: Numerical ID of a subject
        :param int age: Age of a subject in years
        :param str sex: Gender of a subject (F/M)
        :param str hand: Dominating hand of a subject. (L/R)
        :param int stimuli: Chosen stimuli subset, number from 1 to 3
        :param int distractors: Chosen distractors subset, number from 1 to 3. Can be None if no distractors are used
        :param str data_path: Root folder with source data. See code/README for more
        """
        # Create a BIDS-ID for the subject (format: sub-XX)
        self.id = f'{subject_id:02}'
        self.age = age
        self.sex = sex
        self.hand = hand
        self.stimuli = stimuli
        self.distractors = distractors

        # Assign task name on basis of whether received distractors value is None (which means, no distractor used in
        # the task)
        if distractors:
            self.task = 'distractor'
        else:
            self.task = 'nodistractor'

        # Determine locations of EEG and behavioral data
        self.vhdr_path = op.join(data_path, f'eeg/p0{self.id}.vhdr')
        self.beh_path = op.join(data_path, f"behavioral/resultfile_p0{self.id}.txt")

    def get_event_type(self, trigger_id):
        """
        Helper function to determine type of event from its trigger ID
        :param int trigger_id: Trigger ID, ranges from 1 to 245
        :return str: Event description as a word
        """
        match trigger_id:
            case trigger_id if trigger_id in range(1, 57):
                return 'encoding'
            case trigger_id if trigger_id in range(101, 157):
                return 'distractor'
            case trigger_id if trigger_id in range(201, 217):
                return 'position'
            case trigger_id if trigger_id in range(221, 223):
                return 'retrocue'
            case 240:
                return 'left'
            case 241:
                return 'right'
            case 242:
                return 'down'
            case 243:
                return 'up'
            case 244:
                return 'feedback'
            case 245:
                return 'begin/end'
            case _:
                return 'n/a'

    def get_stim_file(self, trigger_id):
        """
        Helper function to determine shown/played stimulus file from its trigger ID. Look at STIM_MAT above for more
        :param int trigger_id: Trigger ID, ranges from 1 to 245
        :return str: Filename of shown/played stimulus
        """
        match trigger_id:
            case trigger_id if trigger_id in range(1, 17):
                return self.STIM_MAT[self.stimuli - 1][0]
            case trigger_id if trigger_id in range(21, 37):
                return self.STIM_MAT[self.stimuli - 1][1]
            case trigger_id if trigger_id in range(41, 57):
                return self.STIM_MAT[self.stimuli - 1][2]
            case trigger_id if trigger_id in range(101, 117) and self.distractors:
                return self.STIM_MAT[self.distractors - 1][0]
            case trigger_id if trigger_id in range(121, 137) and self.distractors:
                return self.STIM_MAT[self.distractors - 1][1]
            case trigger_id if trigger_id in range(141, 157) and self.distractors:
                return self.STIM_MAT[self.distractors - 1][2]
            case 221:
                return 'Two_F3_350.wav'
            case 222:
                return 'One_F3_350.wav'
            case 245:
                return 'test.wav'
            case _:
                return 'n/a'


    def eeg_to_bids(self, bids_root=BIDS_ROOT):
        """
        Expand the collected BrainVision data into BIDS-compliant structure.
        Per default, the data will be expanded into home directory of the script
        :param str bids_root: New location of the data
        """
        # First, let's find and read the source EEG data
        raw = mne.io.read_raw_brainvision(self.vhdr_path)

        # Add known metadata
        raw = raw.set_channel_types({"ECG": "ecg", "HEOG": "eog", "VEOG": "eog"})
        raw.info["line_freq"] = 50

        # Use mne-bids to expand the existing data
        bids_path = BIDSPath(subject=self.id, task=self.task, root=bids_root)
        write_raw_bids(raw, bids_path, overwrite=True)

        # Cleaning auto-generated events.tsv from mne-bids

        # Second, let's find where the auto-generated _events.tsv file is.
        events_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='eeg', suffix='events',
                               extension=".tsv")
        events = pd.read_csv(events_path, sep="\t")

        # I'll rename one column for a cleaner look
        events.rename(columns={'trial_type': 'trial'}, inplace=True)

        # We only want stimuli, so filter the dataset so that it only contains stimulus rows
        events = events[events.trial.str.match(r'Stimulus/S...')]

        # Fill in new columns according to information coded in stimulus ID:
        # Take the last 3 symbols of event comments and transform them to event codes
        events['trial'] = events['trial'].transform(lambda string: int(string[-3:]))
        # Define event type using event code
        events['event'] = events['trial'].transform(lambda stimulus: self.get_event_type(stimulus))
        # Determine stimulus file using event code
        events['stim_file'] = events['trial'].transform(lambda stimulus: self.get_stim_file(stimulus))
        # Add object rotation if exists
        events['rotation'] = events['trial'].transform(
            lambda stimulus: 'n/a' if (stimulus > 156) else (stimulus % 20 - 1) * 22.5 + 11.25)
        # Add object position if exists
        events['position'] = events['trial'].transform(
            lambda stimulus: (stimulus % 200 - 1) * 22.5 + 11.25 if (201 <= stimulus <= 216) else 'n/a')

        # Every object position is marked as a separate event RIGHT AFTER the event encoding an object and its
        # rotation. We use this to couple an object and its position, so that one row represents one real event.
        # Then we clean the table from unnecessary position-only rows.
        for index, event in events.iterrows():
            if event['event'] == 'position':
                events.at[index - 1, 'position'] = event['position']

        events = events[events.event != 'position']

        # Let's write the new dataframe to _events.tsv
        events[['onset', 'duration', 'trial', 'sample', 'stim_file', 'event', 'rotation', 'position']].to_csv(
            events_path, index=False, na_rep="n/a", sep="\t")

        # Next, let's add a JSON sidecar with description of *_events.tsv data

        json_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='eeg', suffix='events',
                             extension=".json")
        json_eeg_events = textfiles.eeg_events()
        textfiles.write(json_eeg_events, json_path)

        # Last, let's update the auto-generated metadata with available information.
        json_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='eeg', suffix='eeg',
                             extension=".json")
        with open(json_path, 'r+') as data:
            eeg_json = json.load(data)
            eeg_json["Instructions"] = "Instructions can be found..."
            eeg_json["EEGReference"] = "FCz"
            eeg_json["EEGGround"] = "Fpz"
            eeg_json["InstitutionName"] = "Max Plack Institute for Human Development"
            eeg_json["InstitutionAddress"] = "Lentzeallee 94, 14195 Berlin, Germany"
            eeg_json["ManufacturersModelName"] = "BrainAmp DC and BrainAmp ExG"
            eeg_json["SoftwareVersions"] = "BrainVision Recorder Professional V.1.24.0001"
            eeg_json["CapManufacturer"] = "EasyCAP"
            eeg_json["CapManufacturersModelName"] = "actiCAP 64 Ch Standard-2"
            del eeg_json["EMGChannelCount"]
            del eeg_json["MiscChannelCount"]
            data.seek(0)
            json.dump(eeg_json, data, ensure_ascii=False, indent=4)
            data.truncate()

    def beh_to_bids(self, bids_root=BIDS_ROOT):
        """
        Copy behavioral data of a subject to a new BIDS-compatible location and drop redundant/empty columns
        :param bids_root: New location of the data
        """
        # First, copy the initial behavioral data file into a BIDS-compatible folder
        bids_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='beh', suffix="beh",
                             extension=".tsv").mkdir()
        shutil.copy(self.beh_path, bids_path)

        # Drop redundant and empty columns
        beh_data = pd.read_csv(bids_path, sep='\t')

        # It is not enough to just use any number of whitespaces as delimiter. One edge case supposes that the
        # participant has neither changed the object, nor the orientation (e.g. the correct object has spawned in the
        # correct orientation). This means some data will be filled with whitespaces, and this causes data shift for
        # some trials when using delim_whitespace=True. So I'm stripping the whitespaces semi-manually.
        beh_data = beh_data.applymap(lambda x: str(x).replace(" ", ""))
        beh_data.columns = beh_data.columns.str.replace(" ", "")

        # Drop duplicate header rows (needs to happen before checking for empty cells!)
        beh_data = beh_data[beh_data.iloc[:, 0] != beh_data.columns[0]]

        # Columns to drop
        empty_cols = [col for col in beh_data.columns if
                      (beh_data[col].isnull().all() or beh_data[col].eq("NaN").all())]

        # Some columns already carry information from participants.tsv (e.g. age, gender...). Other columns do
        # not carry any relevant information and have been inherited through adjusting the script from previous
        # experiments.
        redundant_cols = ['task_version', 'date', 'subID', 'sub_gender', 'sub_age', 'practice', 'righthanded',
                          'colorset_pins', 'type_of_task', 'type_of_ings', 'position_odd_pings', 'object_test_name',
                          'block_repe_null', 'distractors']

        # For tasks without distractor, the would-be distractor values are still recorded. They do not carry
        # any valuable information and can be removed.
        if not self.distractors:
            redundant_cols += ['distractor_name', 'distractor_id', 'distractor_rot', 'onset_distractor']

        beh_data.drop(empty_cols + redundant_cols, axis=1, inplace=True)

        # Correct typo in column name
        beh_data.rename(columns={'object_2_ID': 'object_2_id'}, inplace=True)

        # Fill empty values
        beh_data.fillna("n/a", inplace=True)  # for true n/a
        beh_data = beh_data.replace("NaN", "n/a", regex=True)  # for NaN as strings
        beh_data = beh_data.replace("", "n/a", regex=True)  # for empty cells

        # Write cleared dataset into sub-<ID>_task-<taskname>_beh.tsv file
        beh_data.to_csv(bids_path, sep='\t', index=False)

        # Create an accompanying JSON sidecar with data description
        json_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype="beh", suffix="beh",
                             extension=".json")
        json_data = textfiles.behavioral(self.task)
        textfiles.write(json_data, json_path)

    def data(self):
        """
        Constructs and returns a dictionary which can be used as a data row in participants.tsv
        :return pd.DataFrame: Participant dataframe with a single row of information
        """
        participant_dict = pd.DataFrame([{'participant_id': f'sub-{self.id}',
                                          'age': self.age,
                                          'hand': self.hand,
                                          'sex': self.sex,
                                          'stimuli_set': self.stimuli,
                                          'distractor': {True: 1, False: 0}[bool(self.distractors)],
                                          'distractor_set': self.distractors}])
        return participant_dict
