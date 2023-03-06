# helmet_detector

![image](https://user-images.githubusercontent.com/98154707/223004364-9a55b27a-2a04-4528-b1ff-852d618344c2.png)


- Trouble
   - Various Dataset
   
     단순하고 낮은 화질의 데이터를 이용한 훈련으로 train accuracy가 1이 되는 과적합 발생
    

   - CNN(Convolution Nural Network)
   
      기존의 알고리즘은 이미지의 feature를 스스로 추출하고 학습하는 알고리즘
      
      -> 2개 이상의 객체를 탐지하고 분류하기에 한계
      
      각 이미지에 label을 부여하고 bounding box를 이용하여 이미지의 특징을 더 잘 추출할 수 있는 알고리즘 사용    
      [Object Detction](https://github.com/Hennakk/helmet_detection)
