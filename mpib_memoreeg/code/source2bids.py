"""
Following code formats source data of experiment into Brain Imaging Data Structure v1.8.0 (BIDS,
https://bids.neuroimaging.io).

BIDS standard compliance additionally tested on BIDS Validator v.1.9.9 (https://bids-standard.github.io/bids-validator/)

Required dependencies:
- mne <= 1.2.0
- mne-bids <= 0.11

The script (and two "subscripts" belonging to it, subject.py and textfiles.py) is intended to run from the
BIDS_ROOT/code folder and expects following folder/data structure:

BIDS_ROOT
├── code
│   └── source2bids.py
│   └── subject.py
│   └── textfiles.py
└── sourcedata
│   ├── behavioral
│   │   ├── resultfile_p001.txt
│   │   ...
│   ├── eeg
│   │   ├── p001.eeg
│   │   ├── p001.vhdr
│   │   ├── p001.vmrk
│   │   ...
│   ├── stimuli
│   ├── eyetracking
│   ├── irb_data_protection
│   └── participants_log.tsv
...

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
import os
import os.path as op
from distutils.dir_util import copy_tree
import pandas as pd
import urllib3
import textfiles
import subject as s

# Create constants for easier use
# Which or how many participants should be converted by MNE-BIDS? (future ID sequence)
SUBJECTS = range(1, 5)
# Should only annotations for the whole dataset be updated?
UPDATE_TEXT_ONLY = False
# Default data root for BIDS to convert into
BIDS_ROOT = op.join(op.dirname(op.realpath(__file__)), "..")
# Default source data root
DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "../sourcedata")


# make_ functions contain very similar code to generate text annotations.
# I put it this way for readability in main().

def make_dataset_description():
    """
    Create a description JSON for the complete dataset and put it into the dataset_description.json file
    """
    description = textfiles.dataset_description()
    filename = op.join(BIDS_ROOT, "dataset_description.json")
    textfiles.write(description, filename)


def make_participants_json():
    """
    Create participants.json with description of columns and their values in participants.tsv
    """
    filename = op.join(BIDS_ROOT, "participants.json")
    textfiles.write(textfiles.participants(), filename)


def make_bidsignore():
    """
    Create a .bidsignore file for BIDS-validator
    """
    bidsignore = textfiles.bidsignore()
    filename = op.join(BIDS_ROOT, ".bidsignore")
    with open(filename, "w") as output:
        output.write(bidsignore)


def make_readme():
    """
    Create a README markdown file with description of the dataset.
    """
    filename = op.join(BIDS_ROOT, "README.md")
    with open(filename, "w") as fout:
        fout.write(textfiles.readme())

    # Remove automatically generated README (from mne-bids, so will be only generated if subject data is updated)
    if not UPDATE_TEXT_ONLY:
        os.remove(op.join(BIDS_ROOT, "README"))


def make_changes():
    """
    Create a CHANGES file.
    """
    filename = op.join(BIDS_ROOT, "CHANGES")
    with open(filename, "w") as fout:
        fout.write(textfiles.changes())


def make_license():
    """
    Pull PDDL license description into LICENSE.
    """
    lic_text_url = "https://opendatacommons.org/licenses/pddl/pddl-10.txt"
    http = urllib3.PoolManager()
    req = http.request("GET", lic_text_url)
    assert req.status == 200
    license_str = req.data.decode("utf-8")

    filename = op.join(BIDS_ROOT, "LICENSE")
    with open(filename, "w") as output:
        output.write(license_str)


def make_bids_validator_config():
    """
    Make a .bidsconfig.json file.
    """
    # 38: As stated in README, one subject is always assigned one type of task. Therefore, BIDS validator will always
    # treat one of the missing task types as inconsistency.
    bids_validator_config_json = {
        "ignore": [
            38  # [WARN] Not all subjects contain the same files. Each subject should contain the same number of
            # files with the same naming unless some files are known to be missing. (code: 38 - INCONSISTENT_SUBJECTS)
        ]}
    filename = op.join(BIDS_ROOT, ".bids-validator-config.json")
    textfiles.write(bids_validator_config_json, filename)


def main():
    # Main idea is: process the participants_log.tsv line by line and transform accompanying subject data.

    # Read the log file
    log = pd.read_csv('../sourcedata/participants_log.tsv', sep='\t')

    # Map handedness information from 0/1 to L/R
    log['Righthanded (1=yes, 0=no)'].replace({0: 'L', 1: 'R'}, inplace=True)

    # We have 80 "true" participants with IDs ranging from p001 to p080.
    # Other IDs, e.g. for pilot participants, are to filter out.
    id_pattern = r'p0\d\d'
    log = log[log.Parti_ID.str.match(id_pattern)]

    # Create an empty dataframe with assigned column names as basis for future participants.tsv.
    participants = pd.DataFrame(columns=['participant_id',
                                         'age',
                                         'hand',
                                         'sex',
                                         'stimuli_set',
                                         'distractor',
                                         'distractor_set'])

    # Iterate through subjects: one subject - one row. SUBJECTS is a generated sequence of numbers
    # and can be altered above.
    for sub_id in SUBJECTS:

        # This is the data row with participant data.
        participant_data = log.iloc[sub_id - 1]

        # Take all known information out of it and use it to create a Subject class instance.
        age = participant_data['Age']
        hand = participant_data['Righthanded (1=yes, 0=no)']
        sex = participant_data['Gender']
        stimuli_set = participant_data['Stimuli_set']
        distractor = participant_data['Distractor (yes=1 no=0)']
        if distractor == 1:
            distractor_set = participant_data['Distractor_set']
        else:
            distractor_set = None

        participant = s.Subject(sub_id, age, sex, hand, stimuli_set, distractor_set)

        # There is an option to not just update text files but also convert source data anew with MNE-BIDS tool.
        if not UPDATE_TEXT_ONLY:

            # Transform accompanying data (EEG and behavioral).
            participant.eeg_to_bids()
            participant.beh_to_bids()

        # Append participant info to future participants.tsv
        participants = pd.concat([participants, participant.data()], ignore_index=True)

    # Fill empty places in the dataset and overwrite generated participants.tsv from MNE-BIDS with newly created one.
    participants.fillna('n/a', inplace=True)
    filename = op.join(BIDS_ROOT, "participants.tsv")
    participants.to_csv(filename, index=False, na_rep="n/a", sep="\t")

    # Once again, copy stimui folder if more than a text update is needed.
    if not UPDATE_TEXT_ONLY:
        # Copy stimuli from sourcedata
        copy_tree(op.join(DATA_PATH, "stimuli"), op.join(BIDS_ROOT, "stimuli"))

    # Finish up with self-explanatory annotations and config files.
    make_dataset_description()
    make_participants_json()

    make_readme()
    make_license()
    make_changes()

    make_bidsignore()
    make_bids_validator_config()


if __name__ == '__main__':
    main()
