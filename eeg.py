"""
Class for subject data manipulation
"""
import os.path as op
import mne
import shutil
import json
import beh_json
import events_json
import datetime

import pandas as pd
from numpy import nan
from mne_bids import BIDSPath, write_raw_bids

DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "data")
BIDS_ROOT = op.dirname(op.realpath(__file__))

def get_object_type(stimulus):
    match stimulus:
        case stimulus if stimulus in range(1, 17):
            return 'encoding-1'
        case stimulus if stimulus in range(21, 37):
            return 'encoding-2'
        case stimulus if stimulus in range(41, 57):
            return 'encoding-3'
        case stimulus if stimulus in range(101, 117):
            return 'distractor-1'
        case stimulus if stimulus in range(121, 137):
            return 'distractor-2'
        case stimulus if stimulus in range(141, 157):
            return 'distractor-3'
        case stimulus if stimulus in range(201, 217):
            return 'position'
        case 221:
            return 'retrocue-1'
        case 222:
            return 'retrocue-2'
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
            return nan


class Subject:
    """
    Class represents experiment data for a single participant and allows for easier formatting.
    """

    def __init__(self, subject_id, data_path=DATA_PATH):
        """
        Construct necessary subject data.
        :param subject_id: (int) ID of the experiment participant
        """
        self.id = f'{subject_id:02}'

        # Here I'm using the agreement to test every second subject without distractor.
        if subject_id % 2 == 1:
            self.task = 'distractor'
        else:
            self.task = 'nodistractor'

        self.vhdr_path = op.join(data_path, f'eeg/p0{self.id}.vhdr')
        self.beh_path = op.join(data_path, f"behavioral/resultfile_p0{self.id}.txt")

    def eeg_to_bids(self, bids_root=BIDS_ROOT):
        """
        Expand the BrainVision EEG data into BIDS.
        """
        bids_path = BIDSPath(subject=self.id, task=self.task, root=bids_root)
        raw = mne.io.read_raw_brainvision(self.vhdr_path)

        # Add known metadata
        raw = raw.set_channel_types({"ECG": "ecg", "HEOG": "eog", "VEOG": "eog"})
        raw.info["line_freq"] = 50

        write_raw_bids(raw, bids_path, overwrite=True)

        # Cleaning auto-generated events.tsv from mne-bids
        events_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='eeg', suffix='events', extension=".tsv")
        events = pd.read_csv(events_path, sep="\t")
        events.rename(columns={'trial_type': 'trial'}, inplace=True)

        # We only want stimuli, so filter the dataset so that it only contains stimulus rows
        events = events[events.trial.str.match(r'Stimulus/S...')]

        events['trial'] = events['trial'].transform(lambda string: int(string[-3:]))
        events['event'] = events['trial'].transform(lambda stimulus: get_object_type(stimulus))
        events['rotation'] = events['trial'].transform(lambda id: nan if (id > 156) else (id % 20 - 1)*22.5)
        events['position'] = events['trial'].transform(lambda id: (id % 200 - 1)*22.5 if (201 <= id <= 216) else nan)

        for index, event in events.iterrows():
            if event['event'] == 'position':
                events.at[index-1, 'position'] = event['position']

        events = events[events.event != 'position']

        events.to_csv(events_path, index=False, na_rep="n/a", sep="\t")


    def beh_to_bids(self, bids_root=BIDS_ROOT):
        """
        Copy behavioral data of a subject to a new BIDS-compatible location and drop redundant/empty columns
        """

        # First, copy the initial behavioral data file into a BIDS-compatible folder
        bids_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype='beh', suffix="beh",
                             extension=".tsv").mkdir()
        shutil.copy(self.beh_path, bids_path)

        # Drop redundant and empty columns
        beh_data = pd.read_csv(bids_path, delim_whitespace=True)

        # Columns to drop
        empty_cols = [col for col in beh_data.columns if beh_data[col].isnull().all()]
        redundant_cols = ['task_version', 'date', 'subID', 'sub_gender', 'sub_age', 'practice', 'righthanded',
                          'colorset_pins']

        beh_data.drop(empty_cols + redundant_cols, axis=1, inplace=True)

        # Drop duplicate header rows
        beh_data = beh_data[beh_data.iloc[:, 0] != beh_data.columns[0]]

        # Write cleared dataset into sub-<ID>_task-<taskname>_beh.tsv file
        beh_data.to_csv(bids_path, sep='\t', index=False)

        # Create an accompanying JSON sidecar with data description
        json_path = BIDSPath(subject=self.id, task=self.task, root=bids_root, datatype="beh", suffix="beh",
                             extension=".json")
        json_data = beh_json.create(self.task)
        with open(json_path, 'w', encoding='utf-8') as output:
            json.dump(json_data, output, ensure_ascii=False, indent=4)
            output.write("\n")
