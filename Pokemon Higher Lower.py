import discord
import random
import os
import pandas as pd
import asyncio
from discord import app_commands


data = pd.read_csv('https://gist.githubusercontent.com/santiagoolivar2017/0591a53c4dd34ecd8488660c7372b0e3/raw/4be104b8bc8876acd15f8e21f1c5945f10e3aa1e/Pokemon-description-image.csv')
otherData = pd.read_csv('https://raw.githubusercontent.com/frank2204/fantastic-lamp/main/data/pokedex_(Update_05.20).csv')
spritesURL = 'https://play.pokemonshowdown.com/sprites/gen6/'
possibleURL = 'https://www.serebii.net/pokemon/art/' # + 006-mx.png

print(otherData.keys)

TOKEN = os.getenv('BOT_TOK')

print(otherData.columns.values)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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



class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)






    async def on_ready(self):
        print("Hello world")
        print("We have logged in as {0.user}".format(client))
        try:
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)







    async def on_message(self, message):
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        userID = message.author.id 


        # Stops bot feedback :D
        if userID == self.user.id:
            return

        if user_message.lower == "$pokemonGens":
            smallIndex1 = random.randrange(0,len(otherData))
            bigIndex2 = random.randrange(smallIndex1,len(otherData))

            smallName = fixName(otherData.iloc[smallIndex1]['Name'].lower())
            bigName = fixName(otherData.iloc[bigIndex2]['Name'].lower())


            beegEnbed = discord.Embed(title = "Is the pokemon on the right from a higher or lower Generation than the one on the left?", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
            beegEnbed.set_image(url = spritesURL + bigName + ".png")
            print(spritesURL + bigName + ".png")
            print(spritesURL + smallName + ".png")

            smolEnbed = discord.Embed(title = "Is the pokemon on the right from a higher or lower Generation than the one on the left?", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
            smolEnbed.set_image(url = spritesURL + smallName + ".png")
            embeds = []
            await message.channel.send('Guess that Pokemon!')
            if(random.random()>=0.5):
                print("smol beeg")
                embeds.append(smolEnbed)
                embeds.append(beegEnbed)
            else:
                print("beeg smol")
                embeds.append(beegEnbed)
                embeds.append(smolEnbed)
            await message.channel.send(embeds = embeds)






        elif user_message.lower() == "$pokemonguess":
            randomIndex = random.randrange(0,len(otherData))

           

            randomPokedexURL = getPokedexURL(randomIndex)

            fullURL = possibleURL+ randomPokedexURL +  ".png"
            beegEnbed = discord.Embed(title = "Guess that Pokemon!", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
            print(fullURL)
            beegEnbed.set_image(url = fullURL)
            await message.channel.send('Guess that Pokemon!', embeds = [beegEnbed])
            randomPokemonName = otherData.iloc[randomIndex]['name']
            print(randomPokemonName)
            #randomPokemonName = fixName(randomPokemonName)
            #await message.channel.send(spritesURL + otherData.iloc[randomIndex]['Name'].lower() + ".png")

            def is_correct(m):
                return m.author == message.author


            try:
                guess = await self.wait_for('message', check=is_correct, timeout=10.0)
            except asyncio.TimeoutError:
                return await message.channel.send(f'Sorry, you took too long it was {randomPokemonName}.')

            if guess.content.lower() == randomPokemonName.lower():
                await message.channel.send('You are right!')
            else:
                await message.channel.send(f'Oops. It is actually {randomPokemonName}.')


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@client.tree.command()
@app_commands.describe(
    timeout='Time to answer',
    gen='The generation or generations you want to play with',
)
async def pokemonguess(interaction: discord.Interaction, timeout: int = 10, gen: int = 12345678):
    """The fun discord bot functionality"""
    randomIndex = random.randrange(0,len(otherData))
       
    randomPokedexURL = getPokedexURL(randomIndex)
    fullURL = possibleURL+ randomPokedexURL +  ".png"
    beegEnbed = discord.Embed(title = "Guess that Pokemon!", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3", colour = discord.Color.random(seed=randomIndex))
    print(fullURL)
    beegEnbed.set_image(url = fullURL)
    await interaction.response.send_message('Guess that Pokemon!', embeds = [beegEnbed])
    #await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    randomPokemonName = otherData.iloc[randomIndex]['name']
    print(randomPokemonName)
    #randomPokemonName = fixName(randomPokemonName)
    #await message.channel.send(spritesURL + otherData.iloc[randomIndex]['Name'].lower() + ".png")
    def is_correct(m):
        return m.author == interaction.user
    try:
        guess = await client.wait_for('message', check=is_correct, timeout = timeout)
    except asyncio.TimeoutError:
        return await interaction.channel.send(f'Sorry, you took too long it was {randomPokemonName}.')
    if guess.content.lower() == randomPokemonName.lower():
        await interaction.channel.send('You are right!')
    else:
        await interaction.channel.send(f'Oops. It is actually {randomPokemonName}.')



@client.tree.command()
@app_commands.describe(
    timeout='Time to answer'
)
async def pokemongen(interaction: discord.Interaction, timeout: int = 10):
    """Given two pokemon can you determine which came first?"""
    smallIndex1 = random.randrange(0,len(otherData))
    bigIndex2 = random.randrange(0,len(otherData))


    left, right = random.sample(range(0,len(list(otherData))), 2)
    leftURL = possibleURL + getPokedexURL(left) +  ".png"
    rightURL = possibleURL + getPokedexURL(right) +  ".png"

    # Make embed
    leftEnbed = discord.Embed(title = "Which one came first Left or Right?Which one came first Left or Right?Which one came first Left or Right?Which one came first Left or Right?", url = "https://i.stack.imgur.com/Fzh0w.png", colour = discord.Color.fuchsia())
    rightEnbed = discord.Embed(title = "Which one came first Left or Right?Which one came first Left or Right?Which one came first Left or Right?Which one came first Left or Right?", url = "https://i.stack.imgur.com/Fzh0w.png", colour = discord.Color.fuchsia())
    leftEnbed.set_footer("\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000|")
    rightEnbed.set_footer("\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000\u3000|")
    # Paste in images.
    leftEnbed.set_image(url = leftURL)
    rightEnbed.set_image(url = rightURL)

    # Combine into embeds
    embeds = [leftEnbed,rightEnbed]
    
    ### smallName = fixName(otherData.iloc[smallIndex1]['name'].lower())
    ### bigName = fixName(otherData.iloc[bigIndex2]['name'].lower())


    ### beegEnbed = discord.Embed(title = "Is the pokemon on the right from a higher or lower Generation than the one on the left?", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
    ### beegEnbed.set_image(url = spritesURL + bigName + ".png")
    print(leftURL)
    print(rightURL)

    ### smolEnbed = discord.Embed(title = "Is the pokemon on the right from a higher or lower Generation than the one on the left?", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
    ### smolEnbed.set_image(url = spritesURL + smallName + ".png")
    ### embeds = []
    ### await interaction.channel.send('Guess that Pokemon!')
    await interaction.response.send_message(embeds = embeds)
    def is_correct(m):
        return m.author == interaction.user

client.run(TOKEN)
