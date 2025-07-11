from django.core.mail import send_mail
import random
from django.core.cache import cache
from LeaseTool.settings import EMAIL_HOST_USER

def send_OTP(email, name):
    try:
        otp = str(random.randint(100000, 999999))
        print(f"[DEBUG] OTP for {email}: {otp}")

        # Properly indented multi-line message
        message = f"""
Hi {name},

Welcome to LeaseTool – your smart solution for managing and renting tools seamlessly.

Your One-Time Password (OTP) for account verification is: {otp}

🔒 This OTP is valid for 5 minutes. Please do not share it with anyone.

With LeaseTool, you can:
✔️ Track your rentals and returns  
✔️ Get real-time availability and updates  
✔️ Manage all tool transactions digitally  

Thank you for choosing LeaseTool.
Let’s build something amazing together!

- Team LeaseTool
"""

        send_mail(
            subject='OTP Verification - LeaseTool',
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        # Cache the OTP with a 5-minute timeout
        cache.set(f"otp_{email}", otp, timeout=300)

        return True

    except Exception as e:
      
        return False
