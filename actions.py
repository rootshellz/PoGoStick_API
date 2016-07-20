# Imports
from datetime import datetime

# Project Imports
import api


def enumerate_profile():
    print("[.] Attempting to retrieve your profile")
    profile = api.get_profile()
    profile = profile.payload[0].profile
    print("[.] Successfully retrieved your profile")

    # Profile Definitions
    # account_creation_time = profile.creation_time
    # username = profile.username
    # tutorial = profile.tutorial
    # avatar = profile.avatar
    # poke_storage = profile.poke_storage
    # item_storage = profile.item_storage
    # daily_bonus = profile.daily_bonus
    # unknown12 = profile.unknown12
    # unknown13 = profile.unknown13
    # pokecoin = profile.currency[0].amount
    # stardust = profile.currency[1].amount

    print("    [.] Username: %s" % profile.username)
    start_date = datetime.fromtimestamp(int(profile.creation_time)/1000)
    print("    [.] Start Date: %s" % start_date.strftime('%Y-%m-%d %H:%M:%S'))
    print("    [.] Pokemon Storage: %s" % profile.poke_storage)
    print("    [.] Item Storage: %s" % profile.item_storage)
    print("    [.] Pokecoins: %s" % profile.currency[0].amount)
    print("    [.] Stardust: %s" % profile.currency[1].amount)
