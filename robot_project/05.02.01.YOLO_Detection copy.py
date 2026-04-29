import cv2
from ultralytics import YOLO

# 1. 모델 로드 (n: nano 버전으로 매우 빠르고 가볍습니다)
# 처음 실행 시 모델 파일(yolov8n.pt)이 자동으로 다운로드됩니다.
model = YOLO('yolov8n.pt') 

# 2. 웹캠 연결 (0번 카메라)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    if not ret:
        break

    # 3. 객체 탐지 수행 (stream=True는 실시간 처리에 최적화된 모드입니다)
    results = model(frame, stream=True)

    # 4. 결과 시각화
    for r in results:
        # 감지된 객체의 바운딩 박스, 라벨, 신뢰도를 프레임 위에 그립니다.
        annotated_frame = r.plot()

    # 결과 화면 출력
    cv2.imshow("YOLOv8 Real-Time Detection", annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()