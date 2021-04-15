import glob
import os
import cv2

IMAGE_SHAPE = 128, 64, 3

dir_type = "train" # train, gallery and probe

base_dir_src = os.path.join(os.getcwd(), f'{dir_type}_images/')
base_dir_dst = os.path.join(os.getcwd(), 'bbox_train')
try:
    os.mkdir(base_dir_dst)
except FileExistsError:
    pass

files = glob.glob(base_dir_src+"*.jpg")

files = sorted([f.split("/")[-1] for f in files])

with open(f"vric_{dir_type}.txt") as f:
     annotations=f.read().splitlines()

image_names = []
id_labels = []
cam_labels = []
curr_id = None
for s in annotations:
    image_name, id_label, cam_label = s.split(" ")
    image_names.append(image_name)
    id_labels.append(id_label)
    cam_labels.append(int(cam_label))


unique_ids = set([i for i in id_labels])
dir_names = {uid:f'{i+1:04d}' for i,uid in enumerate(unique_ids)}
id_totals = {f'{i+1:04d}':[] for i,uid in enumerate(unique_ids)}

# create directories
for dir_name in dir_names.values():
    try:
        os.mkdir(os.path.join(base_dir_dst, dir_name))
    except FileExistsError:
        print(f"Dir {dir_name} already exists!")
        pass

for image_name, id_label, cam_label in zip(image_names, id_labels, cam_labels):
    src = os.path.join(base_dir_src, image_name)
    final_name = dir_names[id_label], dir_names[id_label]+f"{cam_label:03d}_{image_name.split('.')[0]}.jpg"
    dst = os.path.join(base_dir_dst, *final_name)
    id_totals[dir_names[id_label]].append((image_name,final_name))
    try:
        image = cv2.imread(src, cv2.IMREAD_COLOR)
        cv2.imwrite(dst, cv2.resize(image, IMAGE_SHAPE[:-1]))
    except FileNotFoundError:
        print(src, dst + " => NOT FOUND!")
        pass