from TestingFramework import main
arg1 = "-d bafu5k -scen ts_len -a shift -alg screen"
main(arg1)
arg1 = "-d humidity -scen ts_len -a shift -alg rpca,CDREP"
main(arg1)
arg1 = "-d humidity -scen ts_len -a shift -alg all"
main(arg1)
