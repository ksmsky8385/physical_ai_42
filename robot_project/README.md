### 가상환경 설정법

``` bash
cd robot_project

# 가상환경 생성
python3 -m venv --system-site-packages .venv
# 가상환경 활성화
source .venv/bin/activate
# 필수 라이브러리 설치
pip install numpy==1.21.5
# 설치된 패키지 목록 저장
pip freeze > requirements.txt
# 패키지 목록 기반 의존성 설치
pip install -r requirements.txt
# [7] VSCode 설치 및 실행
code .
```