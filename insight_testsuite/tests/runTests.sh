#par1=_2016 
#par2=_first10000 
par1=_1
par2=
clear
python ../../src/donation-analytics.py ./test$par1/input/itcont$par2.txt ./test$par1/input/percentile.txt ./test$par1/output/repeat_donors$par2.txt ./test$par1/output/log$par2.txt
