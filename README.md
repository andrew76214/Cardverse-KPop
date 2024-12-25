# Cardverse-KPop




---
## 自動檢測程式碼中的 import 並安裝
### 使用 pipreqs 工具：

pipreqs 可以掃描程式碼，檢測使用到的依賴包並生成 requirements.txt。
安裝 pipreqs：
```bash
pip install pipreqs
```
在程式碼所在目錄生成依賴列表：
```bash
pipreqs /path/to/your/code
```
生成的 requirements.txt 文件會包含程式碼中所有需要的依賴包。
安裝這些依賴：
```bash
pip install -r requirements.txt
```

### 使用 autopip 工具（快速安裝缺少的依賴）：

autopip 會根據程式碼中的 import 嘗試自動安裝缺少的依賴。
安裝 autopip：
```bash
pip install autopip
```
使用 autopip 執行程式碼：
```bash
autopip python your_script.py
```