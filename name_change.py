import os
import re

def rename_images(directory):
    for filename in os.listdir(directory):
        if filename.startswith("object_"):
            # 파일명에서 정보 추출
            match = re.match(r'object_([\d\.]+)_([\d\.]+)_x(\d+)_y(\d+)_(\w+)\.png', filename)
            if not match:
                print(f"Skipping {filename}: pattern not matched")
                continue

            # 파일명에서 위도, 경도, x, y, 월 정보 추출
            latitude = match.group(1).replace(".", "")
            longitude = match.group(2).replace(".", "")
            x_coord = match.group(3)
            y_coord = match.group(4)
            month = match.group(5)

            # 일관된 형식의 새로운 파일명으로 변경
            new_filename = f"object_{latitude}_{longitude}_x{x_coord}_y{y_coord}_{month}.png"

            # 새로운 파일명 덮어쓰기
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_filename)
            try:
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
            except FileExistsError:
                print(f"File {new_filename} already exists. Skipping renaming.")

# 이미지 저장 디렉토리
image_directory = r"C:\Users\jo0o0\carde\flask_map\car_images"
rename_images(image_directory)
