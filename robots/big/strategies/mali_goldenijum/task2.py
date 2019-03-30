# oslobadaj goldenijum i nosi ga na vagu
weight =3
def run():
	
	r.goto(160,0)
	r.goto(0,780) # ovde spusti rucicu
	sleep(1)
	#rrucica(1)
	r.goto(-250,780) # gurne plavi da bi oslobodio goldenijum
	sleep(1)
	#rrucica(0)
		
	r.goto(-900,780) # malo dalje od goldenijumove lokacije da izgura pak neki ako je stajao tu 
	r.goto(-750,700,180) 
	r.goto(-750,800,-90) # goldenijumova lokacija
	sleep(1)
	#nazgold(1)
	#pump(2,1)

	r.goto(-750,700) # odmakne se zbog rotacije 
	r.goto(170,-300)
	r.goto(170,-390,90)
	sleep(1)	 
	 
	
