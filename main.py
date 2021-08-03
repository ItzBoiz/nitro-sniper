import keep_alive
import asyncio
import json
import time
import traceback
from os import system, getenv
from random import randint
from discord.ext import commands
import re
import httpx
from colorama import Fore, init
import platform

init()
data = {}

token = getenv('token')

os = platform.system()

if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

print(Fore.RED + """\
███╗░░██╗██╗████████╗██████╗░░█████╗░  ░██████╗███╗░░██╗██╗██████╗░███████╗██████╗░
████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗  ██╔════╝████╗░██║██║██╔══██╗██╔════╝██╔══██╗
██╔██╗██║██║░░░██║░░░██████╔╝██║░░██║  ╚█████╗░██╔██╗██║██║██████╔╝█████╗░░██████╔╝
██║╚████║██║░░░██║░░░██╔══██╗██║░░██║  ░╚═══██╗██║╚████║██║██╔═══╝░██╔══╝░░██╔══██╗
██║░╚███║██║░░░██║░░░██║░░██║╚█████╔╝  ██████╔╝██║░╚███║██║██║░░░░░███████╗██║░░██║
╚═╝░░╚══╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░  ╚═════╝░╚═╝░░╚══╝╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝
 ░                   ░                           ░
 """ + Fore.RESET)

bot = commands.Bot(command_prefix=".", self_bot=True)
ready = False

codeRegex = re.compile(
    "(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)")

while 1:
    try:

        @bot.event
        async def on_message(ctx):
            global ready
            if not ready:
                print(Fore.LIGHTCYAN_EX +
                      'Sniping Discord Nitro and Giveaway on ' +
                      str(len(bot.guilds)) + ' Servers 🔫\n' + Fore.RESET)
                print(Fore.LIGHTBLUE_EX +
                      time.strftime("%H:%M:%S ", time.localtime()) +
                      Fore.RESET,
                      end='')
                print("[+] Bot is ready")
                ready = True
            if codeRegex.search(ctx.content):
                print(Fore.LIGHTBLUE_EX +
                      time.strftime("%H:%M:%S ", time.localtime()) +
                      Fore.RESET,
                      end='')
                code = codeRegex.search(ctx.content).group(2)

                start_time = time.time()
                if len(code) < 16:
                    try:
                        print(Fore.LIGHTRED_EX +
                              "[=] Auto-detected a fake code: " + code +
                              " From " + ctx.author.name + "#" +
                              ctx.author.discriminator + Fore.LIGHTMAGENTA_EX +
                              " [" + ctx.guild.name + " > " +
                              ctx.channel.name + "]" + Fore.RESET)
                    except:
                        print(Fore.LIGHTRED_EX +
                              "[=] Auto-detected a fake code: " + code +
                              " From " + ctx.author.name + "#" +
                              ctx.author.discriminator + Fore.RESET)

                else:
                    async with httpx.AsyncClient() as client:
                        result = await client.post(
                            'https://discordapp.com/api/v6/entitlements/gift-codes/'
                            + code + '/redeem',
                            json={'channel_id': str(ctx.channel.id)},
                            headers={
                                'authorization': token,
                                'user-agent': 'Mozilla/5.0'
                            })
                        delay = (time.time() - start_time)
                        try:
                            print(Fore.LIGHTGREEN_EX + "[-] Sniped code: " +
                                  Fore.LIGHTRED_EX + code + Fore.RESET +
                                  " From " + ctx.author.name + "#" +
                                  ctx.author.discriminator +
                                  Fore.LIGHTMAGENTA_EX + " [" +
                                  ctx.guild.name + " > " + ctx.channel.name +
                                  "]" + Fore.RESET)
                        except:
                            print(Fore.LIGHTGREEN_EX + "[-] Sniped code: " +
                                  Fore.LIGHTRED_EX + code + Fore.RESET +
                                  " From " + ctx.author.name + "#" +
                                  ctx.author.discriminator + Fore.RESET)

                    if 'This gift has been redeemed already' in str(
                            result.content):
                        print(Fore.LIGHTBLUE_EX +
                              time.strftime("%H:%M:%S ", time.localtime()) +
                              Fore.RESET,
                              end='')
                        print(Fore.LIGHTYELLOW_EX +
                              "[-] Code has been already redeemed" +
                              Fore.RESET,
                              end='')
                    elif 'nitro' in str(result.content):
                        print(Fore.LIGHTBLUE_EX +
                              time.strftime("%H:%M:%S ", time.localtime()) +
                              Fore.RESET,
                              end='')
                        print(Fore.GREEN + "[+] Code applied" + Fore.RESET,
                              end='')
                    elif 'Unknown Gift Code' in str(result.content):
                        print(Fore.LIGHTBLUE_EX +
                              time.strftime("%H:%M:%S ", time.localtime()) +
                              Fore.RESET,
                              end='')
                        print(Fore.LIGHTRED_EX + "[-] Invalid Code" +
                              Fore.RESET,
                              end=' ')

        keep_alive.keep_alive()
        bot.run(token, bot=False)
    except:
        file = open("traceback.txt", "w")
        file.write(traceback.format_exc())
        file.close()
        exit(0)
        exit(0)
