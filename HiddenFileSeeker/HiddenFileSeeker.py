'''
Finds all hidden files of certain type in certain localization.
Prints path to hidden files, number of files checked and number of errors.
'''

import os
import ctypes

count = 0   # Count files
errors = 0  # Count errors

for (dirname, dirs, files) in os.walk('C:\\'):  # Seek only on drive C
    for filename in files:
        if filename.endswith('.png'):  # Choose type of files
            try:
                hidden = ctypes.windll.kernel32.GetFileAttributesW(dirname + "\\" + filename)
                if hidden == 34:
                    print(dirname + "\\" + filename)
                else:
                    count += 1
            except:  # Broad exception clause - just to count errors
                errors += 1
                continue


print("Files: " + str(count))
print("Errors: " + str(errors))