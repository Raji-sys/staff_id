import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings
import os

def generate_qr_code(staff, save_to_file=True):
    """Generate QR code for staff verification URL"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Full URL for QR code
    site_domain = settings.SITE_DOMAIN if hasattr(settings, 'SITE_DOMAIN') else settings.ALLOWED_HOSTS[0]
    protocol = "https" if not settings.DEBUG else "http"
    verification_url = f"{protocol}://{site_domain}{staff.get_verification_url()}"
    
    qr.add_data(verification_url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    if save_to_file:
        # Save to media directory
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        os.makedirs(qr_dir, exist_ok=True)
        qr_path = os.path.join(qr_dir, f'qr_{staff.uuid}.png')
        img.save(qr_path)
        return f'qr_codes/qr_{staff.uuid}.png'
    else:
        # Return as BytesIO for immediate use
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        return buffer

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip