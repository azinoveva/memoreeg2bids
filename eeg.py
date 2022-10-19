"""
Class for subject data manipulation
"""
import re
import os.path as op
from os import mkdir
import mne
import shutil
from mne_bids.copyfiles import copyfile_brainvision
from mne_bids import BIDSPath, write_raw_bids

ID_FORMAT = re.compile(r'\d\d')
DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "data")
BIDS_ROOT = op.dirname(op.realpath(__file__))


class Subject:
    """
    Class represents experiment data for a single participant and allows for easier formatting.
    """
    def __init__(self, subject_id, task):
        """
        Construct the BrainVision EEG data class.
        :param subject_id: (str) ID of the study subject. Matches the ID_FORMAT pattern.
        """
        if ID_FORMAT.match(subject_id):
            self.id = subject_id
            self.task = task
            self.vhdr_path = op.join(DATA_PATH, f'eeg/p0{subject_id[-2:]}.vhdr')
            self.raw = mne.io.read_raw_brainvision(self.vhdr_path)
        else:
            raise ValueError('This subject ID does not match given ID pattern!')

    def copy_eeg(self, new_path):
        """
        Copy EEG data to new destination
        :param new_path: (str) New destination of the files
        """
        copyfile_brainvision(self.vhdr_path, new_path, verbose=True)


    def eeg_to_bids(self):
        """
        Expand the BrainVision EEG data into BIDS.
        :param task: (str) Name of the recorded task
        """
        bids_path = BIDSPath(subject=self.id, task=self.task, root=BIDS_ROOT)
        write_raw_bids(self.raw, bids_path, overwrite=True)


    def beh_to_bids(self):
        """
        Filter necessary behavioral data of a participant and move it to corresponding BIDS folder
        :param task: (str) Name of the recorded task
        """
        bids_path = BIDSPath(subject=self.id, task=self.task, root=BIDS_ROOT, datatype='beh', suffix="beh", extension=".tsv").mkdir()
        shutil.copy(op.join(DATA_PATH, f"behavioral/resultfile_p0{self.id}.txt"), bids_path)


    def update_json(self, json_path):
        """
        Update sub-<sub_ID>_task-<taskname>_eeg.json with fresh information about the equipment.
        :param json_path: Path of the JSON sidecar to update
        """
        pass

