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
def submit_claim(request, item_pk, claim_type=None):
    item = get_object_or_404(Item, pk=item_pk)

    # Prevent the user who reported the item from claiming it
    if request.user == item.submitted_by:
        messages.error(request, 'You cannot claim an item that you reported.')
        return redirect('item_detail', pk=item_pk)

    # Only allow claims on unclaimed items or items with rejected claims
    if item.status not in ['unclaimed', 'rejected']:
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
        # Pre-select claim type if provided
        if claim_type in ['claim', 'inquiry']:
            form = ClaimForm(initial={'claim_type': claim_type})
        else:
            form = ClaimForm()

    return render(request, 'claims/submit_claim.html', {'form': form, 'item': item, 'claim_type': claim_type})

#View own cliams
@login_required
def my_claims(request):
    claims = Claim.objects.filter(claimant=request.user)
    return render(request, 'claims/my_claims.html', {'claims': claims})

#Admin view to see all claims
@login_required
def admin_claims(request):
    if not (request.user.is_staff or request.user.user_type == 'teacher'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    #Filtering options
    status_filter = request.GET.get('status', 'pending_approval')

    # Get items pending approval
    pending_approval_items = Item.objects.filter(status='reported').order_by('-created_at')

    # Get claims based on filter
    if status_filter == 'pending_approval':
        claims = []  # No claims to show on this tab
    elif status_filter == 'all':
        claims = Claim.objects.all()
    else:
        claims = Claim.objects.filter(status=status_filter)

    # Calculate counts for each category
    counts = {
        'pending_approval': Item.objects.filter(status='reported').count(),
        'pending': Claim.objects.filter(status='pending').count(),
        'approved': Claim.objects.filter(status='approved').count(),
        'rejected': Claim.objects.filter(status='rejected').count(),
        'completed': Claim.objects.filter(status='completed').count(),
        'all': Claim.objects.count(),
        'all_actionable': (
            Item.objects.filter(status='reported').count() +
            Claim.objects.filter(status__in=['pending', 'approved', 'rejected']).count()
        )
    }

    return render(request, 'claims/admin_claims.html', {
        'claims': claims,
        'current_filter': status_filter,
        'pending_approval_items': pending_approval_items,
        'counts': counts
    })

#Admin view to review claim detail
@login_required
def review_claim(request, claim_pk):
    if not (request.user.is_staff or request.user.user_type == 'teacher'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    claim = get_object_or_404(Claim, pk=claim_pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')

        if action == 'approve':
            claim.status = 'approved'
            claim.item.status = 'verified'
            claim.item.verified_date = timezone.now()  # Start 60-day countdown
            claim.item.save()
            messages.success(request, f'Claim approved and verified for {claim.item.name}. 60-day countdown started.')
        elif action == 'reject':
            claim.status = 'rejected'
            claim.item.status = 'rejected'
            claim.item.save()
            messages.success(request, f'Claim rejected for {claim.item.name}. Item is now available for new claims.')
        elif action == 'complete':
            # NEW WORKFLOW: Must verify claim first before marking as returned
            if claim.status != 'approved':
                messages.error(request, 'You must verify the claim first before marking the item as returned.')
                return redirect('review_claim', claim_pk=claim_pk)
            
            claim.status = 'completed'
            claim.item.status = 'returned'
            claim.item.returned_to = claim.claimant
            claim.item.save()
            messages.success(request, f'Item {claim.item.name} marked as returned to {claim.claimant.get_full_name() or claim.claimant.username}.')
        elif action == 'discard':
            discard_reason = request.POST.get('discard_reason_claim', 'Discarded during claim review')
            claim.item.status = 'discarded'
            claim.item.discard_date = timezone.now()
            claim.item.discard_reason = discard_reason
            claim.item.discarded_by = request.user
            claim.item.save()
            messages.success(request, f'Item {claim.item.name} marked as discarded/donated.')
        elif action == 'undo':
            # Undo action - revert to pending state
            previous_item_status = 'unclaimed' if claim.item.status in ['verified', 'rejected'] else claim.item.status
            
            claim.status = 'pending'
            claim.reviewed_by = None
            claim.reviewed_at = None
            claim.admin_notes = admin_notes  # Keep any notes
            
            # Reset item status appropriately
            if claim.item.status in ['verified', 'rejected', 'returned']:
                claim.item.status = 'unclaimed'
                claim.item.returned_to = None
                claim.item.save()
            
            claim.save()
            messages.success(request, f'Action undone. Claim for {claim.item.name} has been reverted to pending status.')
            return redirect('admin_claims')

        claim.reviewed_by = request.user
        claim.reviewed_at = timezone.now()
        claim.admin_notes = admin_notes
        claim.save()

        return redirect('admin_claims')
    
    return render(request, 'claims/review_claim.html', {'claim': claim})