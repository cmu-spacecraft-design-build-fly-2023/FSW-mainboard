import exceptions


class Handler:
    def __init__(self, handling_info: dict):
        """
        handling_info: should be a dictionary
            - key: string, method name
            - value: tuple, (handler method, exception to raise)
        """
        self.handlers = handling_info

    def handle_method(self, method):

        def handle(*args, **kwargs):
            if method.__name__ in self.handlers:
                m_handler, m_exception = self.handlers[method.__name__]
                try:
                    return method(*args, **kwargs)
                except Exception as e:
                    if m_handler():
                        try:
                            return method(*args, **kwargs)
                        except Exception as e:
                            raise m_exception(e)
                    raise m_exception(e)
            else:
                raise exceptions.handler_cant_handle_exception(
                    Exception("tried to handle unhandlable method")
                )

        return handle

    def is_handled(self, method):
        return method.__name__ in self.handlers
