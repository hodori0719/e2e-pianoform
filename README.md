# RUNNING THE CODE

# Dependencies

The dependencies for this repository can be opened in a conda environment with
   
    $ conda create --name <env> --file requirements.txt
    
Then activate with

    $ conda activate

# Data

The GrandStaff dataset is [publicly available](https://sites.google.com/view/multiscore-project/datasets) here.

!IMPORTANT: For the code in this repository to run, the **grandstaff.tgz file must be downloaded from the above link** and unzipped into the **Data/grandstaff** directory.

You MUST also run

    $ python3 vekern.py

To generate the corresponding .vekrn files.

# Testing
You can test a model trained on the ORIGINAL DATA with:
  
    $ python3 main.py config/GrandStaff/CRNN.gin
    
You can test a model trained on the MODIFIED DATA with:
  
    $ python3 main.py config/GrandStaff/CRNNV.gin

  By default, these are loaded with my best trained weights which are included in this repository. To change this, you must edit the code.
    
# Optional: Data Preprocessing
A random 80/10/10 partition of 2% of the original dataset can be generated then converted to equivalent vekern files with:

    python3 train_test_split.py
    python3 vekern_partition.py

**Note that doing so likely invalidate the currently trained weights provided with this repository.**

# Optional: Training
You can train a model on the ORIGINAL DATA from scratch with:
  
    $ python3 main.py config/GrandStaff/CRNN.gin
    
You can train a model on the MODIFIED DATA from scratch with:
  
    $ python3 main.py config/GrandStaff/CRNNV.gin

Note that these scripts, by default, will consecutively train for 45 epochs, the same as the final weights included in my report. However, depending on CPU/GPU limitations of the system, the code may not be able to consecutively run for 45 epochs due to a possible memory leak issue. In the experiment, both models have been trained in groupings of 15/5/10/10/5 epochs, for a total of 45. Also, training may take a considerable amount of time depending on the compute resources available.

This repository is based on the public implementation of the paper:

>**Antonio Ríos-Vila**, David Rizo, José M.Iñesta, Jorge Calvo-Zaragoza<br />
  *[End-to-end optical music recognition for pianoform sheet music](https://link.springer.com/article/10.1007/s10032-023-00432-z#citeas)*<br />
  International Journal on Document Analysis and Recognition

Which implements an end-to-end Optical Music Recognition method for pianoform music sheets.
