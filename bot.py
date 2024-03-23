import discord
import asyncio
from constants import TIMEOUT_SECONDS
from game import Game

# Initialize Discord client
client = discord.Client()
game = Game()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!start'):
        await message.channel.send('Truth or Dare game started! Use !join to join the game.')

    elif message.content.startswith('!join'):
        if message.author not in game.players:
            game.add_player(message.author)
            await message.channel.send(f'{message.author.mention} joined the game!')
        else:
            await message.channel.send(f'{message.author.mention} is already in the game!')

    elif message.content.startswith('!truth'):
        if message.author in game.players:
            await message.channel.send(f'{game.get_current_player().mention}, your truth prompt is: {game.get_truth_prompt()}')
            await wait_for_response(message)
        else:
            await message.channel.send(f'{message.author.mention}, you are not in the game!')

    elif message.content.startswith('!dare'):
        if message.author in game.players:
            await message.channel.send(f'{game.get_current_player().mention}, your dare prompt is: {game.get_dare_prompt()}')
            await wait_for_response(message)
        else:
            await message.channel.send(f'{message.author.mention}, you are not in the game!')

    elif message.content.startswith('!players'):
        if game.players:
            player_list = "\n".join([f"{player.display_name}" for player in game.players])
            await message.channel.send(f'Players in the game:\n{player_list}')
        else:
            await message.channel.send('No players in the game.')

async def wait_for_response(message):
    try:
        response_message = await client.wait_for('message', timeout=TIMEOUT_SECONDS, check=lambda m: m.author == game.get_current_player())
        await message.channel.send(f'{response_message.author.mention} responded with: {response_message.content}')
        game.next_turn()
    except asyncio.TimeoutError:
        await message.channel.send(f'{game.get_current_player().mention} did not respond in time. Skipping their turn.')
        game.next_turn()

client.run('YOUR_TOKEN')
