weight=4
def run():
    #Inicijalizovanje svih pokretnih delova na robotu	
    nazgold(0)
    napgold(0)
    lfliper(0)
    rfliper(0)
    rrucica(0)
    lrucica(0)
    
    r.speed(120)
    r.forward(100)

    #Mora da zaobidje prvi pak ispred pocetne pozicije

    r.turn(-60)
    r.forward(230)
    r.turn(60)
    r.forward(250)

    r.goto(0,150)

    #Pozicija odakle treba da kupi pakove iz kruga
    r.turn(145)

    @_spawn
    def _():
        rfliper(2)
    lfliper(2)
    r.forward(520)
    r.goto(-1200,-500)
