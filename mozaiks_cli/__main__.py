import json
from datetime import date, datetime

_old_default = json.JSONEncoder.default
json.JSONEncoder.default = lambda self, obj: obj.isoformat() if isinstance(obj, (date, datetime)) else _old_default(self, obj)

from mozaiks_cli.main import main


if __name__ == "__main__":
    main()  