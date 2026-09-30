
Recommended base model for training yolo26n.pt optimized for edge deployments.
```
   )
    parser.add_argument(
        "--model",
        default="yolo26n.pt",
        help="Base model checkpoint or YAML architecture to train from.",
    )
```
Execute training, required arg: --data  
```bash
python train_Ultralytics_YOLO_model.py --data path/to/dataset.yaml
```

Snapshot of training start:
```

Current ultralytics settings... JSONDict("/home/shon/.config/Ultralytics/settings.json"):
{
  "settings_version": "0.0.6",
  "datasets_dir": "/home/shon/PycharmProjects/datasets",
  "weights_dir": "/home/shon/PycharmProjects/tiger_watch/weights",
  "runs_dir": "/home/shon/PycharmProjects/tiger_watch/runs",
  "uuid": "b84c7a844290d326925dbcbae9fb553d3363b1f32c00e2ba424fdc349f27a78f",
  "sync": true,
  "api_key": "",
  "openai_api_key": "",
  "clearml": true,
  "comet": true,
  "dvc": true,
  "hub": true,
  "mlflow": true,
  "neptune": true,
  "raytune": true,
  "tensorboard": false,
  "wandb": false,
  "vscode_msg": true,
  "openvino_msg": true
}
New https://pypi.org/project/ultralytics/8.4.89 available 😃 Update with 'pip install -U ultralytics'
Ultralytics 8.4.82 🚀 Python-3.12.3 torch-2.12.1+cu130 CUDA:0 (NVIDIA GeForce RTX 4060 Ti, 7806MiB)
engine/trainer: agnostic_nms=False, amp=True, angle=1.0, augment=False, auto_augment=randaugment, batch=16, bgr=0.0, box=7.5, cache=False, cfg=None, classes=None, close_mosaic=10, cls=0.5, cls_pw=0.0, compile=False, conf=None, copy_paste=0.0, copy_paste_mode=flip, cos_lr=False, cutmix=0.0, data=/home/shon/Sandbox/datasets/YOLO_wildlife/dataset.yaml, degrees=0.0, deterministic=True, device=None, dfl=1.5, dis=6.0, distill_model=None, dnn=False, dropout=0.0, dynamic=False, embed=None, end2end=None, epochs=100, erasing=0.4, exist_ok=False, fliplr=0.5, flipud=0.0, format=torchscript, fraction=1.0, freeze=None, hsv_h=0.015, hsv_s=0.7, hsv_v=0.4, imgsz=640, iou=0.7, keras=False, kobj=1.0, line_width=None, lr0=0.01, lrf=0.01, mask_ratio=4, max_det=300, mixup=0.0, mode=train, model=yolo26n.pt, momentum=0.937, mosaic=1.0, multi_scale=0.0, name=tiger_watch_yolo, nbs=64, nms=False, opset=None, optimize=False, optimizer=auto, overlap_mask=True, patience=100, perspective=0.0, plots=True, pose=12.0, pretrained=True, profile=False, project=runs/train, quantize=None, rect=False, resume=False, retina_masks=False, rle=1.0, save=True, save_conf=False, save_crop=False, save_dir=/home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo, save_frames=False, save_json=False, save_period=-1, save_txt=False, scale=0.5, seed=0, shear=0.0, show=False, show_boxes=True, show_conf=True, show_labels=True, simplify=True, single_cls=False, source=None, split=val, stream_buffer=False, task=detect, time=None, tracker=tracktrack.yaml, translate=0.1, val=True, verbose=True, vid_stride=1, visualize=False, warmup_bias_lr=0.1, warmup_epochs=3.0, warmup_momentum=0.8, weight_decay=0.0005, workers=8, workspace=None
Overriding model.yaml nc=80 with nc=6

                   from  n    params  module                                       arguments                     
  0                  -1  1       464  ultralytics.nn.modules.conv.Conv             [3, 16, 3, 2]                 
  1                  -1  1      4672  ultralytics.nn.modules.conv.Conv             [16, 32, 3, 2]                
  2                  -1  1      6640  ultralytics.nn.modules.block.C3k2            [32, 64, 1, False, 0.25]      
  3                  -1  1     36992  ultralytics.nn.modules.conv.Conv             [64, 64, 3, 2]                
  4                  -1  1     26080  ultralytics.nn.modules.block.C3k2            [64, 128, 1, False, 0.25]     
  5                  -1  1    147712  ultralytics.nn.modules.conv.Conv             [128, 128, 3, 2]              
  6                  -1  1     87040  ultralytics.nn.modules.block.C3k2            [128, 128, 1, True]           
  7                  -1  1    295424  ultralytics.nn.modules.conv.Conv             [128, 256, 3, 2]              
  8                  -1  1    346112  ultralytics.nn.modules.block.C3k2            [256, 256, 1, True]           
  9                  -1  1    164608  ultralytics.nn.modules.block.SPPF            [256, 256, 5, 3, True]        
 10                  -1  1    249728  ultralytics.nn.modules.block.C2PSA           [256, 256, 1]                 
 11                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']          
 12             [-1, 6]  1         0  ultralytics.nn.modules.conv.Concat           [1]                           
 13                  -1  1    119808  ultralytics.nn.modules.block.C3k2            [384, 128, 1, True]           
 14                  -1  1         0  torch.nn.modules.upsampling.Upsample         [None, 2, 'nearest']          
 15             [-1, 4]  1         0  ultralytics.nn.modules.conv.Concat           [1]                           
 16                  -1  1     34304  ultralytics.nn.modules.block.C3k2            [256, 64, 1, True]            
 17                  -1  1     36992  ultralytics.nn.modules.conv.Conv             [64, 64, 3, 2]                
 18            [-1, 13]  1         0  ultralytics.nn.modules.conv.Concat           [1]                           
 19                  -1  1     95232  ultralytics.nn.modules.block.C3k2            [192, 128, 1, True]           
 20                  -1  1    147712  ultralytics.nn.modules.conv.Conv             [128, 128, 3, 2]              
 21            [-1, 10]  1         0  ultralytics.nn.modules.conv.Concat           [1]                           
 22                  -1  1    463104  ultralytics.nn.modules.block.C3k2            [384, 256, 1, True, 0.5, True]
 23        [16, 19, 22]  1    243516  ultralytics.nn.modules.head.Detect           [6, 1, True, [64, 128, 256]]  
YOLO26n summary: 260 layers, 2,506,140 parameters, 2,506,140 gradients, 5.8 GFLOPs

Transferred 606/708 items from pretrained weights
AMP: running Automatic Mixed Precision (AMP) checks...
AMP: checks passed ✅
train: Fast image access ✅ (ping: 0.0±0.0 ms, read: 5571.7±1087.5 MB/s, size: 209.1 KB)
train: Scanning /home/shon/Sandbox/datasets/YOLO_wildlife/labels/train.cache... 3200 images, 2275 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 3200/3200 958.7Mit/s 0.0s
val: Fast image access ✅ (ping: 0.0±0.0 ms, read: 1622.6±1236.5 MB/s, size: 301.5 KB)
val: Scanning /home/shon/Sandbox/datasets/YOLO_wildlife/labels/val.cache... 800 images, 597 backgrounds, 0 corrupt: 100% ━━━━━━━━━━━━ 800/800 59.9Mit/s 0.0s
optimizer: 'optimizer=auto' found, ignoring 'lr0=0.01' and 'momentum=0.937' and determining best 'optimizer', 'lr0' and 'momentum' automatically... 
optimizer: AdamW(lr=0.001, momentum=0.9) with parameter groups 114 weight(decay=0.0), 126 weight(decay=0.0005), 126 bias(decay=0.0)
Plotting labels to /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo/labels.jpg... 
Image sizes 640 train, 640 val
Using 8 dataloader workers
Logging results to /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo
Starting training for 100 epochs...

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      1/100       2.5G     0.7632      11.94     0.0146          8        640: 100% ━━━━━━━━━━━━ 200/200 5.6it/s 35.7s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 2.7it/s 9.2s
                   all        800        256      0.708      0.287      0.384      0.294

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      2/100       3.5G     0.9152      8.445     0.0189         12        640: 100% ━━━━━━━━━━━━ 200/200 6.7it/s 29.7s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 6.3it/s 4.0s
                   all        800        256      0.718      0.236      0.418      0.239

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
      3/100       3.5G      1.105      4.995    0.02276         15        640: 100% ━━━━━━━━━━━━ 200/200 6.8it/s 29.5s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 6.2it/s 4.0s
                   all        800        256       0.76      0.213      0.413      0.245

 
```


Snapshot of training end:
```
      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
     99/100       3.5G     0.3432     0.1915   0.007753          9        640: 100% ━━━━━━━━━━━━ 200/200 6.9it/s 28.8s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 7.3it/s 3.4s
                   all        800        256      0.626      0.674      0.654      0.509

      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
    100/100       3.5G     0.3285      0.181   0.007696          6        640: 100% ━━━━━━━━━━━━ 200/200 6.9it/s 28.9s
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 7.3it/s 3.4s
                   all        800        256      0.662      0.674      0.675      0.513

100 epochs completed in 0.928 hours.
Optimizer stripped from /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo/weights/last.pt, 5.4MB
Optimizer stripped from /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo/weights/best.pt, 5.4MB

Validating /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo/weights/best.pt...
Ultralytics 8.4.82 🚀 Python-3.12.3 torch-2.12.1+cu130 CUDA:0 (NVIDIA GeForce RTX 4060 Ti, 7806MiB)
YOLO26n summary (fused): 122 layers, 2,376,006 parameters, 0 gradients, 5.2 GFLOPs
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100% ━━━━━━━━━━━━ 25/25 7.2it/s 3.5s
                   all        800        256      0.684      0.605      0.681      0.556
                   Dog        132        163      0.975      0.706      0.895      0.724
                   Cat         15         17      0.947      0.765      0.898      0.715
                 Tiger          2          3          0          0          0          0
                  Bird         52         71          1      0.556      0.783      0.596
                 Snake          2          2      0.499          1      0.828      0.746
Speed: 0.2ms preprocess, 1.2ms inference, 0.0ms loss, 0.4ms postprocess per image
Results saved to /home/shon/PycharmProjects/tiger_watch/runs/detect/runs/train/tiger_watch_yolo

 
```

Training results:  
https://github.com/ShonCamarlinghi/tiger_watch/tree/main/runs/train/tiger_watch_yolo


