import sqlite3
import numpy as np

# 매칭된 박스 좌표 numpy 파일 불러오기
matching_boxes_with_same_color = np.load('matching_boxes.npy', allow_pickle=True)

# 데이터베이스 연결 (파일 없으면 생성됨)
conn = sqlite3.connect('bounding_boxes.db')
cursor = conn.cursor()

# 테이블 생성 (이미 테이블이 있으면 생략됨)
cursor.execute('''
CREATE TABLE IF NOT EXISTS matching_boxes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    x1 INTEGER,
    y1 INTEGER,
    x2 INTEGER,
    y2 INTEGER
)
''')

# 매칭된 박스 데이터를 데이터베이스에 저장
for box in matching_boxes_with_same_color:
    cursor.execute('''
    INSERT INTO matching_boxes (x1, y1, x2, y2) VALUES (?, ?, ?, ?)
    ''', (box[0], box[1], box[2], box[3]))

# 변경사항 저장 및 연결 종료
conn.commit()
conn.close()

print("Matching boxes with same color have been saved to the database.")

