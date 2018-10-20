weight=1
def run():

    ###############################################################

    # 575 -54
    init_linear()
    lift(1)
    #r.goto(330, -150)
    sleep(0.1)
    #r.absrot(0)
    r.goto(530,-150)
    #r.absrot(0)
    r.goto(1500,-150)
    sleep(1)
    rotate(0)
    lift(0)
    pump(0,1)
    sleep(1.5)
    lift(1)
    sleep(1.5)
    rotate(2)
    pump(0,0)
    r.goto(800,-150, -1)
