# What will be the value of City.all_cities after we run the
# code below?

class Alien:
    count = 0
    places = []

    def __init__(self, planet, species):
        self.planet = planet
        self.species = species


mart = Alien("Mars", "martian")
mart.places.append("Mars")
mart.count += 1

dalek = Alien("Scaro", "dalek")
dalek.places.append("Scaro")
dalek.count += 1
Alien.count += 2
print(dalek.count)
