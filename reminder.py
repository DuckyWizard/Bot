from telegram.ext import Updater, CommandHandler
import datetime

# Armazenar a mensagem personalizada
custom_message = 'BIP BIP BIP! Aqui está o seu lembrete.'

def start(update, context):
    update.message.reply_text('Olá! Eu sou o seu bot de lembretes. Use /set <segundos> <repetir> <mensagem> para configurar um lembrete.')

def set_reminder(update, context):
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        repeat = int(context.args[1])

        if due < 0:
            update.message.reply_text('Desculpe, não consigo voltar no tempo!')
            return

        # Adicionar trabalho
        reminder_message = ' '.join(context.args[2:])
        context.job_queue.run_repeating(alarm, due, context=chat_id)

        text = 'Lembrete configurado!'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Uso: /set <segundos> <repetir> <mensagem>')

def alarm(context):
    job = context.job
    context.bot.send_message(job.context, text=custom_message)

def customize(update, context):
    global custom_message
    custom_message = ' '.join(context.args)
    update.message.reply_text('Mensagem de lembrete personalizada!')

def main():
    updater = Updater("5736615218:AAEdcz7eYtaTuwnwRc8f5dooTOp7xO1bk3o", use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("set", set_reminder, pass_args=True, pass_job_queue=True))
    dp.add_handler(CommandHandler("customize", customize, pass_args=True))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
