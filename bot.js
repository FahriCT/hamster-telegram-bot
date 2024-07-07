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
        Bot Hamster Kombat \n
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

    if (!query_id) {
        await ctx.reply('Anda belum menginput query id. Gunakan perintah /in <query_id> untuk menginput.');
        return;
    }

    try {
        exec(`python3 hamster.py -f "data/${user_id}.txt" -u y -m 10000000 -c y -a n -t n -d n -l n`, (error, stdout, stderr) => {
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
            const output = stdout;

            const response = [
                "Bot berjalan",
                `[ Level ] : ${extractValue(output, "Level")}`,
                `[ Total Earned ] : ${extractValue(output, "Total Earned")}`,
                `[ Coin ] : ${extractValue(output, "Coin")}`,
                `[ Energy ] : ${extractValue(output, "Energy")}`,
                `[ Level Energy ] : ${extractValue(output, "Level Energy")}`,
                `[ Level Tap ] : ${extractValue(output, "Level Tap")}`,
                `[ Exchange ] : ${extractValue(output, "Exchange")}`,
                `[ Passive Earn ] : ${extractValue(output, "Passive Earn")}`,
                `[ Tap Status ] : ${extractValue(output, "Tap Status")}`,
                `[ Booster ] : ${extractValue(output, "Booster")}`,
                `[ Checkin Daily ] : ${extractValue(output, "Checkin Daily")}`
            ].join('\n');

            user_status[user_id] = response;
            ctx.reply(response);
        });
    } catch (e) {
        console.error(`Exception: ${e}`);
        ctx.reply(`Exception: ${e}`);
    }
});

function extractValue(output, label) {
    const match = output.match(new RegExp(`\\[\\s*${label}\\s*\\]\\s*:\\s*(\\S[^\n]*)`));
    return match ? match[1].trim() : 'N/A';
}

bot.launch();
