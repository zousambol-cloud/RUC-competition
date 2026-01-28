@echo off
chcp 65001
echo 运行 MAD 多智能体辩论系统...

:: 设置参数
set INPUT_FILE=input.txt
set OUTPUT_DIR=output
set LANG_PAIR=zh-zh
set API_KEY=sk-348b5942180f419ea1ba5dc04fecd32d

:: 运行命令
python .\code\debate4tran.py -i .\%INPUT_FILE% -o .\%OUTPUT_DIR% -lp %LANG_PAIR% -k %API_KEY%

echo 运行完成！
pause