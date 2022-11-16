import discord
import os
from KeepAlive import keep_alive
import random
import json
import requests
from neuralintents import GenericAssistant

chatbot = GenericAssistant("intents.json")
chatbot.train_model()
chatbot.save_model()

client = discord.Client()
abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
       'w', 'x', 'y', 'z']


# random_letter = random.choice(abc)


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("What's popping?"):
        await message.channel.send("Don't mind me, just watching.")

    if message.content.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    if message.channel.id == CHATBOTCHANNEL:
        response = chatbot.request(message.content)
        await message.channel.send(response)



    if message.content.startswith("!help"):
        await message.channel.send(
            "Hello! I am bot that responds to commands and messages in chat." 
            "Here are some commands I can do: "
            "!wordfight - A game that whoever types a random letter first wins. \n"
            "!inspire - Get some inspiration from quotes. \n"
            "!help - Get information about this bot, this command.\n"
            "I also have a chat bot feature if you type in the botchat channel which uses AI to recognize things like greetings and respond accordingly.")

    if message.content.startswith("!wordfight"):

        channel = message.channel

        def check(m):
            return m.content == random_letter and m.channel == channel


        random_letter = random.choice(abc)
        await message.channel.send('First person to say ' + random_letter + ' wins!')
        msg = await client.wait_for('message', check=check)
        await message.channel.send('{.author} is the winner!'.format(msg))


    if any([keyword in message.content.upper() for keyword in ('SOPHISTICATED', 'FANCY', 'MYSTERY')]):
        await message.channel.send(":face_with_monocle:")
    if 'SURE' in message.content.upper():
        await message.channel.send(":face_with_raised_eyebrow:")


keep_alive()
#TOKEN = 
client.run(TOKEN)
