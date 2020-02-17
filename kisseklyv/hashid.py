from hashids import Hashids
import config


HASH_ID_PADDING = 1000  # lägg till id för att få längre strängar


def get_hashid_from_id(id: int) -> str:
    id += HASH_ID_PADDING
    cfg = config.Config()
    hashids = Hashids(salt=cfg.HASHIDS_SALT)
    return hashids.encode(id)

def get_id_from_hashid(hashid: str) -> int:
    cfg = config.Config()
    hashids = Hashids(salt=cfg.HASHIDS_SALT)
    return hashids.decode(hashid)[0] - HASH_ID_PADDING
