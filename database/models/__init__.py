from database.models.creation_process import CreatedTimePoints
from database.models.notifications import Notifications, SendTime, ChatToSend
from database.models.users import Users

active_models = [
    Users,
    ChatToSend,

    Notifications,
    SendTime,

    CreatedTimePoints,
]
