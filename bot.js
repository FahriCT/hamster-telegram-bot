const { Telegraf } = require('telegraf');
const { exec } = require('child_process');

// Token bot Anda
const BOT_TOKEN = 'YOUR_BOT_TOKEN';
const bot = new Telegraf(BOT_TOKEN);

// Dictionary untuk menyimpan query_id user
const user_data = {};

// Command handler untuk /start
bot.command('start', async (ctx) => {
    await ctx.reply(`
        BOT HAMSTER\n
        1. /in <query_id> = Input Query id\n
        2. /ck = Cek query id mu\n
        3. /run = Jalankan Bot\n
        4. /r = Refresh status bot mu
    `);
});

// Command handler untuk /in <query_id>
bot.command('in', async (ctx) => {
    const query_id = ctx.message.text.split(' ')[1];
    const user_id = ctx.message.from.id;
    user_data[user_id] = query_id;
    await ctx.reply('Query id berhasil disimpan');
});

// Command handler untuk /ck
bot.command('ck', async (ctx) => {
    const user_id = ctx.message.from.id;
    const query_id = user_data[user_id];
    
    if (query_id) {
        await ctx.reply(`Query id di akun mu adalah ${query_id}`);
    } else {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
    }
});

// Command handler untuk /run
bot.command('run', async (ctx) => {
    const user_id = ctx.message.from.id;
    const query_id = user_data[user_id];
    
    if (!query_id) {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
        return;
    }
    
    try {
        exec(`python3 hamster.py ${query_id}`, (error, stdout, stderr) => {
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
                `[ Level ] : ${extractValue(output, "Level")}\n` +
                `[ Total Earned ] : ${extractValue(output, "Total Earned")}\n` +
                `[ Coin ] : ${extractValue(output, "Coin")}\n` +
                `[ Energy ] : ${extractValue(output, "Energy")}\n` +
                `[ Level Energy ] : ${extractValue(output, "Level Energy")}\n` +
                `[ Level Tap ] : ${extractValue(output, "Level Tap")}\n` +
                `[ Exchange ] : ${extractValue(output, "Exchange")}\n`;

            ctx.reply(response);
        });
    } catch (e) {
        console.error(`Exception: ${e}`);
        ctx.reply(`Exception: ${e}`);
    }
});

// Command handler untuk /r


// Function untuk mengekstrak nilai dari output
function extractValue(output, label) {
    const match = output.match(new RegExp(`\\[ ${label} \\] : (\\d+)`));
    return match ? match[1] : 'N/A';
}

// Mulai bot
bot.launch();
