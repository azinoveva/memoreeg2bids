import os.path as op
import pandas as pd
import json

from mne_bids import BIDSPath

import eeg
import make_json

SUBJECTS = range(1, 81)
BIDS_ROOT = op.join(op.dirname(op.realpath(__file__)), "bids")
DATA_PATH = op.join(op.dirname(op.realpath(__file__)), "data")


def make_dataset_description():
    """
    Create a description JSON for the dataset and dump it into the dataset_description.json file
    """
    dataset_description_json = {
        "Name": "mpib_memoreeg",  # REQUIRED
        "BIDSVersion": "1.7.0",  # REQUIRED
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
                "R": "righthanded",
                "L": "lefthanded",
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
                1: "",
                2: "",
                3: ""
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
            "Description": "A predetermined set of distractor stimuli used with a given participant (if distractor "
                           "used)",
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

    # Map handedness information from 0/1 to L/R
    participants['Righthanded (1=yes, 0=no)'].replace({0: 'L', 1: 'R'}, inplace=True)

    # We have 80 "true" participants with IDs ranging from p001 to p080.
    # Other IDs, e.g. for pilot participants, are to filter out.
    id_pattern = r'p0\d\d'
    participants = participants[participants.Parti_ID.str.match(id_pattern)]

    # add BIDS-formatted ID and rename columns
    participants['participant_id'] = [f'sub-{sub:02}' for sub in SUBJECTS]
    participants = participants.rename(
        columns={'Age': 'age', 'Righthanded (1=yes, 0=no)': 'handedness', 'Gender': 'gender',
                 'Stimuli_set': 'stimuli_set', 'Distractor (yes=1 no=0)': 'distractor',
                 'Distractor_set': 'distractor_set'})

    # Write relevant data to the participants.tsv file
    filename = op.join(BIDS_ROOT, "participants.tsv")
    participants[
        ['participant_id', 'age', 'handedness', 'gender', 'stimuli_set', 'distractor', 'distractor_set']].to_csv(
        filename, index=False, na_rep="n/a", sep="\t")


def make_bidsignore():
    text = """README.md"""

    filename = op.join(BIDS_ROOT, ".bidsignore")
    with open(filename, 'w', encoding='utf-8') as output:
        output.write(text)


def main():
    eeg_01 = eeg.Subject(80)
    eeg_01.eeg_to_bids()
    eeg_01.beh_to_bids()

    eeg_01 = eeg.Subject(1)
    eeg_01.eeg_to_bids()
    eeg_01.beh_to_bids()

    eeg_01 = eeg.Subject(2)
    eeg_01.eeg_to_bids()
    eeg_01.beh_to_bids()

    json_path = BIDSPath(root=BIDS_ROOT, suffix="events", extension=".json")
    json_eeg_events = make_json.eeg_events()
    with open(json_path, 'w', encoding='utf-8') as output:
        json.dump(json_eeg_events, output, ensure_ascii=False, indent=4)
        output.write("\n")


if __name__ == '__main__':
    main()
