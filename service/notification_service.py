def send_notification(bot, msg_queue):
    while True:
        user_chat_id, gift_to = msg_queue.get()
        try:
            bot.send_message(user_chat_id, f"You Secret Santa to: {gift_to}")
        except Exception as e:
            print("Send error: ", e)
        msg_queue.task_done()