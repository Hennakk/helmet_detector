# helmet_detector

- 모델 훈련 과정





- Trouble  
   - Various Dataset  
   단순하고 낮은 화질의 데이터를 이용한 훈련으로 train accuracy가 1이 되는 과적합 발생
    

   - Classification의 단일객체
   단일객체에 대해 image가 주어졌을 때 어떤 class인지 구별하는 알고리즘  
   즉, 이미지의 feature를 스스로 추출하고 학습하는 알고리즘  
      -> 2개 이상의 객체를 탐지하고 분류하기에 한계
      
      sol) 각 이미지에 label을 부여하고 bounding box를 이용하여 이미지의 특징을 더 잘 추출할 수 있는 알고리즘 사용 [Object Detction](https://github.com/Hennakk/helmet_detection)
