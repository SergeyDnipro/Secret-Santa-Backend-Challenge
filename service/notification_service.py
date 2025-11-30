def send_notification_worker(bot, msg_queue):
    """ Background thread for sending results to players"""
    while True:
        user_chat_id, gift_to = msg_queue.get()
        try:
            bot.send_message(user_chat_id, f"Your gift receiver -> {gift_to}")
        except Exception as e:
            print("Send error: ", e)
        msg_queue.task_done()