from datagen.types.util.min import Range


class PredicateBuilderUtil():
    @staticmethod
    def range_to_dict(value: Range | None) -> dict | None:
        if value is None:
            return None
        return {
            "min": value.start,
            "max": value.end
        }

    @staticmethod
    def to_dict(value):
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            return to_dict()
        return value

    @staticmethod
    def safe_token(value: object) -> str:
        replmap = {
            "enchantment": "ench",
            "minecraft": "mc",
            "type": "typ",
            "linear_": "ln",
            "base": "bs",
            "per_": "p",
            "level": "lvl",
            "above": "abv",
            "first": "fs",
            "000000": "m",
            "000": "k",
            "true": "1b",
            "false": "0b",
            "expected": "xpctd",
            "projectile": "prjctl",
            "player": "plr",
            "source": "src",
            "entity": "ntt",
            "oo": "o",
            "light": "lgt"
        }
        token = str(value)
        token = ''.join(ch if ch.isalnum() else '_' for ch in token)
        token = token.strip('_')
        for k in replmap:
            v = replmap[k]
            it = 0
            while k in token:
                it += 1
                token = token.replace(k, v)
                if it > 50: break
        while '__' in token:
            token = token.replace('__', '_')
        return (token if token else "value")

    @staticmethod
    def id_suffix(*parts: object) -> str:
        return '_'.join(PredicateBuilderUtil.safe_token(part) for part in parts)
