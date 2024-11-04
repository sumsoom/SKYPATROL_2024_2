import sys
import os
import torch
import cv2
import numpy as np

# mmrotate 모듈 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'mmrotate'))

# 필요한 모듈 가져오기
from mmdet.apis import init_detector
from mmrotate.apis import inference_detector_by_patches

# 모델 초기화
config_file = 'mmrotate/configs/oriented_rcnn/oriented_rcnn_r50_fpn_1x_dota_le90.py'
checkpoint_file = 'mmrotate/checkpoints/oriented_rcnn_r50_fpn_1x_dota_le90-6d2b2ce0.pth'
model = init_detector(config_file, checkpoint_file, device='cpu')

# 이미지 추론 및 bounding box 추출 함수
def get_bounding_boxes(model, image_path):
    # 패치 기반 추론을 위한 설정 값
    sizes = [600]  # 패치 크기 설정 (예: 600x600)
    steps = [400]  # 패치 간의 이동 간격 설정
    ratios = [1.0]  # 이미지 크기 비율 설정
    merge_iou_thr = 0.5  # 결과 병합 시 사용할 IoU 임계값

    result = inference_detector_by_patches(model, image_path, sizes, steps, ratios, merge_iou_thr)
    
    bboxes = []
    for label_result in result:
        if len(label_result) == 0:
            continue
        for bbox in label_result:
            if bbox[-1] > 0.5:  # confidence threshold
                bboxes.append(bbox[:4].astype(int))
    return bboxes

# 이미지 파일 경로 설정
image1_path = 'images/image1.png'
image2_path = 'images/image2.png'

# 이미지 추론
bboxes1 = get_bounding_boxes(model, image1_path)
bboxes2 = get_bounding_boxes(model, image2_path)

# 좌표 비교 함수
def find_matching_boxes(bboxes1, bboxes2):
    matched_indices = []
    for i, box1 in enumerate(bboxes1):
        for j, box2 in enumerate(bboxes2):
            if np.array_equal(box1, box2):
                matched_indices.append((i, j))
    return matched_indices

matched_boxes = find_matching_boxes(bboxes1, bboxes2)

# 이미지 읽기
img1 = cv2.imread(image1_path)
img2 = cv2.imread(image2_path)

# 색상 추출 함수 (bounding box 내 평균 색상)
def get_average_color(image, box):
    x1, y1, x2, y2 = box
    roi = image[y1:y2, x1:x2]
    avg_color = cv2.mean(roi)[:3]  # BGR 포맷의 평균 색상 추출
    return avg_color

# 색상 비교 함수
def compare_colors(color1, color2, threshold=30):
    # 색상 값의 차이를 계산하여 threshold 이하인 경우 동일한 색상으로 간주
    diff = np.linalg.norm(np.array(color1) - np.array(color2))
    return diff < threshold

# 일치하는 bounding box들의 색상 비교 후 색상이 변하지 않은 좌표 저장
matching_boxes_with_same_color = []
for idx1, idx2 in matched_boxes:
    color1 = get_average_color(img1, bboxes1[idx1])
    color2 = get_average_color(img2, bboxes2[idx2])
    
    if compare_colors(color1, color2):
        matching_boxes_with_same_color.append(bboxes1[idx1])

# 색상이 변하지 않은 매칭된 박스 정보를 numpy 파일로 저장
np.save('matching_boxes.npy', matching_boxes_with_same_color)
print("Matching boxes with same color have been saved as numpy array.")