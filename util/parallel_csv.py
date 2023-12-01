# Usage: python3 parallel_csv.py file_list.txt directory_of_csv_files

import csv
import sys
import os

script_args = sys.argv
directory_prefix = script_args[2]
results_db = {}

extn_list_file = open(script_args[1], "r")
extn_list = extn_list_file.readlines()
extn_list = list(map(lambda x: x.strip("\n"),extn_list))
extn_list.sort()
extn_list_file.close()

csv_dir = os.getcwd() + "/" + directory_prefix
files = os.listdir(csv_dir)

print(files)

for file in files:
  file_name, file_extension = os.path.splitext(file)
  if file_extension == ".csv":
    f = open(csv_dir + "/" + file, "r")
    csvreader = csv.reader(f)
    for row in csvreader:
        assert len(row) == 3
        first_extn = row[0]
        second_extn = row[1]
        compat_bool = row[2] == "True"
        results_db[(first_extn, second_extn)] = compat_bool
    f.close()

compat_csv_file = open("pairwise.csv", "w")
writer = csv.writer(compat_csv_file)
writer.writerow(["first =>>"] + extn_list)

for second_extn in extn_list:
  row_to_write = [second_extn]
  for first_extn in extn_list:
    extn_pair = (first_extn, second_extn)
    val_to_write = "dne"
    if first_extn == second_extn:
      val_to_write = "n/a"
    elif extn_pair in results_db:
      val_to_write = "yes" if results_db[extn_pair] else "no"
    else:
      print(extn_pair)
      assert False
    
    row_to_write.append(val_to_write)
  writer.writerow(row_to_write)