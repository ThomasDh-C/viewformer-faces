import os
from tqdm import tqdm
import json
import pandas as pd

images_base_addr = '/home/tmd4/FEI_face_db/'
jpeg_files = [f for f in os.listdir(images_base_addr) if '.jpg' in f]
jpeg_files.sort(key=lambda x: int(x.split('-')[0])*100 + int(x.split('-')[1].split('.')[0]))

pose_dict = {'pitch': [], 'roll': [], 'yaw': [], 
            'pose_idx': [], 'image_addr': [], 'face_x': [], 'face_y': []}
# have to use left and top of pose
pitch, roll, yaw = {}, {}, {}
for f in jpeg_files:
    json_file = open(images_base_addr + f.replace('.jpg', '.json'), 'r')
    faceDetail = json.load(json_file)
    json_file.close()
    if len(faceDetail['FaceDetails']) == 0:
        # print(f)
        continue

    pose = faceDetail['FaceDetails'][0]['Pose']
    p, r, y = pose['Pitch'], pose['Roll'], pose['Yaw']
    pose_idx = (f.split('-')[1].split('.')[0])
    pose_dict['pitch'].append(p)
    pose_dict['roll'].append(r)
    pose_dict['yaw'].append(y)
    pose_dict['pose_idx'].append(pose_idx)
    pose_dict['image_addr'].append(f)
pose_df = pd.DataFrame(pose_dict)
pose_df_filt = pose_df[pose_df['pose_idx'].map(lambda x: int(x)) <= 11]
