## Hard Coded to one server & Map Size
#
#Unused imports, remove with caution

#Sends messages in discord twice sometimes
import discord, time, nltk, numpy, requests, random
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from PyQt5 import QtWidgets, QtGui

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description)


#Will display in the IDE or Console
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if message.content.startswith('?ping'):#Check discord server messages for command keywords
        await bot.add_reaction(message, '\U0001F914') #Bot reacts to message with *thinking*
        print(str(message.author) + " used Ping") #Prints out Discord ID of calling player
        await bot.process_commands(message) #Return the bot to listening for @bot.commands
    if message.content.startswith('?siege'):
        await bot.add_reaction(message, '\U0001F914')
        print(str(message.author) + " used Siege Search")
        await bot.process_commands(message)
    await bot.process_commands(message)

@bot.command()
async def death():
    def deathgrab():
        loadhold = []
        load = []
        deaths = []
        #servers with RustIO upload death events and causes in a json file
        r = requests.get(url='http://149.56.19.220:28076/deaths.json')
        temp = str(r.json()) #convert from json
        temp = temp.replace('[', '') #cleaning list
        temp = temp.replace(']', '')
        temp = temp.replace('{', '')
        temp = temp[:-1]
        temp = temp.split("}")
        for i in range(1, len(temp)):
            temp[i] = temp[i][1:]
        for i in range(0, len(temp) -1):
            loadhold.append(temp[i])
        for i in range(0, len(loadhold[:10])):
            hold = loadhold[i].split(',')
            load.append(hold)
        #take only x and z from lists and append to new list
        for i in range(0, len(load)):
            load[i][0] = load[i][0][5:]
            load[i][1] = load[i][1][6:]

        #hardcoded for mapsize, use playrust.io and the ingame map to calculate the required coordnate tags {0}{1}{2} in each element of coords list, or test to check default       
        coords = [ [-2100, 'B', 29], [-1950, 'C', 28], [-1800, 'D', 27], [-1650, 'E', 26], [-1500, 'F', 25], [-1350, 'G', 24], [-1200, 'H', 23], [-1050, 'I', 22], [-900, 'J', 21], [-750, 'K', 20], [-600, 'L', 19], [-450, 'M', 18], [-300, 'N', 17],  [-150, 'O', 16],  [0, 'P', 15], [150, 'Q', 14], [300, 'R', 13], [450, 'S', 12], [600, 'T', 11], [750, 'U', 10], [900, 'V', 9], [1050, 'W', 8], [1200, 'X', 7], [1350, 'Y', 6], [1500, 'Z', 5], [1650, 'AA', 4], [1800, 'AB', 3], [1950, 'AC', 2], [2100, 'AD', 1] ]
        xloc = []
        yloc = []
        #take the x and z coordinates from the json file and compare them to the first elements of coords, the map is square so the number words for both, and assign the Letter and Number values to a new list
        for i in range(0, len(load)):
            for o in range(0, len(coords)):
                if int(load[i][0]) > coords[o][0] and int(load[i][0]) < coords[o+1][0]:
                    xloc.append(str(coords[o][1] + " - " + str(coords[o+1][1])))
            try:
                for o in range(0, len(coords)):
                    if int(load[i][1]) > coords[o][0] and int(load[i][1]) < coords[o+1][0]:
                        yloc.append(str(coords[o][2]) + " - " + str(coords[o+1][2]))
            except:
                #effective y axis is trimmed, had issues, easy fix
                yloc.append("29")

        for i in range(0, len(xloc) -1):
            #combine the lists created above, and seperate with a space
            print(xloc[i] + " " + yloc[i])
            deaths.append(xloc[i] + " " + yloc[i])
        #funtion returns the final list
        return(deaths)
    #bot sends the list as a user in discord, it was converted to a string and passes clean
    await bot.say(deathgrab())

#Get the current online users and their connection time from battlemetrics.com
#hardcode your server url, or edit the code and prompt for the user to paste the required id
#at the ending of the site variable, probably using a @bot.event

@bot.command()
async def ping():
    def search():
        site = "https://www.battlemetrics.com/servers/rust/433578"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        soup = BeautifulSoup(page, "html.parser")
        online = []
        player = []
        panel = str(soup.find('dl', class_='dl-horizontal'))
        panel = panel.split("<")
        panel = str(panel).split(">")
        panel = str(panel).split(",")
        panel = str(panel).split("\\")
        panel = str(panel).split('"')
        active_panel = soup.find('table', class_='bm-table')
        player_panel = active_panel.find('tbody')
        player_list = player_panel.find_all(class_='player-name')
        player_time_panel = player_panel.find_all('time')
        playercount = panel[69]
        playercount = playercount[:4]
        for i in range(0, len(player_list)):
            player_list[i] = str(player_list[i])[:-4]
            player_list[i] = str(player_list[i])[68:]
            player.append(player_list[i])
        for i in range(0, len(player_time_panel)):
            player_time_panel[i] = str(player_time_panel[i])[37:]
            player_time_panel[i] = str(player_time_panel[i])[:-70]
        online.append("Area 51 (" + playercount +"):\n ")
        for i in range(0, len(player_list)):
            online.append(player_list[i] + " -+- " + player_time_panel[i] + "  -|-  ")
        onlinestring = ' '.join(str(x) for x in online)
        return(onlinestring)
    await bot.say(search())

#SIEGE SEARCH
@bot.command()
#takes ubisoft id name after ?siege *with a space after*, and stores in content variable
async def siege(content='repeating...'):
    def convUser(username):

        #takes raw input from runSearch()
        names = nltk.word_tokenize(username)
        global fnamelist
        fnamelist = names
        return names

    def getRank(x):
        #x is soup from Search()
        tokpanel = str(x.find('div', id = 'season-10'))
        tokpanel = nltk.word_tokenize(tokpanel)
        del tokpanel[0:63]
        del tokpanel[1: len(tokpanel)]
        tokpanel[0] = tokpanel[0][-22:-16]
        tokpanel[0] = tokpanel[0].replace("-","")
        tokpanel[0] = tokpanel[0].replace("rank","")
        ranklist = ["Copper IV", "Copper III", "Copper II", "Copper I",
                    "Bronze IV", "Bronze III", "Bronze II", "Bronze I",
                    "Silver IV", "Silver III", "Silver II", "Silver I",
                    "Gold IV", "Gold III", "Gold II", "Gold I", "Plat III",
                    "Plat II", "Plat I", "DIAMOND"]
        rank = ranklist[int(tokpanel[0]) - 1]
        return rank

    def getWinLoss(x):
        #x is soup from Search()
        infopanel = x.find('div', id = 'season-10')
        infopanelsmall = infopanel.find_all('div', class_="value")
        infopanelsmall = str(infopanelsmall)
        infopanel = nltk.word_tokenize(infopanelsmall)
        infopanelsmall = infopanelsmall.split("\n")
        winloss = infopanelsmall[15]
        return winloss

    def getMMR(x):
        #x is soup from Search()
        infopanel = x.find('div', id = 'season-10')
        infopanelsmall = infopanel.find_all('div', class_="value")
        infopanelsmall = str(infopanelsmall)
        infopanel = nltk.word_tokenize(infopanelsmall)
        infopanelsmall = infopanelsmall.split("\n")
        mmr = infopanelsmall[9]
        return mmr

    def getHMMR(x):
        #x is soup from Search()
        infopanel = x.find('div', id = 'season-10')
        infopanelsmall = infopanel.find_all('div', class_="value")
        infopanelsmall = str(infopanelsmall)
        infopanel = nltk.word_tokenize(infopanelsmall)
        infopanelsmall = infopanelsmall.split("\n")
        hmmr = infopanelsmall[11]
        return hmmr

    def getCasualKD(x):
        #x is soup from Search
        mainpanel = str(x.find('div', class_='trn-stats'))
        mainpanel = nltk.word_tokenize(mainpanel)
        del mainpanel[0:375]
        del mainpanel[1:len(mainpanel)]
        KD = mainpanel[0]
        return KD

    def Search(x):
        #try:
        #x takes username from convUsername
        site = "https://r6.tracker.network/profile/pc/" + x
        #set header to allow script to access site
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = Request(site,headers=hdr)
        page = urlopen(req)
        #parse the site saved in site variable
        soup = BeautifulSoup(page, "html.parser")
        return soup

        
        """except:
            result = ("Invalid Player Name(s), Please Try Again")
            time.sleep(4)
            return result"""

    def runSearch(x):
        #x is passed from other function
        #gets back tokenized list from NLTK
        names = convUser(x)
        for i in range(0, len(names)):
            global fKD, fhmmr, fmmr, fwinloss, frank, fname, labels
            #calls each function to get player stats from single save
            fKD = getCasualKD(Search(names[i]))
            fhmmr = getHMMR(Search(names[i]))
            fmmr = getMMR(Search(names[i]))
            fwinloss = getWinLoss(Search(names[i]))
            frank = getRank(Search(names[i]))
            fname = names[i]
            #print the data out in a formatted way
            output = "Siege Stats: \n "+ "Ubisoft ID: " + fname + "\n Rank: " + frank + "\n Casual KD: " + fKD + "\n Highest MMR: " +fhmmr+ "\n Current MMR: " + fmmr + "\n Ranked Win/Loss: " +fwinloss
            return output
    


    #
    await bot.say(runSearch(content))
  

#Havent tested 
@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

bot.run("NDQzMjEzOTI1NzQ0NTA4OTUw.Dj7S_g.XxRCJlpQfoZ_VtWfipMHmIxc1tA")
