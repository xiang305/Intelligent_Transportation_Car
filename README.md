# Iot_物流運輸概念車
## 1.關於專案
這是一個可以用在物流運輸方面的遙控車，使用者可操控車子移動並觀看實時畫面。同時，車子則可記錄兩點之間的路線。此功能可應用於動線多變、不定的場景下，讓使用者客製化自己的運輸路線
## 2.所需材料
- [雙層四驅自走車底盤](https://www.tenlong.com.tw/products/10241289256) * 1
- Rasberry Pi 4 * 1
- 麵包板 * 1
- L298N馬達驅動模組 * 1
- 1.5v電池 * 4
- 四顆並聯電池盒(包含正負極單芯線) * 1
- 穩定5V的行動電源(可用樹莓派UPS 鋰電池擴充板替代) * 1
- 數條公對公、公對母、母對母杜邦線
- 捆線帶(非必要，用於整理杜邦線)
- 雙面膠(非必要，用於固定車上裝置)
## 3.線路設計與實體照片
### 線路設計
![線路設計](image/l298n與馬達.jpg)
### 實體正面
![實體照片](image/實體正面.jpg)
### 實體背面
![實體照片](image/實體背面.jpg)
## 4.實作步驟
### 步驟一 (自走車組裝)
可參考[四軸自走車底盤組裝](https://www.youtube.com/watch?v=qmBYOK8da6Y&ab_channel=Yung-ChenChou)影片
### 步驟二 (測試硬體)
- 將攝影鏡頭安裝在樹梅派上，可參考[Raspberry Pi 相機模組安裝](https://blog.wuct.me/raspberry-pi-100abbe7a1fd)，並運用[camera_test.py](code/camera_test.py)檔案測試鏡頭是否能正常拍攝
- 運用[engine_test.py](code/engine_test.py)檔案測試L298N能否控制馬達 & 馬達能否正常轉動。若車子無法正常移動，可嘗試以下方法
  - 直接將電池組連接到各個馬達，測試馬達是否故障
  - 查看L298N的ENA與ENB腳位是否有jumper
  - 嘗試能否控制單邊的馬達轉動，測試L298N是否故障
  - 提供額外的電源，測試是否電壓不足，但需要注意[規格書](chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/http://www.pu-yang.com.tw/media/products/0731191001406789695.pdf)
### 步驟三 (執行程式)
執行[main.py](code/main.py)檔案，透過網頁操控車子
## 5.模型訓練
本專案預計使用YOLO模型，YOLO是一種流行的物體檢測深度學習模型，可以在圖像中識別和定位多個物體，並為每個物體提供邊界框和類別標籤。更詳細的介紹可參考[深度學習-物件偵測:You Only Look Once (YOLO)
](https://chih-sheng-huang821.medium.com/%E6%B7%B1%E5%BA%A6%E5%AD%B8%E7%BF%92-%E7%89%A9%E4%BB%B6%E5%81%B5%E6%B8%AC-you-only-look-once-yolo-4fb9cf49453c)
### 訓練資料格式
格式為txt檔，格式為 class x_center y_center width height，各欄位以空白分隔，意義如下：
- class：類別ID，辨別該物品是什麼。若想製作耽誤體檢測模型，全部設定為相同類別即可
- x_center：物體中心點在畫面上的 X 座標
- y_center：物體中心點在畫面上的 Y 座標
- width：標註方框的寬度
- height：標註方框的高度
### 自行訓練
1. 準備資料集圖片，並使用標註軟體來標註要檢測的物體範圍。這邊推薦使用labelImg，因為標註完後可直接輸出YOLO所需的txt格式，不需進行額外轉換，操作說明可參考[LabelImg 影像標註工具使用教學](https://blog.gtwang.org/useful-tools/labelimg-graphical-image-annotation-tool-tutorial/#google_vignette)
2. 可執行[splitData.py](code/splitData.py)檔案，自行設定訓練與測試集的比例並隨機分配，或自行手動分配
3. 建立訓練模型的yaml檔，並開始訓練。可參考[yolo 自己訓練模型](https://blog.davidou.org/archives/2376)
### Roboflow訓練
Roboflow 是一個可以將訓練資料集輸出成不同機器學習模型格式與進行模型訓練的網站，同時它可以對資料集進行標記、切分訓練測試比例、調整影像大小以及資料擴增，可參考[客製化 YOLOv5 模型 (四)：標註資料、導出資料集](https://ithelp.ithome.com.tw/articles/10305264)，訓練成果如下：

可透過此介面得知檢測範圍、信心程度、準確率等資訊
## 6.Demo影片
[物流運輸概念車 Demo展示](https://youtu.be/6LKaLzW9TY4)
## 7.修改方向
- 將訓練好的**物體追蹤模型部署**在樹莓派上，讓車子可追蹤特定人或物移動。如此一來，使用者便不需要再手動遙控紀錄路線
- 目前的路線記錄功能是透過記錄使用者的操作歷程來實現，容易出現不準確的狀況。可**添加imu傳感器**，紀錄車子的速度及方向，更加準確的還原路徑
- 可用支架把**鏡頭架高**，比較容易識別目標
- 添加**重量感測模組**，讓使用者可設定負重閥值，並讓車子在超出負荷時執行預設的行動
- 添加**麥克風模組**，讓使用者可透過簡單的語音指令，命令車子執行返回起點、前往目的地或停止等行動
## 8.參考資料
- [利用roboflow訓練模型](https://medium.com/@andy6804tw/%E5%BF%AB%E9%80%9F%E4%B8%8A%E6%89%8Byolo-%E5%88%A9%E7%94%A8-roboflow-%E5%92%8C-ultralytics-hub-%E5%AE%8C%E6%88%90%E6%A8%A1%E5%9E%8B%E8%A8%93%E7%B7%B4%E8%88%87%E7%AE%A1%E7%90%86-%E4%B8%8A-37acd110a8a0)
- [樹莓派腳位](https://pinout.xyz/)
- [L298n控制馬達](https://atceiling.blogspot.com/2021/04/raspberry-pi-pico10l298n.html#google_vignette)
