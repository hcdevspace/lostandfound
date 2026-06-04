from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from items.models import Item
from .models import Claim
from .forms import ClaimForm
from accounts.emails import (
    send_claim_submitted_email,
    send_claim_approved_email,
    send_claim_rejected_email,
    send_claim_completed_email,
    send_item_discarded_email,
    send_item_approved_email,
    send_item_rejected_email,
)
from lostandfound.throttle import rate_limit
from lostandfound.spam_detector import score_claim

# Create your views here.

# Submission
@login_required
@rate_limit(max_requests=10, window_seconds=3600)  # 10 claim submissions per hour
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
            sp_score, sp_reasons = score_claim(claim)
            claim.spam_score = sp_score
            claim.spam_reasons = sp_reasons
            claim.save(update_fields=['spam_score', 'spam_reasons'])
            send_claim_submitted_email(request.user, claim)
            messages.success(request, f'Your {claim.get_claim_type_display().lower()} has been submitted successfully!')
            return redirect('my_claims')
    else:
        # Pre-select claim type if provided
        if claim_type in ['claim', 'inquiry']:
            form = ClaimForm(initial={'claim_type': claim_type})
        else:
            form = ClaimForm()

    return render(request, 'claims/submit_claim.html', {'form': form, 'item': item, 'claim_type': claim_type})

# View own claims
@login_required
def my_claims(request):
    claims = Claim.objects.filter(claimant=request.user)
    return render(request, 'claims/my_claims.html', {'claims': claims})

# Admin view to see all claims
@login_required
def admin_claims(request):
    if not (request.user.is_staff or request.user.user_type == 'teacher'):
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')

    from lostandfound.spam_detector import SPAM_THRESHOLD
    status_filter = request.GET.get('status', 'pending_approval')

    clean_items = Item.objects.filter(status='reported', spam_score__lt=SPAM_THRESHOLD).order_by('-created_at')
    spam_items = Item.objects.filter(status='reported', spam_score__gte=SPAM_THRESHOLD).order_by('-spam_score', '-created_at')
    spam_claims = Claim.objects.filter(status='pending', spam_score__gte=SPAM_THRESHOLD).order_by('-spam_score', '-created_at')

    if status_filter == 'pending_approval':
        claims = []
        pending_approval_items = clean_items
    elif status_filter == 'spam':
        claims = []
        pending_approval_items = []
    elif status_filter == 'all':
        claims = Claim.objects.filter(status__in=['pending', 'approved', 'rejected'], spam_score__lt=SPAM_THRESHOLD).order_by('-created_at')
        pending_approval_items = clean_items
    elif status_filter == 'completed':
        claims = Claim.objects.filter(status='completed').order_by('-created_at')
        pending_approval_items = []
    else:
        claims = Claim.objects.filter(status=status_filter, spam_score__lt=SPAM_THRESHOLD).order_by('-created_at')
        pending_approval_items = []

    counts = {
        'pending_approval': clean_items.count(),
        'pending': Claim.objects.filter(status='pending', spam_score__lt=SPAM_THRESHOLD).count(),
        'approved': Claim.objects.filter(status='approved').count(),
        'rejected': Claim.objects.filter(status='rejected').count(),
        'completed': Claim.objects.filter(status='completed').count(),
        'all': Claim.objects.filter(status__in=['pending', 'approved', 'rejected'], spam_score__lt=SPAM_THRESHOLD).count() + clean_items.count(),
        'all_actionable': clean_items.count() + Claim.objects.filter(status__in=['pending', 'approved', 'rejected'], spam_score__lt=SPAM_THRESHOLD).count(),
        'spam': spam_items.count() + spam_claims.count(),
    }

    return render(request, 'claims/admin_claims.html', {
        'claims': claims,
        'current_filter': status_filter,
        'pending_approval_items': pending_approval_items,
        'spam_items': spam_items,
        'spam_claims': spam_claims,
        'counts': counts,
    })

# Admin view to review claim detail
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
            claim.item.verified_date = timezone.now()
            claim.item.save()
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.admin_notes = admin_notes
            claim.save()
            send_claim_approved_email(claim.claimant, claim)
            messages.success(request, f'Claim approved and verified for {claim.item.name}. 60-day countdown started.')

        elif action == 'reject':
            claim.status = 'rejected'
            claim.item.status = 'rejected'
            claim.item.save()
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.admin_notes = admin_notes
            claim.save()
            send_claim_rejected_email(claim.claimant, claim)
            messages.success(request, f'Claim rejected for {claim.item.name}. Item is now available for new claims.')

        elif action == 'complete':
            if claim.status != 'approved':
                messages.error(request, 'You must verify the claim first before marking the item as returned.')
                return redirect('review_claim', claim_pk=claim_pk)

            claim.status = 'completed'
            claim.item.status = 'returned'
            claim.item.returned_to = claim.claimant
            claim.item.save()
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.admin_notes = admin_notes
            claim.save()
            send_claim_completed_email(claim.claimant, claim)
            messages.success(request, f'Item {claim.item.name} marked as returned to {claim.claimant.get_full_name() or claim.claimant.username}.')

        elif action == 'discard':
            discard_reason = request.POST.get('discard_reason_claim', 'Discarded during claim review')
            claim.item.status = 'discarded'
            claim.item.discard_date = timezone.now()
            claim.item.discard_reason = discard_reason
            claim.item.discarded_by = request.user
            claim.item.save()
            claim.reviewed_by = request.user
            claim.reviewed_at = timezone.now()
            claim.admin_notes = admin_notes
            claim.save()
            # Notify both the claimant and the original reporter
            if claim.claimant.email:
                send_item_discarded_email(claim.claimant, claim.item)
            if claim.item.submitted_by and claim.item.submitted_by != claim.claimant and claim.item.submitted_by.email:
                send_item_discarded_email(claim.item.submitted_by, claim.item)
            messages.success(request, f'Item {claim.item.name} marked as discarded/donated.')

        elif action == 'undo':
            claim.status = 'pending'
            claim.reviewed_by = None
            claim.reviewed_at = None
            claim.admin_notes = admin_notes

            if claim.item.status in ['verified', 'rejected', 'returned']:
                claim.item.status = 'unclaimed'
                claim.item.returned_to = None
                claim.item.verified_date = None
                claim.item.save()

            claim.save()
            messages.success(request, f'Action undone. Claim for {claim.item.name} has been reverted to pending status.')
            return redirect('admin_claims')

        return redirect('admin_claims')

    return render(request, 'claims/review_claim.html', {'claim': claim})


@login_required
def bulk_action_claims(request):
    if not (request.user.is_staff or request.user.user_type in ['teacher', 'admin']):
        return redirect('home')
    if request.method != 'POST':
        return redirect('admin_claims')

    action = request.POST.get('bulk_action')
    claim_ids = request.POST.getlist('selected_claims')
    item_ids = request.POST.getlist('selected_items')

    if claim_ids:
        claims_qs = Claim.objects.filter(pk__in=claim_ids)
        if action == 'spam':
            claims_qs.update(spam_score=99, spam_reasons='Manually marked as spam by admin')
            messages.success(request, f'{claims_qs.count()} claim(s) marked as spam.')
        elif action == 'restore':
            claims_qs.update(spam_score=0, spam_reasons='')
            messages.success(request, f'{claims_qs.count()} claim(s) restored from spam.')
        elif action == 'delete':
            count = claims_qs.count()
            claims_qs.delete()
            messages.success(request, f'{count} claim(s) permanently deleted.')
        elif action == 'approve':
            for claim in claims_qs:
                claim.status = 'approved'
                claim.item.status = 'verified'
                claim.item.verified_date = timezone.now()
                claim.item.save()
                claim.reviewed_by = request.user
                claim.reviewed_at = timezone.now()
                claim.save()
            messages.success(request, f'{len(claim_ids)} claim(s) approved.')
        elif action == 'reject':
            for claim in claims_qs:
                claim.status = 'rejected'
                claim.item.status = 'rejected'
                claim.item.save()
                claim.reviewed_by = request.user
                claim.reviewed_at = timezone.now()
                claim.save()
            messages.success(request, f'{len(claim_ids)} claim(s) rejected.')

    if item_ids:
        from items.models import Item
        items_qs = Item.objects.filter(pk__in=item_ids)
        if action == 'spam':
            items_qs.update(spam_score=99, spam_reasons='Manually marked as spam by admin')
            messages.success(request, f'{items_qs.count()} report(s) marked as spam.')
        elif action == 'restore':
            items_qs.update(spam_score=0, spam_reasons='')
            messages.success(request, f'{items_qs.count()} report(s) restored from spam.')
        elif action == 'delete':
            count = items_qs.count()
            items_qs.delete()
            messages.success(request, f'{count} report(s) permanently deleted.')
        elif action == 'approve':
            for item in items_qs:
                item.status = 'unclaimed'
                item.approved_by = request.user
                item.approval_date = timezone.now()
                item.approval_notes = 'Bulk approved'
                item.save()
                send_item_approved_email(item.submitted_by, item)
            messages.success(request, f'{len(item_ids)} report(s) approved.')
        elif action == 'reject':
            for item in items_qs:
                item.status = 'discarded'
                item.approved_by = request.user
                item.approval_date = timezone.now()
                item.save()
                send_item_rejected_email(item.submitted_by, item)
            messages.success(request, f'{len(item_ids)} report(s) rejected.')

    return redirect(f'/claims/admin/?status={request.POST.get("return_tab", "pending_approval")}')