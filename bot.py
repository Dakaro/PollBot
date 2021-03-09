import os

import discord 
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GILD = os.getenv('DISCORD_GUILD')
#TOKEN = DISCORD_TOKEN


client = discord.Client()

message_id = None

async def show_help():
    embed_var = discord.Embed(title='PollBot', description='Bot for voting', color=0xE93610 )
    embed_var.add_field(name="-help", value="show help", inline=False)
    embed_var.add_field(name="-voting", value="message for voting. Uder this command you have to type emoji with description", inline=False)
    embed_var.add_field(name="-result", value="showing results of the latest voting", inline=False)
    return embed_var

async def voting(message):
    global message_id
    message_id = message

@client.event
async def show_results(message):
    array = [ (r.count, r.emoji) for r in message.reactions ]
    total_count = 0
    results_txt = '\nvoting results: '
    for r in message.reactions:
        total_count += r.count 
    for i in array:
        procent_result = int( i[0]/total_count * 100)
        results_txt += '\n'+ i[1] + ': ' + str(procent_result) + ' % \n' 
    return results_txt


@client.event 
async def on_message(message):
    if '-voting' in message.content:
        await voting(message)

    if message.content == '-result':
        show_results(message_id)
        if message_id == None:
            await message.channel.send('error: You did not make a voting type "-help" for more')
        else:
            await message.channel.send( await show_results(message_id) )

    if message.content == '-help':
        await message.channel.send( embed =  await show_help() )


client.run(TOKEN)