#! /usr/bin/env bash
scriptFilePath=../../src/donation-analytics.py 
clear

par1_list=('_1' '_2' '_3')
par2_list=('' '-s')
par3_list=('' '-v')

for par1 in "${par1_list[@]}"
do
    if [[ $par1 == '_1' ]]
    then
        echo '-----------------------------------------------------------------------------------------'
        echo 'INSIGHT''S DEMO TEST:'
        
    elif [ $par1 == '_2' ]
    then
        echo '-----------------------------------------------------------------------------------------'
        echo 'INPUT VALIDATION TESTS:'

    elif [ $par1 == '_3' ]
    then
        echo '-----------------------------------------------------------------------------------------'
        echo 'ALGORITHM CORRECTNESS TESTS:'
    fi

    for par2 in "${par2_list[@]}"
    do
        for par3 in "${par3_list[@]}"
        do
            recFilePath=./test$par1/input/itcont.txt 
            pctlFilePath=./test$par1/input/percentile.txt 
            outFilePath=./test$par1/output/repeat_donors$par2$par3.txt 
            logFilePath=./test$par1/output/log$par2$par3.txt
            stdOutPath=./test$par1/output/stdOut$par2$par3.txt   
            dash_s=$par2
            dash_v=$par3
            
            $scriptFilePath $dash_v $dash_s $recFilePath $pctlFilePath $outFilePath $logFilePath &>$stdOutPath
              
            diff $outFilePath ${outFilePath}_CORRECT | tee  ${outFilePath}_TESTRESULT

                if [ -e ${outFilePath}_CORRECT ]
                then
                    if [ -s ${outFilePath}_TESTRESULT ]
                    then
                        echo -n 'FAIL: '
                    else
                        echo -n 'PASS: '
                    fi 
                    echo ${outFilePath}
                fi 

            if [[ $par1 == '_2' ]]
            then
                
                if [[ $par3 == '-v' ]]
                then

                    tail -n+10 $logFilePath | head -31 > ${logFilePath}_sub
                    tail -n+10 ${logFilePath}_CORRECT | head -31 > ${logFilePath}_sub_CORRECT
                    
                    diff ${logFilePath}_sub ${logFilePath}_sub_CORRECT | tee  ${logFilePath}_sub_TESTRESULT

                    if [ -e ${logFilePath}_sub_CORRECT ]
                    then
                        if [ -s ${logFilePath}_sub_TESTRESULT ]
                        then
                           echo -n 'FAIL: '
                        else
                           echo -n 'PASS: '
                        fi
                        echo ${logFilePath} 
                    fi  

                fi
            fi
        done
    done
done

echo '-----------------------------------------------------------------------------------------'
echo "Performance and Scale-up Test"

par1=_2016
inputSize=("_1" "_10" "_100" "_1k" "_10k" "_100k" "_1M" "_10M" "_all20M")

dash_v=''
dash_s=''

for par2 in "${inputSize[@]}"
do
recFilePath=./test$par1/input/itcont$par2.txt 
pctlFilePath=./test$par1/input/percentile.txt 
outFilePath=./test$par1/output/repeat_donors$par2.txt 
logFilePath=./test$par1/output/log$par2.txt

$scriptFilePath $dash_v $dash_s $recFilePath $pctlFilePath $outFilePath $logFilePath
done


