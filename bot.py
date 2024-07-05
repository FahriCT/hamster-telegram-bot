import subprocess
import logging
import re
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


user_data = {}


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        'BOT FAHRI HAMSTER\n'
        '1. /in <query_id> = Input Query id\n'
        '2. /ck = Cek query id mu\n'
        '3. /run = Jalankan Bot\n'
        '4. /r = Refresh status bot mu'
    )


def input_query_id(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Penggunaan: /in <query_id>')
        return
    
    query_id = context.args[0]
    user_id = update.message.from_user.id
    user_data[user_id] = query_id
    update.message.reply_text('Query id berhasil disimpan')


def check_query_id(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if query_id:
        update.message.reply_text(f'Query id di akun mu adalah {query_id}')
    else:
        update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')


def run_bot(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if not query_id:
        update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')
        return
    
    try:
        result = subprocess.run(['python3', '/path/to/hamster.py', query_id], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            level = re.search(r"\[ Level \] : (\d+)", output)
            total_earned = re.search(r"\[ Total Earned \] : (\d+)", output)
            coin = re.search(r"\[ Coin \] : (\d+)", output)
            energy = re.search(r"\[ Energy \] : (\d+)", output)
            level_energy = re.search(r"\[ Level Energy \] : (\d+)", output)
            level_tap = re.search(r"\[ Level Tap \] : (\d+)", output)
            exchange = re.search(r"\[ Exchange \] : (\d+)", output)

            response = "Bot berjalan\n"
            if level:
                response += f"[ Level ] : {level.group(1)}\n"
            if total_earned:
                response += f"[ Total Earned ] : {total_earned.group(1)}\n"
            if coin:
                response += f"[ Coin ] : {coin.group(1)}\n"
            if energy:
                response += f"[ Energy ] : {energy.group(1)}\n"
            if level_energy:
                response += f"[ Level Energy ] : {level_energy.group(1)}\n"
            if level_tap:
                response += f"[ Level Tap ] : {level_tap.group(1)}\n"
            if exchange:
                response += f"[ Exchange ] : {exchange.group(1)}\n"
            
            update.message.reply_text(response)
        else:
            update.message.reply_text(f'Gagal menjalankan bot:\n{result.stderr}')
    except Exception as e:
        update.message.reply_text(f'Error: {str(e)}')


def refresh_status(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if not query_id:
        update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')
        return
    
    try:
        result = subprocess.run(['python3', '/path/to/hamster.py', query_id], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            level = re.search(r"\[ Level \] : (\d+)", output)
            total_earned = re.search(r"\[ Total Earned \] : (\d+)", output)
            coin = re.search(r"\[ Coin \] : (\d+)", output)
            energy = re.search(r"\[ Energy \] : (\d+)", output)
            level_energy = re.search(r"\[ Level Energy \] : (\d+)", output)
            level_tap = re.search(r"\[ Level Tap \] : (\d+)", output)
            exchange = re.search(r"\[ Exchange \] : (\d+)", output)

            response = "Ini adalah status bot mu saat ini\n"
            if level:
                response += f"[ Level ] : {level.group(1)}\n"
            if total_earned:
                response += f"[ Total Earned ] : {total_earned.group(1)}\n"
            if coin:
                response += f"[ Coin ] : {coin.group(1)}\n"
            if energy:
                response += f"[ Energy ] : {energy.group(1)}\n"
            if level_energy:
                response += f"[ Level Energy ] : {level_energy.group(1)}\n"
            if level_tap:
                response += f"[ Level Tap ] : {level_tap.group(1)}\n"
            if exchange:
                response += f"[ Exchange ] : {exchange.group(1)}\n"
            
            update.message.reply_text(response)
        else:
            update.message.reply_text(f'Gagal menjalankan bot:\n{result.stderr}')
    except Exception as e:
        update.message.reply_text(f'Error: {str(e)}')

def main() -> None:
    # Token bot Telegram
    TOKEN = 'YOUR_TELEGRAM_BOT'

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('in', input_query_id))
    dispatcher.add_handler(CommandHandler('ck', check_query_id))
    dispatcher.add_handler(CommandHandler('run', run_bot))
    dispatcher.add_handler(CommandHandler('r', refresh_status))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
