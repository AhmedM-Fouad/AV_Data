#!/usr/bin/env python3
import rosbag
import cv2
from cv_bridge import CvBridge
import csv
import os

bag_path = "neural.bag"   # <-- change this
image_topic = "/camera/image_raw"
steer_topic = "/ackermann_cmd"

# Output folders/files
image_folder = "images"
image_csv = "images.csv"
steer_csv = "steering.csv"

os.makedirs(image_folder, exist_ok=True)
bridge = CvBridge()

# -----------------------------
# CSV FILES SETUP
# -----------------------------
img_csv_file = open(image_csv, "w", newline="")
img_writer = csv.writer(img_csv_file)
img_writer.writerow(["timestamp", "filename"])

steer_csv_file = open(steer_csv, "w", newline="")
steer_writer = csv.writer(steer_csv_file)
steer_writer.writerow(["timestamp", "steering_angle"])

# -----------------------------
# READ BAG
# -----------------------------
print("Reading bag:", bag_path)
bag = rosbag.Bag(bag_path, "r")

for topic, msg, t in bag.read_messages():
    ts = t.to_sec()

    # -----------------------------
    # EXTRACT IMAGES
    # -----------------------------
    if topic == image_topic:
        try:
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            filename = f"{ts:.6f}.png"
            filepath = os.path.join(image_folder, filename)
            cv2.imwrite(filepath, cv_img)

            img_writer.writerow([ts, filename])
            print(f"[IMG] {filename}")
        except Exception as e:
            print("Image error:", e)

    # -----------------------------
    # EXTRACT STEERING
    # -----------------------------
    if topic == steer_topic:
        try:
            steering_angle = msg.drive.steering_angle
            steer_writer.writerow([ts, steering_angle])
            print(f"[STEER] {ts} angle={steering_angle}")
        except Exception as e:
            print("Steering error:", e)

bag.close()
img_csv_file.close()
steer_csv_file.close()

print("\nDone! Images saved in /images and CSV files created.")
