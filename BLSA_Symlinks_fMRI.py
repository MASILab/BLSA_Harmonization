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

#get fMRI
    # fmri_pattern = re.compile('/*run[0-9]{1}/NIFTI')
    for fmri in scans_path.glob('*r*/NIFTI'):
        # print(str(fmri))
        # if not f.exists(): 
        #     print("echo 'Subject {} Session {} does not have flair folder'".format(subj_id, sess_id))
        # else:
        try:
            # todo: figure out if you want to include FNs and FPs or just FPs in this
            fn = [x for x in fmri.glob('*_F*_r*.ni*')]
            # print(fn)
            run_id = re.split("/NIFTI/",str(fn))
            run_id = re.split("_run",run_id[1])
            # print(run_id[1])
            if len(run_id) > 1:
                run_id = re.split(".nii.gz",run_id[1])
            else:
                run_id = re.split("_r",run_id[0])
                run_id = re.split(".nii.gz",run_id[1])
            # todo: figure out what to name symlinks for fMRIs
            SymlinkPath = str(New_dir) + "/" + subj_id + "/" + sess_id + "/func/"+  subj_id + '_' + sess_id +'_run-' + run_id[0] + '_FMRI' + ".nii.gz"
            print(Create_Bash_Line(fn[0],SymlinkPath))
        except:
            print("echo 'Error: no fmri scan for {},{}'".format(subj_id, sess_id))