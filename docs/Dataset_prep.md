
Dataset source : Open Images Dataset v7 from Google | https://storage.googleapis.com/openimages/web/download_v7.html  
Dataset management: Voxel51 | https://docs.voxel51.com/index.html#
Using FiftyOne API we download datasets, split to "train" and "val", create YOLO friendly YAML 
Define variables in the header of the script before run, i.e.:
```
DATASET_NAME = "my_wildlife_dataset"
EXPORT_DIR = "/home/shon/Sandbox/datasets/YOLO_wildlife"
CLASSES = ["Dog", "Cat", "Tiger", "Bird", "Snake", "Bear"]
```
Due to enormous size of open-images dataset, I deliberately avoided default open-images-v7.yaml from Ultralytics https://docs.ultralytics.com/datasets/detect/open-images-v7#applications 
Instead I set fiftyOne dataset container small by picking split="validation" and max_samples=20000  and predefined list of CLASSES in my script.
```
    dataset = foz.load_zoo_dataset(
        "open-images-v7",
        split="validation",         # This keeps the sample count manageable on an RTX 4060 Ti.
        classes=CLASSES,
        label_types=["detections"], 
        label_field="ground_truth",
        max_samples=20000,          # Set max samples to 20,000
        dataset_name=DATASET_NAME,
        persistent=True,
)
```

```bash
python 51_dataset_to_YAML.py
```
51_dataset_to_YAML.py creates dataset.yaml and images, labels folders with train/val split and downloads dataset of predefined classes of limited sample size.
```
(.venv) (base) shon@s2:~/PycharmProjects/tiger_watch$ ls /home/shon/Sandbox/datasets/YOLO_wildlife
dataset.yaml  images  labels
```
dataset.yaml content:
```
names:
  0: Dog
  1: Cat
  2: Tiger
  3: Bird
  4: Snake
  5: Bear
path: /home/shon/Sandbox/datasets/YOLO_wildlife
train: ./images/train/
val: ./images/val/
```

