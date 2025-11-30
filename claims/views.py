from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from items.models import Item
from .models import Claim
from .forms import ClaimForm

# Create your views here.

#Submission
@login_required
def submit_claim(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.status != 'available':
        messages.error(request, 'This item is no longer available for claims.')
        return redirect('item_detail', pk=item_pk)
    
    existing_claim = Claim.objects.filter(item=item, claimant=request.user, status='pending').first()
    if existing_claim:
        messages.warning(request, 'You already have a pending claim for this item.')
        return redirect('my_claims')
    
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.item = item
            claim.claimant = request.user
            claim.save()
            messages.success(request, f'Your {claim.get_claim_type_display().lower()} has been submitted successfully!')
            return redirect('my_claims')
    else:
        form = ClaimForm()

    return render(request, 'claims/submit_claim.html', {'form': form, 'item': item})

#View own cliams
@login_required
def my_claims(request):
    claims = Claim.objects.filter(claimant=request.user)
    return render(request, 'claims/my_claims.html', {'claims': claims})

#Admin view to see all claims
@login_required
def admin_claims(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    #Filtering options
    status_filter = request.GET.get('status', 'pending')
    if status_filter == 'all':
        claims = Claim.objects.all()
    else:
        claims = Claim.objects.filter(status=status_filter)

    return render(request, 'claims/admin_claims.html', {'claims': claims, 'current_filter': status_filter})

#Admin view to review claim detail
@login_required
def review_claim(request, claim_pk):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    claim = get_object_or_404(Claim, pk=claim_pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')

        if action == 'approve':
            claim.status = 'approved'
            claim.item.status = 'claimed'
            claim.item.save()
            messages.success(request, f'Claim approved for {claim.item.name}.')
        elif action == 'reject':
            claim.status = 'rejected'
            messages.success(request, f'Claim rejected for {claim.item.name}.')
        elif action == 'complete':
            claim.status = 'completed'
            claim.item.status = 'returned'
            claim.item.save()
            messages.success(request, f'Item {claim.item.name} marked as returned.')

        claim.reviewed_by = request.user
        claim.reviewed_at = timezone.now()
        claim.admin_notes = admin_notes
        claim.save()

        return redirect('admin_claims')
    
    return render(request, 'claims/review_claim.html', {'claim': claim})