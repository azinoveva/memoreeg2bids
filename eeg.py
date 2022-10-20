"""
Class for subject data manipulation
"""
import re
import os.path as op
import mne
import shutil
import json
import beh_json

import pandas as pd
from mne_bids.copyfiles import copyfile_brainvision
from mne_bids import BIDSPath, write_raw_bids

DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "data")
BIDS_ROOT = op.dirname(op.realpath(__file__))


class Subject:
    """
    Class represents experiment data for a single participant and allows for easier formatting.
    """

    def __init__(self, subject_id):
        """
        Construct the BrainVision EEG data class.
        :param subject_id: (str) ID of the study subject. Matches the ID_FORMAT pattern.
        :param task: (str) Identifier of an experiment task.
        """
        self.id = f'{subject_id:02}'
        if subject_id % 2 == 1:
            self.task = 'distractor'
        else:
            self.task = 'nodistractor'
        self.vhdr_path = op.join(DATA_PATH, f'eeg/p0{self.id}.vhdr')
        self.beh_path = op.join(DATA_PATH, f"behavioral/resultfile_p0{self.id}.txt")

    def copy_eeg(self, new_path):
        """
        Copy EEG data to new destination
        :param new_path: (str) New destination of the files
        """
        copyfile_brainvision(self.vhdr_path, new_path, verbose=True)

    def eeg_to_bids(self):
        """
        Expand the BrainVision EEG data into BIDS.
        """
        bids_path = BIDSPath(subject=self.id, task=self.task, root=BIDS_ROOT)
        raw = mne.io.read_raw_brainvision(self.vhdr_path)
        write_raw_bids(raw, bids_path, overwrite=True)

    def beh_to_bids(self):
        """
        Copy behavioral data of a subject to a new BIDS-compatible location and drop redundant/empty columns
        """

        # First, copy the initial behavioral data file into a BIDS-compatible folder
        bids_path = BIDSPath(subject=self.id, task=self.task, root=BIDS_ROOT, datatype='beh', suffix="beh",
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
        json_path = BIDSPath(subject=self.id, task=self.task, root=BIDS_ROOT, datatype="beh", suffix="beh",
                             extension=".json")
        json_data = beh_json.create(self.task)
        with open(json_path, 'w', encoding='utf-8') as output:
            json.dump(json_data, output, ensure_ascii=False, indent=4)
            output.write("\n")
