class ReportSingleton:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(
                ReportSingleton, cls
            ).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if hasattr(self, 'initialized'):
            return

        self.value = list()
        self.initialized = True

    def get_value(self):
        return self.value

    def set_value(self, v):
        self.value.append(v)
