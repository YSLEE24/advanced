var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
    mapOption = { 
        center: new kakao.maps.LatLng(35.7,	127.7), // 지도의 중심좌표
        level: 12, // 지도의 확대 레벨
        draggable: false, // 지도 이동 비활성화
        zoomable: false   // 확대/축소 비활성화
    };

var map = new kakao.maps.Map(mapContainer, mapOption);

var imageSrc = "/static/images/어부방.png", // 마커이미지의 주소입니다    
imageSize = new kakao.maps.Size(74, 79), // 마커이미지의 크기입니다
imageOption = {offset: new kakao.maps.Point(37,68)}; // 마커이미지의 옵션입니다. 마커의 좌표와 일치시킬 이미지 안에서의 좌표를 설정합니다.

// 지역	위도 (Latitude)	경도 (Longitude)
// 서울특별시,	               37.5665,	126.9780,
// 부산광역시,	               35.1796,	129.0756,
// 대구광역시,	               35.8714,	128.6014,
// 인천광역시,	               37.4563,	126.7052,
// 광주광역시,	               35.1595,	126.8526,
// 대전광역시,	               36.3504,	127.3845,
// 울산광역시,	               35.5384,	129.3114,
// 세종특별자치시,	               36.5041,	127.2495,
// 경기도,	               37.4138,	127.5183,
// 강원특별자치도,	               37.8228,	128.1555,
// 충청북도,	               36.6358,	127.4917,
// 충청남도,	               36.6588,	126.6728,
// 전라북도,	               35.8206,	127.1088,
// 전라남도,	               34.8161,	126.4630,
// 경상북도,	               36.5760,	128.5056,
// 경상남도,	               35.4606,	128.2132,
// 제주특별자치도,	               33.4996,	126.5312,



var latitude = [37.5665, 35.1796, 35.8714, 37.4563, 35.1595, 36.3504, 35.5384, 36.5041, 37.4138, 37.8228, 36.6358, 36.6588, 35.8206, 34.8161, 36.5760, 35.4606, 33.4996]
var longitude = [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114, 127.2495, 127.5183, 128.1555, 127.4917, 126.6728, 127.1088, 126.4630, 128.5056, 128.2132, 126.5312]
// 마커의 이미지정보를 가지고 있는 마커이미지를 생성합니다
var i = 0
for ( i = 0; i < longitude.length; i++ ){
    var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize, imageOption),
    markerPosition = new kakao.maps.LatLng(latitude[i], longitude[i]); // 마커가 표시될 위치입니다
    // 마커를 생성합니다
    var marker = new kakao.maps.Marker({
        position: markerPosition,
        image: markerImage // 마커이미지 설정 
    });
    // 마커가 지도 위에 표시되도록 설정합니다
    marker.setMap(map);  
}

// 커스텀 오버레이에 표출될 내용으로 HTML 문자열이나 document element가 가능합니다
var areaList = [ '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도', '충청북도', '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
var fishingType = ['내수면 어업 중심', '연근해 어업 및 양식', '내수면 어업 중심', '연근해 어업 및 양식', '내수면 어업 중심', '내수면 어업 중심', '연근해 어업 및 양식', '내수면 어업 중심', '내수면 및 연안 어업', '연근해 어업 및 양식', '내수면 어업 중심', '연근해 어업 및 양식', '연근해 어업 및 양식', '연근해 어업 및 양식', '연근해 어업 및 양식', '연근해 어업 및 양식', '연근해 어업 및 양식']
var fishType = ['붕어, 잉어, 메기', '고등어, 멸치, 오징어', '붕어, 잉어, 메기', '꽃게, 조기, 전어', '붕어, 잉어, 메기', '붕어, 잉어, 메기', '고등어, 오징어, 전갱이', '붕어, 잉어, 메기', '붕어, 잉어, 메기, 꽃게', '명태, 오징어, 대구', '붕어, 잉어, 메기', '꽃게, 조기, 전어', '전어, 농어, 조기', '감성돔, 벵에돔, 전갱이', '대구, 오징어, 명태', '고등어, 멸치, 참다랑어', '벵에돔, 참돔, 갈치']
var aquacultureType = ['메기, 쏘가리', '넙치, 조피볼락', '메기, 쏘가리', '넙치, 조피볼락', '메기', '메기', '넙치, 조피볼락', '메기', '메기, 쏘가리', '대구', '메기', '넙치, 조피볼락', '넙치, 조피볼락', '넙치, 조피볼락, 전복, 김', '대구, 전복', '조피볼락, 벤자리, 전복, 김', '넙치, 조피볼락, 전복']

for (i = 0; i < areaList.length; i++ ){

    var content = 
    '<div class="customoverlay" onclick="openModal(\'' + 
    areaList[i] + '\', \'' + fishingType[i] + '\', \'' + fishType[i] + '\', \'' + aquacultureType[i] + 
    '\')">' +
    '   <div>' +
    '       <span class="title">'+
                areaList[i]
    '       </span>' +
    '   </div>' +
    '</div>';

    // 커스텀 오버레이가 표시될 위치입니다 
    latitude =[37.45, 35.06, 35.75, 37.34, 35.04, 36.23, 35.42, 36.38, 37.29, 37.70, 36.52, 36.54, 35.70, 34.70, 36.46, 35.34, 33.38]
    longitude = [126.9780, 129.0756, 128.6014, 126.7052, 126.8526, 127.3845, 129.3114, 127.2495, 127.5183, 128.1555, 127.4917, 126.6728, 127.1088, 126.4630, 128.5056, 128.2132, 126.5312]
    var position = new kakao.maps.LatLng(latitude[i], longitude[i]);  
    
    // 커스텀 오버레이를 생성합니다
    var customOverlay = new kakao.maps.CustomOverlay({
        map: map,
        position: position,
        content: content,
        yAnchor: 1 
    });

}
function openModal(areaName,fishingType,fishType,aquacultureType) {
    document.getElementById('modalTitle').textContent = areaName;
    document.getElementById('fishingType').textContent = fishingType;
    document.getElementById('fishType').textContent = fishType;
    document.getElementById('aquacultureType').textContent = aquacultureType;
    document.getElementById('modal').style.display = 'block';
    document.getElementById('modalBackdrop').style.display = 'block';
}

function closeModal() {
    document.getElementById('modal').style.display = 'none';
    document.getElementById('modalBackdrop').style.display = 'none';
}

