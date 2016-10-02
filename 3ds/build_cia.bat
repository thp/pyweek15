cxitool.exe -n 1WhaleTr -c CTR-N-WHAL -t 0004000000195400 -s settings.txt 3ds/onewhaletrip_3ds/onewhaletrip_3ds.3dsx onewhaletrip_3ds.cxi
makerom -f cia -o onewhaletrip_3ds.cia -target t -i onewhaletrip_3ds.cxi:0:0
pause