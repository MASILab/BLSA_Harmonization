from pathlib import Path
import os
import argparse
from tqdm import tqdm
import re
import glob

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
    print("\n",subj_id, sess_id)
    if not scans_path.exists():
        continue

#get FLAIR
    flair = Path(str(scans_path) + "/FLAIR/NIFTI/")
    # print(flair)
    if not flair.exists(): continue
    try:
        fn = [x for x in flair.glob('*FLAIR.ni*')]
        for f in fn: print(str(f))
        # print(get_bash_line(BIDS_path, subj_id, sess_id, mpr))
    except:
        print("echo 'Error: no flair for {},{}'".format(subj_id, sess_id))

#get PD
    pd = Path(str(scans_path) + "/PD/NIFTI")
    if not pd.exists(): continue
    try:
        pdn = [x for x in pd.glob('*PD.ni*')]
        for f in pdn: print(str(f))
        # print(get_bash_line(BIDS_path, subj_id, sess_id, mpr))
    except:
        print("echo 'Error: no pd for {},{}'".format(subj_id, sess_id))

#get T2
    t2 = Path(str(scans_path) + "/T2/NIFTI")
    if not t2.exists(): continue
    try:
        t2n = [x for x in t2.glob('*T2.ni*')]
        for f in t2n: print(str(f))
        # print(get_bash_line(BIDS_path, subj_id, sess_id, mpr))
    except:
        print("echo 'Error: no t2 for {},{}'".format(subj_id, sess_id))