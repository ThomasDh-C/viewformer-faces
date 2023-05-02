import boto3
import json
from tqdm import tqdm
import os
# import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

images_base_addr = '/home/tmd4/FEI_face_db/'
jpeg_files = [f for f in os.listdir(images_base_addr) if '.jpg' in f]

# Upload files to S3 bucket (7 mins): 2432/2800 --> [2434:]
s3 = boto3.resource('s3')
for f in tqdm(jpeg_files):
    data = open(images_base_addr + f, 'rb')
    s3.Bucket('viewformer').put_object(Key=f, Body=data)
    data.close()

# Delete file from S3 bucket code if needed 
# s3_client = boto3.client('s3')
# _ = s3_client.delete_object(Bucket='viewformer',Key='1-03.jpg')

# Run Rekognition on images (15 mins):
session = boto3.Session()
rekognition_client = session.client('rekognition')
for f in tqdm(jpeg_files):
    response = rekognition_client.detect_faces(Image={'S3Object':{'Bucket':'viewformer','Name':f}},
                                    Attributes=['ALL'])
    f_out = f.replace('.jpg', '.json')
    json_file = open(images_base_addr + f_out, 'w')
    out_data = json.dumps(response, indent=4, sort_keys=True)
    json_file.write(out_data)
    json_file.close()

def plot_img(f):
    # plot the original image
    plt.imshow(plt.imread(images_base_addr + f))
    fig = plt.gcf()
    img_w, img_h = fig.get_size_inches()*fig.dpi
    # get the json analysis data
    json_file = open(images_base_addr + f.replace('.jpg', '.json'), 'r')
    faceDetail = json.load(json_file)
    json_file.close()
    # draw a box around the face
    bound_box = faceDetail['FaceDetails'][0]['BoundingBox']
    ax = plt.gca()
    rect = Rectangle((bound_box['Left']*img_w,
                    bound_box['Top']*img_h ),
                    bound_box['Width']*img_w,
                    bound_box['Height']*img_h,
                    linewidth=2,edgecolor='r',facecolor='none')
    ax.add_patch(rect)
    pose = faceDetail['FaceDetails'][0]['Pose']
    plt.show()
    pitch, roll, yaw = pose['Pitch'], pose['Roll'], pose['Yaw']