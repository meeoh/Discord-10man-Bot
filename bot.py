import discord
import asyncio
import myToken
from pprint import pprint

client = discord.Client()
ourServer = None

@client.event
async def on_ready():
    global ourServer
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')    
    t = iter(client.servers)    
    for server in t:            
        if(server.name == "10 men"):            
            ourServer = server

    onlineUsers = []
    #test stuff here
    it = iter(ourServer.members)
    for user in it:
        print(user.name + " " + str(user.status))                  
        if(str(user.status) != "offline" and user.name != "DAD Scrim BOT"):
            onlineUsers.append(user.name)

    onlineUsers.sort(key=str.lower)
    print(onlineUsers)



@client.event
async def on_message(message):
    #heres when someone actually uses !scrim
    if message.content.startswith('!scrim'):
        it = iter(ourServer.members)
        # for user in it:            
        #     print(user.status)           
        await client.send_message(message.channel,'IM WORKING ON IT FUCK OFF');


    #     counter = 0
    #     tmp = await client.send_message(message.channel, 'Calculating messages...')
    #     async for log in client.logs_from(message.channel, limit=100):
    #         if log.author == message.author:
    #             counter += 1

    #     await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    # elif message.content.startswith('!sleep'):
    #     await asyncio.sleep(5)
    #     await client.send_message(message.channel, 'Done sleeping')

client.run(myToken.token)