# helmet_detector

- Model layer

![image (1)](https://user-images.githubusercontent.com/98154707/223673202-68fe4a88-e044-40a4-8afc-15c09400fdc6.png)



- Train result

![image](https://user-images.githubusercontent.com/98154707/223674115-74f7c179-b868-4682-8bbe-3ea6c9258d11.png)  

<img src="https://user-images.githubusercontent.com/98154707/223673620-5f43fa26-7439-4b39-a471-452f492551f7.png" width="600" height="400"/>

## Trouble  
1. Overfitting

![image (2)](https://user-images.githubusercontent.com/98154707/223673432-a611f516-d5d0-4873-96f4-6c158bc2ef36.png)
  
  Various Dataset  
  단순하고 낮은 화질의 데이터를 이용한 훈련으로 train accuracy가 1이 되는 과적합 발생
   
   
2. 다수 객체 검출 불가
<img src="https://user-images.githubusercontent.com/98154707/223673858-0d087431-2de1-4a48-9600-bfe9729608d0.png" width="600" height="400"/>

   Classification의 단일객체
   단일객체에 대해 image가 주어졌을 때 어떤 class인지 구별하는 알고리즘  
   즉, 이미지의 feature를 스스로 추출하고 학습하는 알고리즘  
      -> 2개 이상의 객체를 탐지하고 분류하기에 한계
      
sol) 각 이미지에 label을 부여하고 bounding box를 이용하여 이미지의 특징을 더 잘 추출할 수 있는 알고리즘 사용 [Object Detction](https://github.com/Hennakk/helmet_detection)
