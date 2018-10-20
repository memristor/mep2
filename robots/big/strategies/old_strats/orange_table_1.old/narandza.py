weight=1
colors=['green','blue','orange','black']
middle='yellow'

combination=['green','orange','blue']
def check_side(side, combination):
    if colors[side-1] in combination and \
       colors[side] in combination and \
       colors[(side+1)%len(colors)] in combination:
           return True
    return False


def get_side(combination):
    for i in range(4):
        if check_side(i,combination):
            return i

# 2,4,3
#get_side(combination)
def get_pump_order(combination):
    rot=get_side(combination)
    print(rot)
    c=[colors[rot-1], colors[rot], colors[(rot+1)%4]]
    print(c)
    pumps=[2,4,3]
    return [pumps[c.index(i)] for i in combination]

def get(col,combination):
    global colors
    colors=col
    if 'yellow' in combination:
        h = list(filter(lambda x: x != 'yellow', combination))
        s=set(colors)-set(h)
        replacement=next(i for i in s)
        idx=combination.index('yellow')
        combination2 = list(combination)
        combination2[idx] = replacement
        rot=get_side(combination2)
        p=get_pump_order(combination2)
        p[idx] = 1
        return (rot, p)
    else:
        return (get_side(combination), get_pump_order(combination))
def get_remaining_pump(p):
    return next(i for i in (set(range(1,5))-set(p)))

lift_pos=0
def unload(n):
    global lift_pos
    if n == 1:
        r.forward(58)
        pump(1,0)
        if lift_pos == 0:
            lift(1)
        r.forward(-58)    
    elif n == 2:  
        if lift_pos == 0:
            lift(1)
            rotate(3)
            lift(0)
        rotate(3)
        pump(2,0)
    elif n == 3:
        if lift_pos == 0:
            lift(1)
            rotate(1)
            lift(0)
        rotate(1)
        pump(3,0)
    elif n == 4:
        if lift_pos == 0:
            lift(1)
            rotate(2)
            lift(0)
        rotate(2)
        pump(4,0)

def run():

    def build_cubes(color):
        for i in color:
            lift(color.index(i))
            unload(i)
            lift(3)
            unload(get_remaining_pump(color))
        
    r.setpos(80,350)

    r.speed(80)
    r.tol = 0

    init_linear()

    combination = ['black','yellow','blue']
    colors = ['green', 'blue', 'orange','black']
    s=get(colors, combination)

    start_rotation = s[0]
    lift(1)
    rotate(start_rotation)

    r.goto(200, 400)#390
    r.goto(880, 400)#390
    #time.sleep(1)
    lift(0)
    pump(0,1)
    sleep(1)
    lift(1)
    #r.forward(800)
    #r.forward(-700)
    r.goto(330,400,-1)#390
    r.goto(330, 100)

    build_cubes(s[1])

    r.goto(330 ,250,-1)
    ########################
    ##STUCK
    #########################
    r.conf_set('enable_stuck', 0)
    r.goto(50,250,-1)
    r.speed(20)
    r.goto(-10,250,-1)
    sleep(0.2)
    r.setpos(0,250)
    r.speed(100)

    ########################


    colors = ['black', 'green', 'blue', 'orange']
    s=get(colors, combination)

    start_rotation = s[0]
    lift(1)
    rotate(start_rotation)
      
    sleep(0.1)
    r.goto(150,250)
    r.goto(150,800)
    r.speed(50)
    r.goto(150,1100)
    lift(0)
    pump(0,1)
    sleep(0.5)
    lift(1)
    r.speed(100)
    r.goto(150,800,-1)
    r.goto(550,300)
    r.goto(550,100)

    build_cubes(s[1])
    r.goto(550,300,-1)

    #####################3
    ##  COLLECTING THIRD
    ####################

    colors = ['green', 'blue', 'orange','black']
    s=get(colors, combination)

    start_rotation = s[0]
    lift(1)
    rotate(start_rotation)

    r.goto(550,1355,-1)
    r.goto(1000,1355)
    lift(0)
    pump(0,1)
    sleep(0.2)
    lift(1)
    r.goto(750,1355,-1)
    r.goto(750,100)

    build_cubes(s[1])

    r.goto(750,300,-1)
    lift(0)
