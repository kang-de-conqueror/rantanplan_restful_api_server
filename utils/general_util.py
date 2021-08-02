from random import random


class GeneralUtil:
    ALPHA_NUMERIC_STRING = "123456789abcdefghijklmnopqrstuvwyxz"

    @staticmethod
    def generate_32_chars_string():
        result = ""
        for i in range(len(GeneralUtil.ALPHA_NUMERIC_STRING)):
            result += GeneralUtil.ALPHA_NUMERIC_STRING[int(
                random() * len(GeneralUtil.ALPHA_NUMERIC_STRING))]
        return result
