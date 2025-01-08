# Iot_物流運輸概念車
## 1.關於專案
這是一個可以用在物流運輸方面的遙控車，主要用途為使用者能觀看實時畫面操控車子移動，車子可記錄兩點之間的路線
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
## 3.線路設計
![線路設計](image/l298n與馬達.jpg)
![實體照片](image/實體照片.jpg)
## 4.程式設計

## 5.模型訓練

## 6.Demo影片
[物流運輸概念車 Demo展示](https://youtu.be/6LKaLzW9TY4)
## 7.修改方向
- 將訓練好的模型部署在樹莓派上，讓車子可以追蹤人移動
- 添加imu傳感器，增進路線紀錄的精準度
- 將車子的平台擴大，移出空間放置負重元，添加測種與重量閥值設定的功能
- 可用支架把鏡頭架高，比較容易識別目標
- 添加
## 8.參考資料
- [利用roboflow訓練模型](https://medium.com/@andy6804tw/%E5%BF%AB%E9%80%9F%E4%B8%8A%E6%89%8Byolo-%E5%88%A9%E7%94%A8-roboflow-%E5%92%8C-ultralytics-hub-%E5%AE%8C%E6%88%90%E6%A8%A1%E5%9E%8B%E8%A8%93%E7%B7%B4%E8%88%87%E7%AE%A1%E7%90%86-%E4%B8%8A-37acd110a8a0)
- [樹莓派腳位](https://pinout.xyz/)
- [L298n控制馬達](https://atceiling.blogspot.com/2021/04/raspberry-pi-pico10l298n.html#google_vignette)
