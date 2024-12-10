// GeoJSON 파일 로드 및 지도에 추가
fetch(geoJsonUrl)
    .then(response => response.json())
    .then(data => {
        L.geoJson(data, {
            style: {
                color: 'orange',
                weight: 2,
            },
            onEachFeature: function (feature, layer) {
                if (feature.properties && feature.properties.adm_nm) {
                    layer.bindPopup(`<b>행정구:</b> ${feature.properties.adm_nm}`);
                    // 행정구 클릭 시 이벤트
                    layer.on('click', function () {
                        map.fitBounds(layer.getBounds()); // 해당 구역으로 확대
                        alert(`행정구 "${feature.properties.adm_nm}"를 클릭하셨습니다.`);

                        // 선택한 행정구를 서버에 업데이트 요청
                        fetch('/update_map', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({
                                district: feature.properties.adm_nm
                            })
                        })
                        .then(response => response.json())
                        .then(data => {
                            console.log("서버 응답:", data);
                        })
                        .catch(error => {
                            console.error("서버 요청 중 오류 발생:", error);
                        });
                    });
                }
            }
        }).addTo(map);
    })
    .catch(error => {
        console.error("GeoJSON 파일 로드 중 오류 발생:", error);
    });
