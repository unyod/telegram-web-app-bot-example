from flask import Flask, render_template, request, jsonify
import telebot
import sqlite3
import threading
import os

TOKEN = "BOT_TOKENINGIZ"
WEBAPP_URL = "https://YOUR_RENDER_LINK.onrender.com"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# DATABASE

def connect_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            coins INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# USER CREATE

def create_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT OR IGNORE INTO users (user_id, coins) VALUES (?, ?)',
        (user_id, 0)
    )

    conn.commit()
    conn.close()


# UPDATE COINS

def update_coins(user_id, coins):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        'UPDATE users SET coins=? WHERE user_id=?',
        (coins, user_id)
    )

    conn.commit()
    conn.close()


# GET TOP USERS

def get_top_users():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        'SELECT * FROM users ORDER BY coins DESC LIMIT 50'
    )

    users = cursor.fetchall()

    conn.close()

    return users


# HOME PAGE

@app.route('/')
def home():
    return render_template('index.html')


# SAVE COINS

@app.route('/save', methods=['POST'])
def save():

    data = request.get_json()

    user_id = data.get('user_id')
    coins = data.get('coins')

    if user_id is None or coins is None:
        return jsonify({
            'status': 'error'
        }), 400

    create_user(user_id)
    update_coins(user_id, coins)

    return jsonify({
        'status': 'success',
        'coins': coins
    })


# ADMIN PANEL

@app.route('/admin')
def admin():

    users = get_top_users()

    return render_template(
        'admin.html',
        users=users
    )


# TELEGRAM BOT

@bot.message_handler(commands=['start'])
def start(message):

    create_user(message.from_user.id)

    keyboard = telebot.types.InlineKeyboardMarkup()

    web_app = telebot.types.WebAppInfo(WEBAPP_URL)

    button = telebot.types.InlineKeyboardButton(
        text='🎮 PLAY GAME',
        web_app=web_app
    )

    keyboard.add(button)

    bot.send_message(
        message.chat.id,
        '⚡ Tap Game ga xush kelibsiz!',
        reply_markup=keyboard
    )


# FLASK START

def run_flask():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


threading.Thread(target=run_flask).start()

print('BOT IS RUNNING...')

bot.infinity_polling(skip_pending=True)