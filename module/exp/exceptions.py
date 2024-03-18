class InputTypeError(Exception):
    def __init__(self, expected_type, current_value):
            self.expected_type = expected_type
            self.current_value = current_value
            message = f"正确的类型为 {expected_type}，而当前值为 {current_value}"
            super().__init__(message)