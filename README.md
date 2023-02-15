# Sentinel 2023 - Learning to Threat Hunt with Python and Splunk

## Pre-requisites
1. Install Python (recommended to use either anaconda / miniconda / default python)
   - Miniconda: https://repo.anaconda.com/miniconda/
   - Anaconda: https://repo.anaconda.com/archive/
   - Python: https://www.python.org/downloads/
2. If you installed either Miniconda / Anaconda, it is recommended to run the following commands
   - `conda create -n Sentinel python=3.X` (python version of your choosing)
   - `conda activate Sentinel`
3. Installing Jupyter Notebook / Jupyter Lab for hands-on exercises
   - `pip3 install jupyterlab` (Recommended as jupyter lab is known to be more stable)
   - `pip3 install notebook`
4. Installing required python packages
   - `pip3 install pandas`

## For students
Please refer to the `students` folder. <br>
Inside it, you will find the folders/files relevant to you:
1. binaries
2. datasets
3. images
4. utils
5. student_notebooks
6. evtx_converter.py
7. parse_useragent_strings.py

The `datasets/windows` folders contains an attack scenario on
a windows server. The EVTX files has already been converted to
json, csv and xml format for you to process for later on.

For the first part of the exercise, you will be going through 
the materials found in `student_notebooks`.

The instructors will go through `student_notebooks/1_Context.ipynb`
to set the context of the attack. After which, you will be given approximately
45 minutes to do the exercises at your own pace. At the end of the exercise,
the instructor will go through the answers.

# For Instructors
Please refer to the `instructors` folder.<br>
Inside it, you will find the folders/files relevant to you:
1. binaries
2. datasets
3. images
4. utils
5. instructor_notebooks
6. student_notebooks
7. evtx_converter.py
8. parse_useragent_strings.py
9. Sentinel Attack Timeline.docx
10. Sentinel Program.pptx

There exist a `instructor_notebooks/hashes.txt` which stores the
md5, sha1 and sha512 hash of `instructor_notebooks/answer_engine.py`.
That way you will know if the students tried to cheat by modifying the `student_notebooks/answer_engine.py`
