import re
    
class Converter:
    @staticmethod
    def str_to_float(value, default=0.0, decimals=None):
        try:
            num = float(value)
            if decimals is not None:
                return round(num, decimals)
            return num
        except (ValueError, TypeError):
            return default
           
    @staticmethod
    def format_float_decimal(value, decimal=2):
        try:
            formatted = f"{float(value):.{decimal}f}"
            return formatted
        except (ValueError, TypeError):
            return value
    
    @staticmethod   
    def is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None