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