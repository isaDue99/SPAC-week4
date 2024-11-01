# SPAC-week4
 Weekly assignment in Python. Processing big amounts of data using generators. Also experimenting with using multiprocessing for performance.

Includes 2 datasets generated with Faker in fake_data_10KB.txt and fake_data_10MB.txt. Further datasets of varying filesizes can be generated with filemaker.py.

To see it in action, run main.py to plot the 10MB dataset sequentially, or run mp_main.py to plot the 10MB dataset using multiprocessing. Other datasets (generated with filemaker.py) can be inputted by changing the file_to_read value at the top of these main files.

Profiling data generated with cProfile for the 2 main scripts can be found in /profiles, and the outputted plots for the 10KB, 10MB and a 1GB dataset can be seen in /plots.
The plots seem to indicate that the datasets were randomly generated from a uniform distribution.
Meanwhile, the profiles showcase that on small datasets (10KB) the overhead invoked by multiprocessing doesn't result in a faster program, but already at datasets of 10MB size there is a significant improvement in execution speed.