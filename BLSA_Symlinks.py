from pathlib import Path
import os
import argparse
from tqdm import tqdm
import re
import glob

def Create_Bash_Line(ogpath, newpath):
    return "ln -s " + str(ogpath) + " " + str(newpath)

# find current path (assumed to be run in harmonization folder for now)
currentdir = Path(os.getcwd())
# find original dataset path
Old_dir = Path(str(currentdir) + "/BLSA/")
# print(Old_dir)
#find organized dataset path
New_dir = Path(str(currentdir) + "/BIDS/BLSA/")
# print(New_dir)

sub_pattern = re.compile('BLSA_[0-9]{4}_[0-9]{2}-[0-9]_[0-9]{2}$')
for b in tqdm([x for x in Old_dir.glob('BLSA_*') if sub_pattern.match(x.name)]):
    #path to the raw scans, no accessors
    scans_path = Path(str(b) + "/SCANS/")
    #get the subject and session IDs
    splits = b.name.split('_')
    subj_id = "sub-" + "".join(splits[:2])
    sess_id = "ses-" + "".join(splits[2].split('-')) + "scanner" + splits[3]
    # print("\n",subj_id, sess_id)
    if not scans_path.exists():
        continue

#get FLAIR
    flair = Path(str(scans_path) + "/FLAIR/NIFTI/")
    # print(flair)
    if not flair.exists(): continue
    try:
        fn = [x for x in flair.glob('*FLAIR.ni*')]
        for f in fn: str(f)
        SymlinkPath = str(New_dir) + "/" + subj_id + "/" + sess_id + "/anat/"+  subj_id + '_' + sess_id +'_FLAIR' + ".nii.gz"
        print(Create_Bash_Line(f,SymlinkPath))
    except:
        print("echo 'Error: no flair for {},{}'".format(subj_id, sess_id))

#get PD
    pd = Path(str(scans_path) + "/PD/NIFTI")
    if not pd.exists(): continue
    try:
        pdn = [x for x in pd.glob('*PD.ni*')]
        for p in pdn: str(p)
        SymlinkPath = str(New_dir) + "/" + subj_id + "/" + sess_id + "/anat/"+  subj_id + '_' + sess_id +'_PD' + ".nii.gz"
        print(Create_Bash_Line(p,SymlinkPath))
    except:
        print("echo 'Error: no pd for {},{}'".format(subj_id, sess_id))

#get T2
    t2 = Path(str(scans_path) + "/T2/NIFTI")
    if not t2.exists(): continue
    try:
        t2n = [x for x in t2.glob('*T2.ni*')]
        for t in t2n: str(f)
        SymlinkPath = str(New_dir) + "/" + subj_id + "/" + sess_id + "/anat/"+  subj_id + '_' + sess_id +'_T2w' + ".nii.gz"
        print(Create_Bash_Line(t,SymlinkPath))
    except:
        print("echo 'Error: no t2 for {},{}'".format(subj_id, sess_id))