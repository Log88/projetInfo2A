from Manager import DatabaseManager as dbm

interiorBg = dbm.create("interiorBg", True)
interiorBg.scrape(100, 'empty room')
interiorBg.scrape(50, 'corridor')
interiorBg.scrape(50, 'hallway')
interiorBg.label()

extincteur = dbm.load("extincteur")
extincteur.cleanAll()
extincteur.scrape(300, 'extinguisher')
extincteur.cutOut()
extincteur.checkFolder()
extincteur.putInContext(interiorBg)




