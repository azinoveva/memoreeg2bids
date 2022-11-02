# README: memoreeg2bids
    
This code processes source data of the MemorEEG experiment conducted at the Max Planck Institute for Human 
Development (MPIB Berlin) into raw Brain Imaging Data Structure format (BIDS, https://bids.neuroimaging.io/).

Source data is currently available on the file server of MPIB Berlin only (see public folder of `zinoveva` in `FB-ARC/AMD` for an example).

Required dependencies:
- `mne` <= 1.2.0
- `mne-bids` <= 0.11

The script (and two "subscripts" belonging to it, `subject.py` and `textfiles.py`) is intended to run from the
BIDS_ROOT/code folder and expects following folder/data structure:

```
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
```