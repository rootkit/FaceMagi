python3 evaluation/prediction_single_path.py --gpu="-1" \
--test-file="./data/demo/list/demo.list" \
--pred-file="./result/demo_result.list" \
--attr-num="40" \
--prototxt-path="./outputs/deploy_single.prototxt" \
--caffemodel-path="./outputs/single_path_resnet_celeba.caffemodel" \
--feature-layer="pred" \
--root-folder="./data" \
--mean-file="./data/pretrained/ResNet_mean.binaryproto"
