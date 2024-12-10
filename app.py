from flask import Flask, render_template, jsonify, request, send_from_directory
import folium
import json
from shapely.geometry import shape
import pandas as pd
import os

# Flask 앱 초기화
app = Flask(__name__, static_folder='static', template_folder='templates')

# GeoJSON 데이터 로드
with open('GeoJSON/hangjeongdong_인천광역시.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# 행정동 중심 좌표 계산
districts_info = []
for feature in geojson_data['features']:
    polygon = shape(feature['geometry'])  # shapely 폴리곤 변환
    center = polygon.centroid  # 중심 계산
    districts_info.append({
        "name": feature["properties"]["adm_nm"],
        "center": [center.y, center.x]  # 위도, 경도 형식
    })

# 메인 페이지 렌더링
@app.route('/')
def index():
    return render_template('index.html')

# Folium 지도 렌더링
@app.route('/map')
def map_view():
    folium_map = folium.Map(location=[37.4563, 126.7052], zoom_start=11)

    # GeoJSON 경계 추가
    folium.GeoJson(
        geojson_data,
        name='geojson'
    ).add_to(folium_map)

    folium.LayerControl().add_to(folium_map)
    folium_map.save('templates/map.html')  # HTML 파일로 저장
    return render_template('map.html')

# 행정동 정보 반환
@app.route('/districts')
def get_districts():
    return jsonify(districts_info)

# GeoJSON 데이터 반환
@app.route('/geojson')
def get_geojson():
    return jsonify(geojson_data)

# CSV 파일 경로
csv_file_path = 'matched_objects.csv'

# CSV 데이터를 JSON 형태로 반환
@app.route('/bounding_boxes', methods=['GET'])
def bounding_boxes():
    df = pd.read_csv(csv_file_path)
    data = df.to_dict(orient='records')
    return jsonify(data)

# 이미지 및 정적 파일 제공
@app.route('/static/<path:filename>')
def serve_static_file(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/icons/<path:filename>')
def serve_icons(filename):
    icons_directory = os.path.join(app.static_folder, 'icons')
    return send_from_directory(icons_directory, filename)

# Flask 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
