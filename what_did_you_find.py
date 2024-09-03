import telebot
import random
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = telebot.TeleBot('7362185509:AAFDqUHyG73RlFWL1dmFx8asqXkHQNglJnE')

# Game data
items = {
    'Garbage Collection': ['plastic', 'boots', 'underwear', 'jewellery', 'rings', 'rotten food', 'broken laptop', 'money'],
    'Loot Local Shop': ['few bucks', 'couple hundred', 'important ornament', 'caught'],
    'Underground Fights': ['ko 5 opponents', 'ko by first opponent', 'lost all fights'],
    'Scout Intelligence': ['took down rival gang', 'suspected and caught', 'rival gang bribed police']
}

# Function to create main menu
def main_menu():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Garbage Collection", callback_data="garbage"),
               InlineKeyboardButton("Loot Local Shop", callback_data="loot"),
               InlineKeyboardButton("Underground Fights", callback_data="fights"),
               InlineKeyboardButton("Scout Intelligence", callback_data="scout"))
    return markup

# Start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to 'Was It Worth' game!", reply_markup=main_menu())

# Callback query handler
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "garbage":
        bot.answer_callback_query(call.id, "Searching for garbage...")
        time.sleep(5)  # Simulate search time
        found_items = random.sample(items['Garbage Collection'], 3)  # Find 3 random items
        result = "After searching the garbage cans, you found:\n" + "\n".join(found_items)
        bot.send_message(call.from_user.id, result)
    elif call.data == "loot":
        bot.answer_callback_query(call.id, "Looting local shop...")
        time.sleep(3)  # Simulate looting time
        result = random.choice(items['Loot Local Shop'])
        if result == 'caught':
            bot.send_message(call.from_user.id, "You were caught and have to pay bail!")
        else:
            bot.send_message(call.from_user.id, f"You successfully looted and got: {result}")
    elif call.data == "fights":
        bot.answer_callback_query(call.id, "Entering underground fight...")
        time.sleep(3)  # Simulate fight time
        result = random.choice(items['Underground Fights'])
        if result == 'ko 5 opponents':
            money = random.randint(100, 500)
            bot.send_message(call.from_user.id, f"You {result} and won ${money}!")
        else:
            bot.send_message(call.from_user.id, f"You {result} and won nothing.")
    elif call.data == "scout":
        bot.answer_callback_query(call.id, "Scouting for intelligence...")
        time.sleep(3)  # Simulate scouting time
        result = random.choice(items['Scout Intelligence'])
        if result == 'took down rival gang':
            money = random.randint(500, 2000)
            bot.send_message(call.from_user.id, f"You {result} and earned ${money}!")
        elif result == 'suspected and caught':
            bot.send_message(call.from_user.id, "You were suspected and caught by the police!")
        else:
            money = random.randint(100, 1000)
            bot.send_message(call.from_user.id, f"The {result}. You have to pay them ${money}.")
    
    # Return to main menu after each action
    bot.send_message(call.from_user.id, "What would you like to do next?", reply_markup=main_menu())

# Start the bot
bot.polling()