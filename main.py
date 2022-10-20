
import os.path as op
from os import mkdir, rename
import shutil
import pandas as pd
import mne
import json
from mne_bids import BIDSPath, write_raw_bids
from mne_bids.copyfiles import copyfile_brainvision
import eeg

SUBJECTS = range(1, 81)
BIDS_ROOT = op.dirname(op.realpath(__file__))
EEG_SOURCE = "data/eeg"
EYE_SOURCE = "data/eyetracking"
BEH_SOURCE = "data/behavioral"



def copy_brainvision():
    """
    :return:
    """
    data_path = op.join(op.dirname(op.realpath(__file__)), 'data/eeg')
    vhdr = op.join(data_path, 'p001.vhdr')
    vhdr_new = op.join(data_path, 'sub-01-.vhdr')
    copyfile_brainvision(vhdr, vhdr_new, verbose=True)
    raw = mne.io.read_raw_brainvision(vhdr)
    raw_renamed = mne.io.read_raw_brainvision(vhdr_new)

def make_dataset_description():
    """
    Create a description JSON for the dataset and dump it into the dataset_description.json file
    """
    dataset_description_json = {
        "Name": "mpib_memoreeg",    #REQUIRED
        "BIDSVersion": "1.7.0",     #REQUIRED
        "DatasetType": "raw",
        "License": "",
        "Authors": [
            ""
        ],
        "Acknowledgements": "",
        "HowToAcknowledge": "",
        "Funding": "",
        "EthicsApproval": "",
        "ReferencesAndLinks": "",
        "DatasetDOI": ""
    }
    filename = op.join(BIDS_ROOT, "dataset_description.json")
    with open(filename, "w", encoding="utf-8") as fout:
            json.dump(dataset_description_json, fout, ensure_ascii=False, indent=4)
            fout.write("\n")

def make_participants():
    """
    Create participant files:
    - participants.tsv with description of participants' characteristics
    - participants.json with description of columns and their values in participants.tsv
    """
    participants_json = {
        "participant_id": {
            "Description": "Unique participant identifier"
        },
        "age": {
            "Description": "Age of a participant",
            "Units": "years"
        },
        "handedness": {
            "Description": "Handedness of a participant, reported by the participant",
            "Levels": {
                1: "righthanded",
                0: "lefthanded",
            }
        },
        "gender": {
            "Description": "Gender of a participant, reported by the participant",
            "Levels": {
                "F": "Female",
                "M": "Male"
            }
        },
        "stimuli_set": {
            "Description": "A predetermined set of stimuli used with a given participant",
            "Levels": {
                1:"",
                2:"",
                3:""
            }
        },
        "distractor": {
            "Description": "Presence of a distractor stimulus with a given participant",
            "Levels": {
                1: "distractors have been used",
                0: "no distractor has been used"

            }
        },
        "distractor_set": {
            "Description": "A predetermined set of distractor stimuli used with a given participant (if distractor used)",
            "Levels": {
                1: "",
                2: "",
                3: ""
            }
        }
    }
    filename = op.join(BIDS_ROOT, "participants.json")
    with open(filename, "w", encoding="utf-8") as fout:
        json.dump(participants_json, fout, ensure_ascii=False, indent=4)
        fout.write("\n")

    # Take data from the log
    participants = pd.read_csv('participants_log.tsv', sep='\t')

    # We have 80 "true" participants with IDs ranging from p001 to p080.
    # Other IDs, e.g. for pilot participants, are to filter out.
    id_pattern = r'p0\d\d'
    participants = participants[participants.Parti_ID.str.match(id_pattern)]

    # add BIDS-formatted ID and rename columns
    participants['participant_id'] = [f'sub-{sub:02}' for sub in SUBJECTS]
    participants = participants.rename(columns={'Age': 'age', 'Righthanded (1=yes, 0=no)': 'handedness', 'Gender': 'gender', 'Stimuli_set': 'stimuli_set', 'Distractor (yes=1 no=0)': 'distractor', 'Distractor_set': 'distractor_set'})

    # Write relevant data to the participants.tsv file
    filename = op.join(BIDS_ROOT, "participants.tsv")
    participants[['participant_id', 'age', 'handedness', 'gender', 'stimuli_set', 'distractor', 'distractor_set']].to_csv(filename, index=False, na_rep="n/a", sep="\t")


def make_raw_bids():
    """
    With help of mne_bids create data structure, starting with EEG data
    """
    eeg_01 = eeg.Subject(2)
    eeg_01.eeg_to_bids()
    eeg_01.beh_to_bids()



def make_bidsignore():
    text = """README.md"""

    filename = op.join(BIDS_ROOT, ".bidsignore")
    with open(filename, 'w', encoding='utf-8') as output:
        output.write(text)


def main():
    make_raw_bids()


if __name__ == '__main__':
    main()
