import discord
import asyncio
import myToken
from pprint import pprint

client = discord.Client()
ourServer = None
inProgress = False
readyUsers = []
firstCaptain = ""
secondCaptain = ""
teamOne = []
teamTwo = []
currentPickingCaptain = ""
pickNum = 1


@client.event
async def on_ready():
    global ourServer
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')    


@client.event
async def on_message(message):
    #heres when someone actually uses !scrim
    global inProgress
    global readyUsers
    global firstCaptain
    global secondCaptain
    global teamOne
    global teamTwo
    global pickNum

    author = str(message.author).split("#")[0]

    if(message.channel.name != "testchannel" and message.content.startswith("!")):
        print(message.channel.name)
        await client.send_message(message.channel, "Please use the bot-setup channel")
        return    



    if (message.content.startswith("!gaben") or message.content.startswith('!ready')) and inProgress == False and len(readyUsers) < 10:        
        if(author in readyUsers):            
            await client.send_message(message.channel, "You're already ready, chill")    
        else:
            readyUsers.append(author)
            await client.send_message(message.channel, author + " is now ready, we need " + str(10 - len(readyUsers)) + " more")
            if(len(readyUsers) == 2):
                await client.send_message(message.channel, "we ready boiz. Please pick two captains by doing !captains captain1 captain2")
                inProgress = True


    elif (message.content.startswith('!captains') and inProgress == True):
        if (firstCaptain != "" and secondCaptain != ""):
            await client.send_message(message.channel, "We already have captains. To change them do !done and start over")
            return

        firstCaptain = message.content.split(" ",1)[1].split()[0]
        secondCaptain = message.content.split(" ",1)[1].split()[1]
        await client.send_message(message.channel, "First captain is now " + firstCaptain + ". Second captain is now " + secondCaptain)
        await client.send_message(message.channel, firstCaptain + " it is now your pick, pick with !pick user. Please choose from " + " ".join(readyUsers))
        readyUsers.remove(firstCaptain)
        readyUsers.remove(secondCaptain)

    elif (message.content.startswith('!pick') and inProgress == True and pickNum < 10):
        if(pickNum == 9):
            await client.send_message(message.channel, "The teams are now made and bot setup is finished.")
            inProgress = False
            readyUsers = []
            firstCaptain = ""
            secondCaptain = ""
            pickNum = 1
            return

        if author.upper() == firstCaptain.upper() and (pickNum == 1 or pickNum == 4 or pickNum == 6 or pickNum == 8 or pickNum == 10):
            pickedUser = message.content.split(" ",1)[1]
            teamOne.append(pickedUser)
            for temp in readyUsers:
                if temp.upper() == pickedUser.upper():
                    readyUsers.remove(temp)
                    break       

            pickNum+=1
            if(pickNum == 2 or pickNum == 3 or pickNum == 5 or pickNum == 7 or pickNum == 9):
                await client.send_message(message.channel, secondCaptain + " it is now your pick, pick with !pick user. Please choose from " + " ".join(readyUsers))
            else:
                await client.send_message(message.channel, firstCaptain + " please pick again from" + " ".join(readyUsers))


        if author.upper() == secondCaptain.upper() and (pickNum == 2 or pickNum == 3 or pickNum == 5 or pickNum == 7 or pickNum == 9):
            pickedUser = message.content.split(" ",1)[1]
            teamTwo.append(pickedUser)
            for temp in readyUsers:
                if temp.upper() == pickedUser.upper():
                    readyUsers.remove(temp)
                    break    

            pickNum+=1
            if(pickNum == 1 or pickNum == 4 or pickNum == 6 or pickNum == 8 or pickNum == 10):
                await client.send_message(message.channel, firstCaptain + " it is now your pick, pick with !pick user. Please choose from " + " ".join(readyUsers))
            else:
                await client.send_message(message.channel, secondCaptain + " please pick again from" + " ".join(readyUsers))
                     
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
        firstCaptain = ""
        secondCaptain = ""
        pickNum = 1
        await client.send_message(message.channel, "Current 10man finished, to make a new one, we need 10 ready users")    

client.run(myToken.token)