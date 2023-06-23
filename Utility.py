import pandas as pd
otherData = pd.read_csv('https://raw.githubusercontent.com/frank2204/fantastic-lamp/main/data/pokedex_(Update_05.20).csv')
print(otherData.keys)
print(otherData.columns.values)
NUMBER_OF_POKEMON = len(otherData)



def getPokedexURL(index):
    basePokedex  = str(otherData.iloc[index]['pokedex_number'])
    name = otherData.iloc[index]['name']

    if(len(basePokedex) == 1):
        basePokedex = str(0) + basePokedex
    if(len(basePokedex) == 2):
        basePokedex = str(0) + basePokedex


    if('mega' in name.lower() and "Yanmega" != name):
        basePokedex = basePokedex + "-m"
        if(name[-2] == " "):
            basePokedex = basePokedex + name[-1]
    
    if('Alolan' in name or 'Galarian' in name):
        basePokedex = basePokedex + "-a"

    if('partner' in name and not 'eevee' in name):
        pikachuList = ["-p", "-a", "-k", "-u", "-s", "-o"]
        basePokedex = basePokedex + random.choice(pikachuList)

    if(' Rotom' in name):
        if('n' == name[2]):
            basePokedex = basePokedex + "-s"
        else:
            basePokedex = basePokedex + "-" + name[0]

    return basePokedex







def fixName(randomPokemonName):
    if('mega' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[1]
        return pokemonName + "-mega"
    
    if('shaymin' == randomPokemonName):
        return 'shaymin'

    if('shaymin' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[0]
        form = pokemonName.split('shaymin')[0]
        return "shaymin-" + form

    if('rotom' == randomPokemonName):
        return randomPokemonName

    if('rotom' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[0]
        form = pokemonName.split('rotom')[0]
        return 'rotom-' + form    


    if('aegislash' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[0]
        form = pokemonName.split('aegislash')[0]
        return 'aegislash-' + form    

    if('pumpkaboo' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[0]
        form = pokemonName.split('pumpkaboo')[0]
        return 'pumpkaboo-' + form    

    if('therian' in randomPokemonName or 'incarnate' in randomPokemonName):
        a = randomPokemonName.rindex('s')
        randomPokemonName = randomPokemonName[:a+1] + '-' + randomPokemonName[1+a:len(randomPokemonName)-6]

    if('ho-oh' == randomPokemonName):
        return 'hooh'

    if('zygarde' in randomPokemonName):
        return 'Zygarde'

    if('mr. mime' in randomPokemonName):
        return 'mr-mime'    

    if('wormadam' in randomPokemonName):
        pokemonName = str(randomPokemonName).split(' ')[0]
        form = pokemonName.split('wormadam')[0]
        return 'wormadam-' + form    
    return randomPokemonName



def getPokemonsName(index: int) -> str:
    return otherData.iloc[index]['name']

def getPokemonsGeneration(index: int) -> int:
    return otherData.iloc[index]['generation']