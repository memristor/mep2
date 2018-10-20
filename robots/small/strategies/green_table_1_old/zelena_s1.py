#load_cfg(r)
##
weight=1
def run():
    r.setpos(58,48)
    r.speed(80)###PROMJENIO SA 100 
    r.t(0)
    ##

    sleep(5)
    #######################
    # TASK
    #######################

    '''
    cev(1)
    cev2(1)
    r.forward(-450)
    r.t(100)
    sleep(2)
    cev(0)
    sleep(2)
    r.t(0)
    '''
    #exit(0)
    klapna(1)
    cev(0)
    r.t(85) ###########otkom
    r.goto(720,48)

    for i in range(10):
        r.forward(25)
        sleep(0.01)
        r.forward(-25)###bio -25
        sleep(0.01) 
    sleep(0.5)
    r.forward(-200)
    r.t(0)
    r.goto(1050, 430)
    r.goto(1200,430)
    sleep(0.05)
    r.goto(1600,95)
    r.goto(1760,95)
    r.turn(90)
    pcelica(2)
    r.goto(1760,50,-1)
    pcelica(1)
    r.goto(1760,110)
    pcelica(0)
    ###############
    ## PREKIDa
    ###############

    r.speed(130)
    r.goto(800,1060,-1)#######ZA PRVI STO 1030
    r.goto(100,1060, -1)
    r.speed(40)
    r.conf_set('enable_stuck',0)
    r.goto(-50,1060, -1)
    r.setpos(0,1060)
    r.speed(80)
    r.conf_set('enable_stuck',1)
    r.goto(100,1060)
    sleep(0.05)
    prekidac(1)
    sleep(0.1)
    r.goto(24, 1060, -1)
    sleep(0.5)
    r.goto(100, 1060)
    prekidac(0)
    sleep(0.3)
    r.speed(150)

    ###################
    ## SORTIRANJE
    #################
    cev(1)
    r.goto(1396, 2278, -1)
    sleep(0.05)
    r.goto(1700, 2493, -1)
    sleep(0.05)
    r.goto(1740,2474)
    sleep(0.05)
    klapna(2)

    #####POZICIONIRANJE ZA SORTIRANJE####
    #povecavam u za 4mm za drugi sto 2291
    r.goto(1740, 2295)
    sleep(0.5)
    r.conf_set('enable_stuck',0)
    cev2(1)
    '''
    for i in range(1):
        r.forward(20)
        sleep(0.05)
        r.forward(-20)
        sleep(0.05)

    for i in range(4):
        klapna(2)
        r.goto(1740,2250)
        sleep(0.05)
        klapna(1)
        r.goto(1740,2205)
        for i in range(1):
            r.forward(20)
            sleep(0.05)
            r.forward(-20)
            sleep(0.05)
        sleep(0.05)
        r.goto(1740,2250,-1)
        sleep(0.05)
        klapna(2)
        r.goto(1740,2295,-1) 
        for i in range(1):
            r.forward(20)
            sleep(0.05)
            r.forward(-20)
            sleep(0.05)
        sleep(0.05)

    klapna(1)
    r.conf_set('enable_stuck',1)
    cev(1)
    '''
    r.forward(-70)
    r.goto(1439,2038)

    #############################
    ##  ISPUSTANJE PROTIVNICKIH
    #############################

    r.goto(1400, 1500)

'''
exit(0)
r.conf_set('enable_stuck',0)
r.goto(1650, 1500)
sleep(0.5)
klapna(2)
cev2(0)
sleep(3)
r.conf_set('enable_stuck',1)
r.forward(-100)

#############################
## ISPALJIVANJE SORTIRANIH ##
#############################
r.goto(700,84, -1)
r.goto(640,84, -1)
#r.turn(190)
sleep(2)
r.t(80)
sleep(3)
cev(0)
klapna(1)
sleep(2)
r.t(0)
###############################
#####ISPUSTANJE SORTIRANIH#####
###############################
klapna(2)

##########################


'''
