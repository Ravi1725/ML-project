import os
import shutil
import subprocess
import glob
import time

source = './test_image/'
dest1 = './dataset/train/A'
dest2 = './dataset/val/A'


for root, dirs, files in os.walk('./dataset/train/A'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


for root, dirs, files in os.walk('./dataset/val/A'):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))


#performing augrmentation
subprocess.call("python augment.py ./test_image fliph noise_0.01 noise_0.02 noise_0.05 trans_20_20 blur_1.0", shell=True)
#os.system("./augment/main.py ../test_image fliph noise_0.01 noise_0.02 noise_0.05 trans_20_20 blur_1.0")
#subprocess.call("cd ..",shell=True)
#count number of files
number_of_files = len([item for item in os.listdir(source) if os.path.isfile(os.path.join(source, item))])
print(number_of_files)

files = os.listdir(source)

percent = (number_of_files*80)//100
print(percent)
i=0
for f in files:
	if(i!=percent):
		shutil.move(source+f, dest1)
		i += 1
	else:
		shutil.move(source+f, dest2)



time.sleep(4)

subprocess.call("python face_detection.py", shell=True)
print("\nface_detected")
time.sleep(4)

subprocess.call("python face_embeddings.py", shell=True)
print("\nface_embedded")
time.sleep(4)

subprocess.call("python face_classification.py", shell=True)

time.sleep(4)

print("[+]DONE!")