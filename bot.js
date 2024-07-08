const { Telegraf } = require('telegraf');
const { exec } = require('child_process');
const fs = require('fs');
const BOT_TOKEN = fs.readFileSync('token.txt', 'utf8').trim();
const bot = new Telegraf(BOT_TOKEN);
const dataPath = 'data/';
const user_data = {};
const user_status = {};

bot.command('start', async (ctx) => {
    await ctx.reply(`
        Bot Hamster Kombat 🐹 \n
        1. /qi <query_id> -  Input Query ID ✍️\n
        2. /ck   = Cek query id mu 🔍\n
        3. /run  = Jalankan Bot 🚀\n
        5. /dlt.  = Hapus query id ❌\n
    `);
});

bot.command('in', async (ctx) => {
    const query_id = ctx.message.text.split(' ')[1];
    const user_id = ctx.message.from.id;

    try {
        fs.writeFileSync(`${dataPath}${user_id}.txt`, query_id.trim());
        user_data[user_id] = query_id.trim();
        await ctx.reply('✅ Query id berhasil disimpan');
    } catch (error) {
        console.error(`❌ Gagal menyimpan query id: ${error.message}`);
        await ctx.reply('❌ Gagal menyimpan query id');
    }
});

bot.command('ck', async (ctx) => {
    const user_id = ctx.message.from.id;
    const query_id = user_data[user_id];

    if (query_id) {
        await ctx.reply(`Query id di akun mu adalah ${query_id}`);
    } else {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
    }
});

bot.command('run', async (ctx) => {
    const user_id = ctx.message.from.id;
    const query_id = user_data[user_id];
    const chat_id = ctx.chat.id; 

    if (!query_id) {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
        return;
    }

    try {
        exec(`python3 hamster.py -f "data/${user_id}.txt" -u y -m 10000000 -c y -a n -t n -d n -l n -ci ${chat_id}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`❌ Gagal menjalankan bot: ${error.message}`);
                ctx.reply(`❌ Gagal menjalankan bot: ${error.message}`);
                return;
            }
            if (stderr) {
                console.error(`Error output: ${stderr}`);
                ctx.reply(`❌ Gagal menjalankan bot: ${stderr}`);
                return;
            }

            console.log(`stdout: ${stdout}`);

            user_status[user_id] = stdout;
            ctx.reply(stdout);
        });
    } catch (e) {
        console.error(`Exception: ${e}`);
        ctx.reply(`Exception: ${e}`);
    }
});

bot.command('dlt', async (ctx) => {
    const user_id = ctx.message.from.id;

    try {
        fs.unlinkSync(`${dataPath}${user_id}.txt`);
        delete user_data[user_id];
        await ctx.reply('✅ Query id berhasil dihapus');
    } catch (error) {
        console.error(`❌ Gagal menghapus query id: ${error.message}`);
        await ctx.reply('❌ Gagal menghapus query id');
    }
});

bot.launch();
