import argparse
import pandas as pd
from pathlib import Path
from bids_validator import BIDSValidator


def arg_parse():

    parser = argparse.ArgumentParser(description="Validate dataset as BIDS formatted.")

    parser.add_argument('path', type=str, help="Path to the dataset to be examined.")

    args = parser.parse_args()

    return args

args = arg_parse()

dir_path = Path(args.path)

assert dir_path.exists(), "Error: %s is not a valid path" % str(dir_path)
assert dir_path.is_dir(), "Error: %s is not a directory" % str(dir_path)

validator = BIDSValidator()

# print(validator.is_bids(str(dir_path)))


#BIDS Validator requires that paths be starting from the dataset, not the root
    #i.e. "/sub-XXXX/..." not "/nfs2/harmonization/BIDS/ADNI/sub-XXXX/..."

df = pd.DataFrame(columns=['Filepath', 'is_BIDS'])
file_num = 0
for f in dir_path.rglob('*'):
    if not f.is_file(): #the BIDS_Validator is only checking files
        continue
    path = ""
    while f.name != dir_path.stem and f.name != "": #this loop constructs the path from the dataset
        #print(f.name)
        if f.is_dir():
            path = f.name + "/" + path
        else:
            path = f.name
        f = f.parent
    path = "/" + path
    df.loc[file_num, ['Filepath', 'is_BIDS']] = [path, validator.is_bids(path)]     #adding filepath to table and its status as BIDS valid or not
    file_num += 1


trues = df['is_BIDS'].values.sum()
for index, row in df.iterrows():
    if row['is_BIDS'] == False:
        print("File:", row['Filepath'], "is not BIDS validated")
#group_df = df.groupby(by="is_BIDS")
#for item, value in group_df:
#    print(value)
print("Ran BIDS validator against the {} dataset".format(dir_path.name))
print("Tested {} files for BIDS formatting.".format(file_num))
print("Number of files that passed BIDS validation: {}".format(trues))

#print("***{} is a valid BIDS formatted dataset.***".format(dir_path.stem))


#print("{} is a valid BIDS formatted directory".format(dir_path.name))
#else:
#    print("{} is not a properly BIDS formatted directory :(".format(dir_path.name))


