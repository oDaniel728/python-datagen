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
        token = str(value)
        token = ''.join(ch if ch.isalnum() else '_' for ch in token)
        while '__' in token:
            token = token.replace('__', '_')
        token = token.strip('_')
        return token if token else "value"

    @staticmethod
    def id_suffix(*parts: object) -> str:
        return '_'.join(PredicateBuilderUtil.safe_token(part) for part in parts)
