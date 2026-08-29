"""Train an Ultralytics YOLO model for the Tiger Watch project.
Ref: https://docs.ultralytics.com/datasets#object-detection
Ref: https://hub.docker.com/r/ultralytics/ultralytics
"""

from __future__ import annotations
import argparse
from pathlib import Path
from typing import Any
from ultralytics import settings
#from ultralytics.yolo.utils.torch_utils import select_device

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train an Ultralytics YOLO model from a dataset YAML file.",
    )
    parser.add_argument(
        "--data",
        type=Path,
        required=True,
        help="Path to the Ultralytics dataset YAML file.",
    )
    parser.add_argument(
        "--model",
 #       default="yolo26n.pt",
        default="yolov9s.pt",
        help="Base model checkpoint or YAML architecture to train from.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=100,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--imgsz",
        type=int,
        default=640,
        help="Training image size.",
    )
    parser.add_argument(
        "--batch",
        type=int,
        default=16,
        help="Batch size.",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="Training device, for example '0', '0,1', 'cpu', or 'mps'.",
    )
    parser.add_argument(
        "--project",
        default="train",
        help="Directory where training runs are saved.",
    )
    parser.add_argument(
        "--name",
        default="tiger_watch_yolo_v9s",
        help="Run name under the project directory.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of dataloader workers.",
    )
    return parser.parse_args()


def train_model(args: argparse.Namespace) -> Any:
    data_path = args.data.expanduser().resolve()
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset YAML not found: {data_path}")

    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: ultralytics. Install project dependencies with "
            "`pip install -r requirements.txt`."
        ) from exc

    model = YOLO(args.model)
    return model.train(
        data=str(data_path),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        project=args.project,
        name=args.name,
        workers=args.workers,
    )


def main() -> None:
    print("Current ultralytics settings...", settings)
    args = parse_args()
    train_model(args)


if __name__ == "__main__":
    main()
