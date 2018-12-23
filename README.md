# LoRaHATの使い方
LoRaHATはLoRaモジュールを搭載した、Raspberry Pi ZeroのHATです。これをRaspberry Pi Zeroの上に取り付けることで、Raspberry Pi同士でLoRa通信をすることができます。
※ Raspberry Pi zero または Raspberry Pi 3とLoRaHATがなければ動作しません


## プログラムについて
プログラムは
- lora_com_child
- lora_com_parent

の2つがあります。どちらも言語はPythonです。
今回のプログラムでは、子機側に人感センサを取り付け、感知したかを親機に送ります。

### lora_com_parent
親機用のプログラム。子機からのデータを受け取り、出力します。

### lora_com_child
子機用のプログラム。子機に取り付けている人感センサが感知したかを出力し、親機の方に送ります。

### 親機と子機のモード転換
`sendCommand(ser, 1.00, "SKSREG S02 0")`
の末尾を`0`にすれば子機、`1`にすれば親機になります
