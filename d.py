import os
import time
import shutil
import argparse

# parsing arguments
arg = argparse.ArgumentParser()
argprs.add_argument("-s", "--source_dir", required=True, help="Src Directory Path Please")
argprs.add_argument("-r", "--replica_dir", required=True, help="Rep Directory Path Please")
argprs.add_argument("-i", "--interval", required=True, help="Sync Interval Please")
argprs.add_argument("-l", "--log_file", required=True, help="Log File Path Please")
args = vars(argprs.parse_args())

# src rep Directory check
if os.path.exists(args["src_d"]) == False:
	print("Src Directory missing. Create? [y-n]")
	os.mkdir(args["src_d"])

if os.path.exists(args["rep_d"]) == False:
	print("Rep Directory missing. Create? [y-n]")
	os.mkdir(args["rep_d"])

# rep Directory delete
for filename in os.listdir(args["rep_d"]):
	filePath = os.path.join(args["rep_d"], filename)
	try:
		if os.path.isfile(filePath) or os.path.islink(filePath):
			os.unlink(filePath)
		elif os.path.isdir(filePath):
			shutil.rmtree(filePath)
	except Exception as e:
		print('Failed to delete %s. Reason: %s' % (filePath, e))

# log file init
f = open(args["log_f"], "w")
f.write("Sync Log\n")
f.write("====================\n")
f.write("utc_time\tfile_operation\tfile_name\n")

# sync
while True:
	for filename in os.listdir(args["src_d"]):
		filePath = os.path.join(args["src_d"], filename)
		replicaFilePath = os.path.join(args["rep_d"], filename)
				
		# copy file
		if os.path.isfile(filePath):
			if os.path.exists(replicaFilePath) == False:
				print("File Copy{}".format(filename))
				shutil.copyfile(filePath, replicaFilePath)
				f.write("{}\tcopy\t{}\n".format(time.time(), filename))

		# copy dir
		elif os.path.isdir(filePath):
			if os.path.exists(replicaFilePath) == False:
				print("Directory Creation{}".format(filename))
				os.mkdir(replicaFilePath)
				f.write("{}\tcreate\t{}\n".format(time.time(), filename))
				shutil.copytree(filePath, replicaFilePath, dirs_exist_ok=True)
				f.write("{}\tcopy\t{}\n".format(time.time(), filename.encode("utf-8")))

	# remove rep files
	for filename in os.listdir(args["rep_d"]):
		filePath = os.path.join(args["rep_d"], filename)
		sourceFilePath = os.path.join(args["src_d"], filename)

		# remove rep dirs
		if os.path.isdir(filePath):
			if os.path.exists(sourceFilePath) == False:
				print("Directory Deletion {}".format(filename))
				shutil.rmtree(filePath)
				f.write("{}\tdelete\t{}\n".format(time.time(), filename))

		# remove rep files
		elif os.path.isfile(filePath):
			if os.path.exists(sourceFilePath) == False:
				print("File Deletion {}".format(filename))
				os.unlink(filePath)
				f.write("{}\tdelete\t{}\n".format(time.time(), filename))

	# wait
	time.sleep(int(args["interval"]))
