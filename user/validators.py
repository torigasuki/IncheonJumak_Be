from django.core.exceptions import ValidationError

class MaxFileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(f"파일 크기는 {self.max_size}바이트 이하여야 합니다.")
