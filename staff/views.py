from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db import models
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .models import Staff, VerificationLog
from .utils import get_client_ip
from .forms import StaffForm

@require_http_methods(["GET"])
def home(request):
    """Landing page"""
    return render(request, 'staff/home.html')

@login_required
@require_http_methods(["GET"])
def staff_list(request):
    """List all staff with search"""
    query = request.GET.get('q', '')
    department = request.GET.get('department', '')
    status = request.GET.get('status', '')
    
    staff_queryset = Staff.objects.all()
    
    if query:
        staff_queryset = staff_queryset.filter(
            models.Q(staff_id__icontains=query) |
            models.Q(first_name__icontains=query) |
            models.Q(last_name__icontains=query) |
            models.Q(email__icontains=query)
        )
    
    if department:
        staff_queryset = staff_queryset.filter(department=department)
    
    if status:
        staff_queryset = staff_queryset.filter(status=status)
    
    paginator = Paginator(staff_queryset, 20)
    page_number = request.GET.get('page')
    staff_page = paginator.get_page(page_number)
    
    context = {
        'staff_list': staff_page,
        'query': query,
        'department': department,
        'status': status,
        'departments': Staff.DEPARTMENT_CHOICES,
        'statuses': Staff.STATUS_CHOICES,
    }
    
    return render(request, 'staff/staff_list.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def staff_create(request):
    """Create new staff"""
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff {staff.get_full_name()} created successfully!')
            return redirect('staff:staff_detail', uuid=staff.uuid)
    else:
        form = StaffForm()
    
    return render(request, 'staff/staff_form.html', {'form': form, 'action': 'Create'})

@login_required
@require_http_methods(["GET", "POST"])
def staff_edit(request, uuid):
    """Edit existing staff"""
    staff = get_object_or_404(Staff, uuid=uuid)
    
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            staff = form.save()
            messages.success(request, f'Staff {staff.get_full_name()} updated successfully!')
            return redirect('staff:staff_detail', uuid=staff.uuid)
    else:
        form = StaffForm(instance=staff)
    
    return render(request, 'staff/staff_form.html', {'form': form, 'action': 'Edit', 'staff': staff})

@login_required
@require_http_methods(["GET"])
def staff_detail(request, uuid):
    """View staff details"""
    staff = get_object_or_404(Staff, uuid=uuid)
    recent_verifications = staff.verification_logs.all()[:10]
        # Log verification attempt
    verification_log = VerificationLog.objects.create(
        staff=staff,
        verified_by=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )

    context = {
        'staff': staff,
        'recent_verifications': recent_verifications,
        'verification_log': verification_log,

    }
    
    return render(request, 'staff/staff_detail.html', context)

@never_cache
@require_http_methods(["GET"])
def verify_staff(request, uuid):
    """Verify staff by UUID from QR code"""
    staff = get_object_or_404(Staff, uuid=uuid)
    
    # Log verification attempt
    verification_log = VerificationLog.objects.create(
        staff=staff,
        verified_by=request.user if request.user.is_authenticated else None,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
    )
    
    context = {
        'staff': staff,
        'is_valid': staff.status == 'active' and not staff.is_expired(),
        'verification_log': verification_log,
    }
    
    return render(request, 'staff/verify.html', context)

@require_http_methods(["GET"])
def print_card(request, uuid):
    """Generate printable ID card with QR code"""
    staff = get_object_or_404(Staff, uuid=uuid)
    
    context = {
        'staff': staff,
    }
    
    return render(request, 'staff/print_card.html', context)

@login_required
@require_http_methods(["GET"])
def download_qr_sticker(request, uuid):
    """Download QR code sticker as PDF"""
    staff = get_object_or_404(Staff, uuid=uuid)
    
    html = render_to_string('staff/qr_sticker_pdf.html', {
        'staff': staff,
        'request': request,
    })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="qr_sticker_{staff.staff_id}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('PDF generation error', status=500)
    
    return response
