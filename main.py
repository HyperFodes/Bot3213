# --- 1. MENSAGEM DE BOAS VINDAS COM BANNER BILÍNGUE (/start) ---
@bot.message_handler(commands=['start'])
def enviar_boas_vindas(message):
    try:
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
        
        # Tenta enviar com a foto
        bot.send_photo(message.chat.id, LINK_BANNER_BOAS_VINDAS, caption=texto, reply_markup=markup, parse_mode="Markdown")
        
    except Exception as e:
        print(f"[ERRO NO START] ❌ Falha ao enviar a foto. Enviando apenas texto. Erro: {e}", flush=True)
        # SE A FOTO FALHAR, ENVIA SÓ O TEXTO E OS BOTÕES PARA O USUÁRIO NÃO FICAR NO VÁCUO
        bot.send_message(message.chat.id, texto, reply_markup=markup, parse_mode="Markdown")
