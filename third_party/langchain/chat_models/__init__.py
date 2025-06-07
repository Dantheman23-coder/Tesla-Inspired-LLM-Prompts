class ChatOpenAI:
    def __init__(self, *_, **__):
        pass
    def __call__(self, x):
        class R:
            def __init__(self, content):
                self.content = content
        return R('stub')
