#python OCR_train.py --device gpu --model_name mobilenet_small --max_epoch 12 --batch_size 1024
#python OCR_train.py --device gpu --model_name shufflenet_v2 --max_epoch 12 --batch_size 1024
python OCR_train.py --device gpu --model_name resnet18 --max_epoch 16 --batch_size 4096