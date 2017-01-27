import discord
import asyncio
import myToken
from pprint import pprint

client = discord.Client()
ourServer = None
inProgress = False
readyUsers = []


@client.event
async def on_ready():
    global ourServer
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')    
    
def clear_chat_channel(message):
    counter = 0
    all_messages = client.messages
    target_channel = message.channel
    for message_step in all_messages:
        if message_step.channel == target_channel:
            client.delete_message(message_step)
            counter += 1
    client.send_message(message.channel, 'I have removed %s old messages' % counter)

@client.event
async def on_message(message):
    #heres when someone actually uses !scrim
    global inProgress
    global readyUsers
    author = str(message.author).split("#")[0]
    if(message.channel.name != "bot-setup" and message.content.startswith("!")):
        await client.send_message(message.channel, "Please use the bot-setup channel")
        return    



    if (message.content.startswith("!gaben") or message.content.startswith('!ready')) and inProgress == False and len(readyUsers) < 10:        
        if(author in readyUsers):            
            await client.send_message(message.channel, "You're already ready, chill")

        else:
            readyUsers.append(author)
            await client.send_message(message.channel, author + " is now ready, we need " + str(10 - len(readyUsers)) + " more")
            if(len(readyUsers) == 10):
                await client.send_message(message.channel, "we ready boiz.")

    if message.content.startswith('!clear'):
        clear_chat_channel(message)




    elif (message.content.startswith('!unready') or message.content.startswith('!ungaben')) and inProgress == False:
        for user in readyUsers:
            if user.upper() == author.upper():
                readyUsers.remove(user)
                await client.send_message(message.channel, author + " You are no longer ready. We now need " + str(10 - len(readyUsers)) + " more")            
                break

    #stopping one        
    elif message.content.startswith('!done'):
        inProgress = False
        readyUsers = []
        await client.send_message(message.channel, "Current 10man finished, to make a new one, type !10man")  



client.run(myToken.token)
