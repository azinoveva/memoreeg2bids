"""
Combined functionality for creating JSON sidecars. Following options are available:
- Create a dataset description (dataset_description.json)
- Create description of participants (participants.json)
- Create description of behavioral dataset for every participant (*_beh.json)
- Update *_eeg.json data from an EEG session

"""


def create(task):
    json = {
        'TaskName': task,
        'block_number': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trial': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_1_name': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_1_id': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_1_rot': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_2_name': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_2_id': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_2_rot': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'retro_cue': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_cue_id': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_cue_rot': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'type_of_task': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'type_of_pings': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'position_odd_pings': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_test_name': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_test_id': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_test_rot': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'rt_resp_abstract_first_key': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'rt_resp_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'acc_ori_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'final_rot_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_object_1': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_object_2': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_retrocue': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_taskcue': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_test': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_feedback': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_ping_10': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trigger_object_1': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trigger_object_2': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trigger_retrocue_1': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trigger_object_concrete': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'trigger_object_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'ping_null_5': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_null_1': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object_null_2': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'block_repe_null': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'threshold_fix': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object1scpos': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'object2scpos': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'objecttestscpos': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'distractors': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'distractor_name': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'distractor_id': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'distractor_rot': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'onset_distractor': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'acc_trial_id_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
        'final_id_abstract': {
            'LongName': '',
            'Description': '',
            'Levels': '',
        },
    }
    return json
