

def send_tg_notification(user_id: int, msg: str) -> None:
    pass


def notify_on_task_failure(admin_id: int, users: tuple) -> None:
    """Send notification message on task failure"""

    send_tg_notification(admin_id, '')
    for user_id in users:
        send_tg_notification(user_id, '')
