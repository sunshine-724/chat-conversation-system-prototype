#各モデルで対話した感想

1. gemma-swallow-q3:latest
そのままのコンテキストサイズで使用すると、VRAMがあふれて会話のテキスト生成が著しく遅くなった
2. okamototk/gemma-2-llama-swallow:27b 
同じくそのままのコンテキストサイズで使用すると、VRAMがあふれて会話のテキスト生成が著しく遅くなった
3. llama3:latest(8b)
GPU100%で動かすことができた。
ただし、誤字が少し見える