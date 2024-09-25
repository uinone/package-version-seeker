# pakage-version-seeker

옛날 버전의 패키지를 설치할때, requirement.txt를 보면 버전이 명시되지 않은 경우가 있습니다.

패키지가 만들어진 당시에는 명시하지 않아도 잘 동작했겠지만, 지금은 아닙니다.

1. 매번 패키지가 만들어진 날짜를 찾고
2. 찾은 날짜랑 가장 비슷한 날짜에 만들어진 버전을 다시 찾아서
3. requirement.txt를 수정하던 저는 귀찮아졌습니다.

그래서 준비했습니다.

## How to use

총 3가지가 필요합니다.
- 문제가 되는 requirement.txt의 경로
- 문제가 되는 패키지의 이름 (ex. mmdet3d)
- 문제가 되는 패키지의 버전 (ex. 0.17.1)

예시로 드는 텍스트 파일은 아래와 같이 작성되어있습니다.
```python
lyft_dataset_sdk
networkx>=2.2,<2.3
# we may unlock the verion of numba in the future
numba==0.48.0
numpy<1.20.0
nuscenes-devkit
plyfile
scikit-image
# by default we also use tensorboard to log results
tensorboard
trimesh>=2.35.39,<2.35.40
```

보시다시피, 몇가지 패키지는 버전 명시가 되어있지 않습니다.

다음과 같이 version-finder를 설치해주세요
```python
pip install pakage-version-seeker
```

이후 다음과 같이 실행합니다.

```python
pvs mmdet3d 0.17.1 ./mmdetection3d/requirements/runtime.txt
```

실행 결과는 다음과 같습니다.

```python
[OUTPUT]
===========================
lyft_dataset_sdk==0.0.8
networkx>=2.2,<2.3
numba==0.48.0
numpy<1.20.0
nuscenes-devkit==1.1.9
plyfile==0.7.4
scikit-image==0.18.3
tensorboard==2.6.0
trimesh>=2.35.39,<2.35.40
===========================
```

특정 파일로 결과를 작성하고싶은 경우, 다음과 같이 '--export-path'를 명시해주세요.

```python
pvs mmdet3d 0.17.1 ./mmdetection3d/requirements/runtime.txt --export-path ./new_requirement.txt
```