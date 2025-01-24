import time

class ShouqianbaService:
    def __init__(self):
        self.base_url = "https://api.shouqianba.com"
        self.terminal_sn = "your_terminal_sn"
        self.terminal_key = "your_terminal_key"

    def create_payment(self, booking):
        # Generate a unique order number
        order_no = f"BOOKING_{booking.id}_{int(time.time())}"
        
        # Return the QR code directly
        return {
            'qr_code': f"NO.0257426067",  # Your fixed QR code
            'terminal_sn': self.terminal_sn,
            'order_no': order_no
        }