from hashids import Hashids
import config


HASH_ID_PADDING = 1000  # lägg till id för att få längre strängar


def get_hashid_from_id(id: int) -> str:
    try:
        id += HASH_ID_PADDING
        cfg = config.Config()
        hashids = Hashids(salt=cfg.HASHIDS_SALT)
        return hashids.encode(id)
    except Exception:
        print("Error in get_hashid_from_id")
        print(f"id: {id}")
        print(f"Salt: {cfg.HASHIDS_SALT}")
        return None

def get_id_from_hashid(hashid: str) -> int:
    try:
        cfg = config.Config()
        hashids = Hashids(salt=cfg.HASHIDS_SALT)
        return hashids.decode(hashid)[0] - HASH_ID_PADDING
    except Exception:
        print("Error in get_id_from_hashid")
        print(f"hashid: {hashid}")
        print(f"Salt: {cfg.HASHIDS_SALT}")
        return None
