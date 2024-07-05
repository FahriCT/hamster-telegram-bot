import subprocess
import logging
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary untuk menyimpan query_id user
user_data = {}

# Command handler untuk /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        'BOT FAHRI HAMSTER\n'
        '1. /in <query_id> = Input Query id\n'
        '2. /ck = Cek query id mu\n'
        '3. /run = Jalankan Bot\n'
        '4. /r = Refresh status bot mu'
    )

# Command handler untuk /in <query_id>
async def input_query_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Penggunaan: /in <query_id>')
        return
    
    query_id = context.args[0]
    user_id = update.message.from_user.id
    user_data[user_id] = query_id
    await update.message.reply_text('Query id berhasil disimpan')

# Command handler untuk /ck
async def check_query_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if query_id:
        await update.message.reply_text(f'Query id di akun mu adalah {query_id}')
    else:
        await update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')

# Command handler untuk /run
async def run_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if not query_id:
        await update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')
        return
    
    try:
        result = subprocess.run(['python3', '/path/to/hamster.py', query_id], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            # Mengurai output konsol untuk mendapatkan informasi yang diperlukan
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

            await update.message.reply_text(response)
        else:
            await update.message.reply_text(f'Gagal menjalankan bot: {result.stderr}')
    except Exception as e:
        await update.message.reply_text(str(e))

# Command handler untuk /r
async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    query_id = user_data.get(user_id)
    
    if not query_id:
        await update.message.reply_text('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.')
        return
    
    try:
        result = subprocess.run(['python3', '/path/to/hamster.py', query_id], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            # Mengurai output konsol untuk mendapatkan informasi yang diperlukan
            level = re.search(r"\[ Level \] : (\d+)", output)
            total_earned = re.search(r"\[ Total Earned \] : (\d+)", output)
            coin = re.search(r"\[ Coin \] : (\d+)", output)
            energy = re.search(r"\[ Energy \] : (\d+)", output)
            level_energy = re.search(r"\[ Level Energy \] : (\d+)", output)
            level_tap = re.search(r"\[ Level Tap \] : (\d+)", output)
            exchange = re.search(r"\[ Exchange \] : (\d+)", output)

            response = "Ini adalah status bot mu saat ini:\n"
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

            await update.message.reply_text(response)
        else:
            await update.message.reply_text(f'Gagal menjalankan bot: {result.stderr}')
    except Exception as e:
        await update.message.reply_text(str(e))

def main() -> None:
    # Buat Updater dan pasang token bot
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    # Pasang semua command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("in", input_query_id))
    application.add_handler(CommandHandler("ck", check_query_id))
    application.add_handler(CommandHandler("run", run_bot))
    application.add_handler(CommandHandler("r", refresh))

    # Mulai bot
    application.run_polling()

if __name__ == "__main__":
    main()
