import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.utils.random as four


DATASET_NAME = "my_wildlife_dataset"
EXPORT_DIR = "/home/shon/Sandbox/datasets/YOLO_wildlife"
CLASSES = ["Dog", "Cat", "Tiger", "Bird", "Snake", "Bear"]


# 1. Load virtual container if the persistent dataset already exists; otherwise download it.
if fo.dataset_exists(DATASET_NAME):
    dataset = fo.load_dataset(DATASET_NAME)
    print(f"Loaded existing dataset '{DATASET_NAME}'")
else:
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
    print(f"Dataset '{DATASET_NAME}' created and saved successfully!")

# 2. Safety step: Wipe old tag attributes to prevent splitting bugs: https://github.com/voxel51/fiftyone/issues/1952
dataset.untag_samples(dataset.distinct("tags"))

# 3. Extract the list of valid class categories dynamically
# access the label field by assigned name label_field="ground_truth"
class_list = dataset.distinct("ground_truth.detections.label")
print(f"Discovered classes for YOLO: {class_list}")

# 4. Partition virtual samples inside FiftyOne (80% train / 20% val)
# https://docs.voxel51.com/api/fiftyone.utils.random.html
four.random_split(
    dataset,
    {"train": 0.8, "val": 0.2},
    seed=42
)

# 5. Export each split in YOLOv5 format. The `split` argument generates the
# images/, labels/, and dataset.yaml layout expected by YOLOv8/YOLOv9/YOLOv10.
for split in ("train", "val"):
    split_view = dataset.match_tags(split)
    print(f"Exporting {len(split_view)} samples to split '{split}'")

    split_view.export(
        export_dir=EXPORT_DIR,            # Double-check path permission
        dataset_type=fo.types.YOLOv5Dataset,
        label_field="ground_truth",       # Must match step 3
        split=split,
        classes=CLASSES,                  # Enforces explicit class indexes (limited set)
        overwrite=(split == "train"),     # Clear stale files once, then add val
    )

print(f"Dataset exported successfully to {EXPORT_DIR}")
