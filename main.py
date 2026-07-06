# --- 5. INFRAESTRUTURA WEB ---
@app.route('/' + TOKEN_BOT, methods=['POST'])
def getMessage():
    try:
        json_string = request.get_data().decode('utf-8')
        print("\n[FLASK] 🌐 Nova requisição interceptada vinda do Telegram!", flush=True)
        update = telebot.types.Update.de_json(json_string)
        
        if update.message:
            print(f"[FLASK] 💬 Mensagem de texto lida: '{update.message.text}' do usuário: {update.message.chat.id}", flush=True)
            
        bot.process_new_updates([update])
        return "!", 200
    except Exception as server_error:
        print(f"[ERRO NO SERVIDOR] ❌ Falha na rota principal: {server_error}", flush=True)
        return "Erro", 500

@app.route("/")
def webhook():
    return "Bot está vivo!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
