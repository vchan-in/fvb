import datetime

def convert_to_unix_epoch(user_input):
    user_datetime = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
    unix_epoch = int(user_datetime.timestamp())
    return unix_epoch

def convert_to_utc(user_input):
    user_datetime = datetime.datetime.strptime(user_input, "%Y-%m-%d %H:%M")
    # utc = user_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    return user_datetime