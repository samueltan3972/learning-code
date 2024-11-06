'''To list down all the file recursively.
'''

# Method 1: pathlib (recommended)
from pathlib import Path

path = Path("../folder")
files = list(path.glob("**/*.txt"))


# Method 2: glob
import glob

path = "../folder" + "/**/*.txt"
files = glob.glob(path, recursive=True) # list

Path(files[0])