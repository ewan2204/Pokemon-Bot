import io
import aiohttp
import discord
import random
import os
import pandas as pd
import asyncio
from discord import app_commands
from Utility import fixName, getPokedexURL, NUMBER_OF_POKEMON, getPokemonsName, getPokemonsGeneration

#Image handling stuff
from PIL import Image
import requests

data = pd.read_csv('https://gist.githubusercontent.com/santiagoolivar2017/0591a53c4dd34ecd8488660c7372b0e3/raw/4be104b8bc8876acd15f8e21f1c5945f10e3aa1e/Pokemon-description-image.csv')

spritesURL = 'https://play.pokemonshowdown.com/sprites/gen6/'
possibleURL = 'https://www.serebii.net/pokemon/art/' # + 006-mx.png


TOKEN = os.getenv('BOT_TOK')



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)





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

        if user_message.lower == "$pokemongens":
            smallIndex1 = random.randrange(0, NUMBER_OF_POKEMON)
            bigIndex2 = random.randrange(smallIndex1, NUMBER_OF_POKEMON)

            smallName = fixName(getPokemonsName(smallIndex1)).lower()
            bigName = fixName(getPokemonsName(bigIndex2)).lower()


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
            randomIndex = random.randrange(0, NUMBER_OF_POKEMON)

           

            randomPokedexURL = getPokedexURL(randomIndex)

            fullURL = possibleURL+ randomPokedexURL +  ".png"
            beegEnbed = discord.Embed(title = "Guess that Pokemon!", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3")
            print(fullURL)
            beegEnbed.set_image(url = fullURL)
            await message.channel.send('Guess that Pokemon!', embeds = [beegEnbed])
            randomPokemonName = getPokemonsName(randomIndex).lower()
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
    randomIndex = random.randrange(0, NUMBER_OF_POKEMON)
       
    randomPokedexURL = getPokedexURL(randomIndex)
    fullURL = possibleURL+ randomPokedexURL +  ".png"
    beegEnbed = discord.Embed(title = "Guess that Pokemon!", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3", colour = discord.Color.random(seed=randomIndex))
    print(fullURL)
    beegEnbed.set_image(url = fullURL)
    await interaction.response.send_message('Guess that Pokemon!', embeds = [beegEnbed])
    #await interaction.response.send_message(f'Hi, {interaction.user.mention}')

    randomPokemonName = getPokemonsName(randomIndex).lower()
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
    timeout='Time to answer',
    gen='The generation or generations you want to play with',
)
async def pokemonguessname(interaction: discord.Interaction, timeout: int = 10, gen: int = 12345678):
    """The fun discord bot functionality"""
    # Select a set of random pokemon to have as options
    pokemonGenerated = random.sample(range(0, NUMBER_OF_POKEMON), 5)
    randomSelection = random.randint(0,4)
    randomPokemon = pokemonGenerated[randomSelection]
       
    randomPokedexURL = getPokedexURL(randomPokemon)
    fullURL = possibleURL+ randomPokedexURL +  ".png"
    embed = discord.Embed(title = "Guess that Pokemon!", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3", colour = discord.Color.random(seed=randomPokemon))
    print(fullURL)
    embed.set_image(url = fullURL)
    


    print(randomPokemon)

	# wrong button pressed red everything
    async def wrongButtonCallback(interaction):
        for child in view.children:
            if child.custom_id == "Correct":
                child.style = discord.ButtonStyle.green
            else:
                child.style = discord.ButtonStyle.danger
            child.disabled = True
        await interaction.response.edit_message(view = view)

	# wrong button pressed
    async def rightButtonCallback(interaction):
        for child in view.children:
            if child.custom_id == "Correct":
                child.style = discord.ButtonStyle.green
            else:
                child.style = discord.ButtonStyle.danger
            child.disabled = True
        await interaction.response.edit_message(view = view)









    view = discord.ui.View()
    for i in range(0, 4):
        button = discord.ui.Button(label = getPokemonsName(pokemonGenerated[i]).lower(), style = discord.ButtonStyle.green, emoji = "👈")
        if i == randomSelection:
            button.custom_id = "Correct"
            button.callback = rightButtonCallback
        else:
            button.callback = wrongButtonCallback
        view.add_item(button)
    
    await interaction.response.send_message('Guess that Pokemon!', embeds = [embed], view = view)




@client.tree.command()
@app_commands.describe(
    timeout='Time to answer'
)
async def pokemongen(interaction: discord.Interaction, timeout: int = 10):
    """Given two pokemon can you determine which came first?"""
    smallIndex1 = random.randrange(0, NUMBER_OF_POKEMON)
    bigIndex2 = random.randrange(0, NUMBER_OF_POKEMON)


    left, right = random.sample(range(0, NUMBER_OF_POKEMON), 2)
    leftURL = possibleURL + getPokedexURL(left) +  ".png"
    rightURL = possibleURL + getPokedexURL(right) +  ".png"
    
    leftFile = None
    rightFile = None
    
    
    
    async with aiohttp.ClientSession() as session: # creates session
        async with session.get(leftURL) as resp: # gets image from url
            img = await resp.read() # reads image from response
            with io.BytesIO(img) as file: # converts to file-like object
                leftFile = discord.File(file, "testimage.png")
        async with session.get(rightURL) as resp: # gets image from url
            img = await resp.read() # reads image from response
            with io.BytesIO(img) as file: # converts to file-like object
                rightFile = discord.File(file, "testimage.png")
    
    #leftImage = discord.File(leftImageByteArray)
    #rightImage = discord.File(rightImageByteArray)
    
    async def wrongButtonCallback(interaction):
        for child in view.children:
            print("Left is " + str(left))
            if child.custom_id == "Left":
                child.label = getPokemonsName(left) + " gen: " + str(getPokemonsGeneration(left))
            elif child.custom_id == "Right":
                child.label = getPokemonsName(right) + " gen: " + str(getPokemonsGeneration(right))
            elif child.custom_id == "Middle":
                child.label = "Streak: 5"
            child.style = discord.ButtonStyle.danger
            child.disabled = True
        await interaction.response.edit_message(view = view)
        
    async def rightButtonCallback(interaction):
        for child in view.children:
            print("Left is " + str(left))
            if child.custom_id == "Left":
                child.disabled = True
                child.label = getPokemonsName(left) + " gen: " + str(getPokemonsGeneration(left))
            elif child.custom_id == "Right":
                child.disabled = True
                child.label = getPokemonsName(right) + " gen: " + str(getPokemonsGeneration(right))
            elif child.custom_id == "Middle":
                child.label = "Play More?"
                child.emoji = "🍣"
            child.style = discord.ButtonStyle.success
        await interaction.response.edit_message(view = view)
    
    leftButton = discord.ui.Button(label = "Left is first", style = discord.ButtonStyle.green, emoji = "👈", custom_id = "Left")
    middleButton = discord.ui.Button(label = "Same Generation", style = discord.ButtonStyle.green, emoji = "🐛", custom_id= "Middle")
    rightButton = discord.ui.Button(label = "Right is first", style = discord.ButtonStyle.green, emoji = "👉", custom_id = "Right")

    if getPokemonsGeneration(left) < getPokemonsGeneration(right):
        leftButton.callback = rightButtonCallback
        middleButton.callback = wrongButtonCallback
        rightButton.callback = wrongButtonCallback
    elif getPokemonsGeneration(left) > getPokemonsGeneration(right):
        leftButton.callback = wrongButtonCallback
        middleButton.callback = wrongButtonCallback
        rightButton.callback = rightButtonCallback
    else:
        leftButton.callback = wrongButtonCallback
        middleButton.callback = wrongButtonCallback
        rightButton.callback = rightButtonCallback
        


    view = discord.ui.View()
    view.add_item(leftButton)
    view.add_item(middleButton)
    view.add_item(rightButton)

    # Make embed
    leftEnbed = discord.Embed(title = "Which pokemon came first Left or Right? (in terms of generation added)", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3", colour = discord.Color.fuchsia())
    rightEnbed = discord.Embed(title = "Which pokemon came first Left or Right? (in terms of generation added)", url = "https://www.amazon.co.uk/gp/video/detail/B013GV3C2C/ref=atv_dp_season_select_s3", colour = discord.Color.fuchsia())
    # Paste in images.
    #leftEnbed.set_image(url = leftURL)
    #rightEnbed.set_image(url = rightURL)

    # Combine into embeds
    embeds = [leftEnbed,rightEnbed] 
    # smallName = fixName(otherData.iloc[smallIndex1]['name'].lower())
    # bigName = fixName(otherData.iloc[bigIndex2]['name'].lower())

    print(leftURL)
    print(rightURL)

    await interaction.response.send_message(files = [leftFile, rightFile], embeds = embeds, view=view)
    def is_correct(m):
        return m.author == interaction.user

client.run(TOKEN)
