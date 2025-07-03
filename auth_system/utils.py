from django.core.mail import send_mail
import random
from django.core.cache import cache
from LeaseTool.settings import EMAIL_HOST_USER
def send_OTP(email, name):
    try:
        otp = str(random.randint(100000, 999999))
        print(f"[DEBUG] OTP for {email}: {otp}")

        message = f"""
        Hi {name},

        Welcome to LesserKit.
        Your OTP for verification is: {otp}

        Please use it within 5 minutes.
        """

        send_mail(
            subject='OTP Verification - LesserKit',
            message=message,
            from_email= EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        cache.set(f"otp_{email}", otp, timeout=300)  # 5 minutes
        return True
    except Exception as e:
        print(f"[ERROR] Failed to send OTP to {email}: {str(e)}")
        return False
