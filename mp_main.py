# alternate version of main.py for experimenting with multiprocessing

import mp_funcs as my_plots
import multiprocessing as mp

file_to_read = "fake_data_10MB.txt"


if __name__ == "__main__": 
   
   my_plots.test_path(file_to_read)

   print("<<< Welcome to the multiprocessing edition of this assignment! >>>")

   # define a process for each main plot function
   p1 = mp.Process(target=my_plots.make_usernames_plot, args=(file_to_read, ))
   p2 = mp.Process(target=my_plots.make_emails_plot, args=(file_to_read, ))
   p3 = mp.Process(target=my_plots.make_birthyears_plot, args=(file_to_read, ))

   p1.start()
   print("  Started make_usernames_plot() in separate process")
   p2.start()
   print("  Started make_emails_plot() in separate process")
   p3.start()
   print("  Started make_birthyears_plot() in separate process")

   p1.join()
   p2.join()
   p3.join()