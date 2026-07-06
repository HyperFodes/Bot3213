import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from flask import Flask, request

# ==========================================
# 1. CONFIGURAÇÕES INICIAIS
# ==========================================
TOKEN_BOT = "8681521626:AAFdIzvJ0ZoRVBb5Z_CdPniMgD2W72EwK-E"
SEU_ID_TELEGRAM = 7665685378
ID_GRUPO_VIP = -1004484883734

# File IDs novos e corretos extraídos do Telegram
LINK_BANNER_BOAS_VINDAS = "AgACAgEAAxkBAAMgaktGeMTfS0zM93iIEA3LqTE4k14AAvMLaxtTCFhGGoTrU4w9Lz4BAAMCAAN5AAM8BA"
LINK_QRCODE_PIX = "AgACAgEAAxkBAAMyaktHg1j63LE0kJCweSYHBWpvJKkAAuELaxttkFhGSUoUR9GTUYEBAAMCAAN4AAM8BA"

# Suas carteiras oficiais configuradas
CARTEIRA_BTC = "bc1qv0vt52xa356n5sfz6ayq9enfr77teemr4htqtf"
CARTEIRA_ETH = "0x68c4a8312b50D1506619314b29981Fe3731035E0"
CARTEIRA_LTC = "ltc1qpcuzhk48n0udpcv64n5x8fjapf505j2qj3ketf"
CARTEIRA_USDT = "0x1e75616b576d7f66f0cd8176ee2f70bef1fe8ddb"

bot = telebot.TeleBot(TOKEN_BOT, threaded=False)
app = Flask(__name__)

# Dicionário para rastrear quem está comprando o quê (Importante para receber o comprovante)
usuarios_comprando = {}

# ==========================================
# 2. COMANDOS DO BOT
# ==========================================

# --- MENSAGEM DE BOAS VINDAS COM BANNER BILÍNGUE (/start) ---
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    try:
        print("[BOT] 📥 Comando /start entrou na função com sucesso!", flush=True)
        idioma_usuario = message.from_user.language_code
        markup = InlineKeyboardMarkup(row_width=1)
        
        if idioma_usuario and 'pt' in idioma_usuario:
            texto = "👋 Bem-vindo ao bot oficial do Criador!\n\nGaranta seu *ACESSO VITALÍCIO* (pague uma vez e fique para sempre) aos melhores conteúdos e arquivos de Minecraft escolhendo sua forma de pagamento:"
            btn_pix = InlineKeyboardButton("🇧🇷 PIX (R$ 30,00)", callback_data="menu_pix")
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            markup.add(btn_pix, btn_stars, btn_crypto)
        else:
            texto = "👋 Welcome to the Creator's official bot!\n\nGet your *LIFETIME ACCESS* (pay once, stay forever) to the best Minecraft content and files by choosing your payment method:"
            btn_stars = InlineKeyboardButton("⭐ Telegram Stars (900 Stars)", callback_data="stars_900")
            btn_crypto = InlineKeyboardButton("🪙 Crypto Dollars ($ 5.00)", callback_data="menu_crypto")
            btn_pix = InlineKeyboardButton("🇧🇷 Brazilian PIX (R$ 30,00)", callback_data="menu_pix")
            markup.add(btn_stars, btn_crypto, btn_pix)
        
        bot.send_photo(message.chat.id, LINK_BANNER_BOAS_VINDAS, caption=texto, reply_markup=markup, parse_mode="Markdown")
        print("[BOT] ✅ Foto enviada com sucesso!", flush=True)
        
    except Exception as e:
        print(f"[ERRO NO START] ❌ Falha ao enviar foto. Enviando texto. Erro: {e}", flush=True)
        bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")


# --- GERENCIAMENTO DOS CLIQUES NOS BOTÕES ---
@bot.callback_query_handler(func=lambda call: True)
def escutar_botoes(call):
    chat_id = call.message.chat.id

    if call.data == "menu_pix":
        usuarios_comprando[chat_id] = "PIX - R$ 30"
        texto_instrucao = (
            f"⚡ *Plano Vitalício de R$ 30 selecionado!*\n\n"
            f"1️⃣ Escaneie o QR Code acima no app do seu banco.\n"
            f"2️⃣ *ATENÇÃO:* Digite manualmente o valor exato de: *R$ 30,00*\n\n"
            f"⚠️ *Se você digitar um valor diferente, seu acesso não será aprovado.*\n\n"
            f"👇 Após fazer o pagamento, envie a *FOTO DO COMPROVANTE* aqui no chat para liberação imediata!\n\n"
            f"ℹ️ Precisa de ajuda? Fale com o suporte: @HardHandsG"
        )
        try:
            bot.send_photo(chat_id, LINK_QRCODE_PIX, caption=texto_instrucao, parse_mode="Markdown")
        except Exception as e:
            print(f"[ERRO NO PIX] ❌ Falha ao enviar QR Code. Erro: {e}", flush=True)
            bot.send_message(chat_id, texto_instrucao, parse_mode="Markdown")

    elif call.data == "stars_900":
        bot.send_invoice(
            chat_id=chat_id,
            title="Lifetime VIP — 900 Stars",
            description="Permanent access to the Creator's Minecraft VIP group.",
            invoice_payload="vip_stars_900",
            provider_token="",
            currency="XTR",
            prices=[LabeledPrice(label="Stars", amount=900)]
        )

    elif call.data == "menu_crypto":
        usuarios_comprando[chat_id] = "Crypto - $ 5.00"
        texto_crypto = (
            f"🪙 *Lifetime VIP Access — Crypto Dollars*\n\n"
            f"Value: *$ 5.00 USD*\n\n"
            f"Send the exact amount to one of the wallets below (tap to copy):\n\n"
            f"🔹 *USDT (Network: BEP-20 / BSC):*\n`{CARTEIRA_USDT}`\n\n"
            f"🔸 *LTC (Litecoin - Recommended/Low Fees):*\n`{CARTEIRA_LTC}`\n\n"
            f"🔹 *BTC (Bitcoin):*\n`{CARTEIRA_BTC}`\n\n"
            f"🔸 *ETH (Ethereum):*\n`{CARTEIRA_ETH}`\n\n"
            f"👇 After sending the payment, please upload the *TRANSACTION RECEIPT/SCREENSHOT* here for manual approval!\n\n"
            f"ℹ️ Need help? Contact support: @HardHandsG"
        )
        bot.send_message(chat_id, texto_crypto, parse_mode="Markdown")

    elif call.data.startswith("aprovar_"):
        bot.answer_callback_query(call.id) # Evita spam de repetição do clique
        id_cliente = call.data.split("_")[1]
        try:
            link_grupo = bot.create_chat_invite_link(ID_GRUPO_VIP, member_limit=1)
            bot.send_message(id_cliente, f"✅ Seu pagamento foi aprovado! / Your payment has been approved!\n\nClique no link abaixo para entrar no grupo VIP permanentemente:\nClick the link below to join the VIP group permanently:\n\n{link_grupo.invite_link}")
            bot.edit_message_caption("✅ Cliente aprovado e link permanente enviado!", chat_id=chat_id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(chat_id, f"Erro ao gerar link. Verifique se o bot é admin do grupo. Erro: {e}")

    elif call.data.startswith("recusar_"):
        bot.answer_callback_query(call.id) # Evita spam de repetição do clique
        id_cliente = call.data.split("_")[1]
        try:
            bot.send_message(id_cliente, "❌ Pagamento recusado / Payment declined.\nSe achar que foi um erro, entre em contato com o suporte: @HardHandsG")
            bot.edit_message_caption("❌ Pagamento recusado.", chat_id=chat_id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(chat_id, f"Erro ao processar recusa. Erro: {e}")


# --- 3. RECEBER COMPROVANTE ---
@bot.message_handler(content_types=['photo'])
def receber_comprovante(message):
    chat_id = message.chat.id
    if chat_id in usuarios_comprando:
        forma_pagamento = usuarios_comprando[chat_id]
        markup_admin = InlineKeyboardMarkup()
        markup_admin.add(
            InlineKeyboardButton("✅ Aprovar", callback_data=f"aprovar_{chat_id}"),
            InlineKeyboardButton("❌ Recusar", callback_data=f"recusar_{chat_id}")
        )
        bot.send_photo(
            SEU_ID_TELEGRAM, 
            message.photo[-1].file_id, 
            caption=f"🔔 NOVO COMPROVANTE RECEBIDO!\n\nUsuário: @{message.from_user.username} (ID: {chat_id})\nMétodo escolhido: {forma_pagamento}\n\nConfira sua carteira/banco e decida abaixo:", 
            reply_markup=markup_admin
        )
        bot.send_message(chat_id, "⏳ Comprovante recebido! Aguarde a verificação.\n⏳ Receipt received! Please wait for verification.")
        del usuarios_comprando[chat_id]


# --- 4. ENTREGA VIA STARS ---
@bot.pre_checkout_query_handler(func=lambda query: True)
def processar_pre_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def pagamento_stars_sucesso(message):
    chat_id = message.chat.id
    link_grupo = bot.create_chat_invite_link(ID_GRUPO_VIP, member_limit=1)
    bot.send_message(chat_id, f"🎉 Thank you for your payment in Stars! Your lifetime access is granted.\n\nClick here to join permanently: {link_grupo.invite_link}")


# ==========================================
# 5. ROTAS DO SERVIDOR WEB (RENDER)
# ==========================================
@app.route('/' + TOKEN_BOT, methods=['POST'])
def getMessage():
    try:
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    except Exception as server_error:
        print(f"[ERRO NO SERVIDOR] ❌ Falha na rota principal: {server_error}", flush=True)
        return "Erro", 500

@app.route("/")
def webhook():
    bot.remove_webhook()
    url_render = "https://bot3213.onrender.com" 
    bot.set_webhook(url=f"{url_render}/{TOKEN_BOT}")
    return "Webhook configurado com sucesso!", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host="0.0.0.0", port=port)
