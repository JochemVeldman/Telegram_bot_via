from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import logging, urllib2, json, re, urllib
    
def start(bot, update):
    update.message.reply_text("Hi, welcome to the directions bot. To start, type /directions and enter the start town and address, and the destination town and address.")
	
def info(bot, update):
    update.message.reply_text("Hi, welcome to the directions bot. Here is some information about this bot. You can start using this bot using /directions. After that, you will have to pass some arguments: start town, address, end town, address. Example input could be: 'Dronten florijn 39 Almere verzetslaan 24'. With these arguments, the bot requests the desired information using the google maps API. JSON results are returned and parsed so it's readable by humans. Enjoy!")
	
def directions(bot, update, args):
	argus = {}
	try:
		argus['origin'] = args[0] + " " + args[1] + " " + args[2]
		argus['destination'] = args[3] + " " + args[4] + " " + args[5]
		argus['key'] = "AIzaSyAfFlTh7-FbAymdjBjE1H59aYomDByB2lA"
		
		params = urllib.urlencode(argus)
		req = urllib2.urlopen("https://maps.googleapis.com/maps/api/directions/json?" + params)
		data = json.load(req)   
		directions = data['routes'][0]['legs'][0]['steps']
		distance = data['routes'][0]['legs'][0]['distance']['text']
		duration = data['routes'][0]['legs'][0]['duration']['text']
		end_address = data['routes'][0]['legs'][0]['end_address']
		start_address = data['routes'][0]['legs'][0]['start_address']
		
		update.message.reply_text("Hey. Here are the directions from " + start_address + " to " + end_address + '. Estimated distance: ' + distance + '. Estimated duration: ' + duration)
	
		for count, step in enumerate(directions):
			update.message.reply_text(re.sub('<[^<]+?>', '', 'Step ' + str(count) + ': ' + step['html_instructions']))	
	except (IndexError, ValueError):
		update.message.reply_text('Make sure the arguments are OK')

def main():
    updater = Updater(token="471478170:AAHVyQ7Gvpi7XhmwyGbyqi-mgJ3fyhQ74bU")
    updater.dispatcher.add_handler(CommandHandler("directions", directions, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("info", info))
    updater.start_polling()
    updater.idle()
    
if __name__ == "__main__":
	main()