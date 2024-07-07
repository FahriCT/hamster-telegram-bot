const { Telegraf } = require('telegraf');
const { exec } = require('child_process');
const fs = require('fs');
const BOT_TOKEN = fs.readFileSync('token.txt', 'utf8').trim();
const bot = new Telegraf(BOT_TOKEN);
const dataPath = 'data/';
const user_data = {};
const user_status = {};
const user_settings = {};

bot.command('start', async (ctx) => {
    await ctx.reply(`
        BOT FAHRI HAMSTER\n
        1. /in <query_id> - Input Query ID ✍️\n
        2. /ck = Cek query id mu 🔍\n
        3. /run = Jalankan Bot 🚀\n
        4. /r = Refresh status bot mu 🔄\n
        5. /dlt = Hapus query id ❌\n
    `);
});

bot.command('in', async (ctx) => {
    const query_id = ctx.message.text.split(' ')[1];
    const user_id = ctx.message.from.id;

    try {
        fs.writeFileSync(`${dataPath}${user_id}.txt`, query_id.trim());
        user_data[user_id] = query_id.trim();
        await ctx.reply('Query id berhasil disimpan');
    } catch (error) {
        console.error(`Gagal menyimpan query id: ${error.message}`);
        await ctx.reply('Gagal menyimpan query id');
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
    const settings = user_settings[user_id] || {};

    if (!query_id) {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
        return;
    }

    let args = `${query_id}`;
    for (const [key, value] of Object.entries(settings)) {
        args += ` -${key} ${value}`;
    }

    const command = `python3 hamster.py -f "${dataPath}${user_id}.txt" -u y -m 10000000 -c y -a n -t n -d n -l n`;

    try {
        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error(`Gagal menjalankan bot: ${error.message}`);
                ctx.reply(`Gagal menjalankan bot: ${error.message}`);
                return;
            }
            if (stderr) {
                console.error(`Error output: ${stderr}`);
                ctx.reply(`Gagal menjalankan bot: ${stderr}`);
                return;
            }

            const output = stdout;
            const response = "Bot berjalan\n" +
                `[ Level 📈 ] : ${extractValue(output, "Level")}\n` +
                `[ Total Earned 💰 ] : ${extractValue(output, "Total Earned")}\n` +
                `[ Coin 🪙 ] : ${extractValue(output, "Coin")}\n` +
                `[ Energy 🔋 ] : ${extractValue(output, "Energy")}\n` +
                `[ Level Energy ⚡ ] : ${extractValue(output, "Level Energy")}\n` +
                `[ Level Tap  👆 ] : ${extractValue(output, "Level Tap")}\n` +
                `[ Exchange 🔄 ] : ${extractValue(output, "Exchange")}\n`;

            user_status[user_id] = response;
            ctx.reply(response);
        });
    } catch (e) {
        console.error(`Exception: ${e}`);
        ctx.reply(`Exception: ${e}`);
    }
});

bot.command('r', async (ctx) => {
    const user_id = ctx.message.from.id;
    const status = user_status[user_id];

    if (status) {
        await ctx.reply(`Ini adalah status bot mu saat ini:\n${status}`);
    } else {
        await ctx.reply('Anda belum menjalankan bot. Gunakan perintah /run untuk menjalankan.');
    }
});

bot.command('dlt', async (ctx) => {
    const user_id = ctx.message.from.id;

    try {
        fs.unlinkSync(`${dataPath}${user_id}.txt`);
        delete user_data[user_id];
        delete user_settings[user_id];
        await ctx.reply('Query id berhasil dihapus');
    } catch (error) {
        console.error(`Gagal menghapus query id: ${error.message}`);
        await ctx.reply('Gagal menghapus query id');
    }
});


function extractValue(output, label) {
    const match = output.match(new RegExp(`\\[ ${label} \\] : (\\d+)`));
    return match ? match[1] : 'N/A';
}

bot.launch();
