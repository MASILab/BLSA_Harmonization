from pathlib import Path
import os
import argparse
from tqdm import tqdm
import re

# find current path (assumed to be run in harmonization folder for now)
currentdir = Path(os.getcwd())
# find original dataset path
Old_dir = Path(str(currentdir) + "/BLSA/")
print(Old_dir)
#find organized dataset path
New_dir = Path(str(currentdir) + "/BIDS/BLSA/")
print(New_dir)

scan_types = ["FLAIR", "T2", "PD"]
sub_pattern = re.compile('BLSA_[0-9]{4}_[0-9]{2}-[0-9]_[0-9]{2}$')
for b in tqdm([x for x in Old_dir.glob('BLSA_*') if sub_pattern.match(x.name)]):
    #path to the raw scans, no accessors
    scans_path = Path(str(b) + "/SCANS/")
    #get the subject and session IDs
    splits = b.name.split('_')
    subj_id = "sub-" + "".join(splits[:2])
    sess_id = "ses-" + "".join(splits[2].split('-')) + "scanner" + splits[3]
    print(subj_id, sess_id)
    if not scans_path.exists():
        continue