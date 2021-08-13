
# * made this file to make database functions  that will work upon the mail


def check_if_key_is_valid(ids):
    from datetime import datetime, timedelta, timezone
    for id in ids.objects.all():
        # print(ids.objects.all())
        if datetime.now(tz=timezone.utc) - id.time_created > timedelta(hours=2):
            p = id.unique_id
            pk = id.pk
            id.delete()
            return False
        return True
