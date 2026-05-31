from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Item
from .forms import ItemForm
from accounts.emails import (
    send_item_reported_email,
    send_item_approved_email,
    send_item_rejected_email,
    send_item_discarded_email,
)

# Create your views here.
@login_required
def report_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.submitted_by = request.user
            item.save()
            send_item_reported_email(request.user, item)
            messages.success(request, 'Item reported successfully! Please bring the physical item to the Lost & Found office for verification. Once staff approves it, the item will be available for claims.')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()

    return render(request, 'items/report_item.html', {'form': form})

@login_required
def item_list(request):
    # Show items that are unclaimed or have rejected claims (available for new claims)
    items = Item.objects.filter(status__in=['unclaimed', 'rejected'])

    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)

    # Get categories from the model for dynamic filtering
    categories = Item.CATEGORY_CHOICES

    return render(request, 'items/item_list.html', {
        'items': items,
        'categories': categories,
    })

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})

@login_required
def my_items(request):
    items = Item.objects.filter(submitted_by=request.user)
    return render(request, 'items/my_items.html', {'items': items})

@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Security check: Only the student who reported it, teachers, or admins can edit
    is_owner = request.user == item.submitted_by
    is_teacher = request.user.user_type == 'teacher'
    is_admin = request.user.user_type == 'admin' or request.user.is_staff

    if not (is_owner or is_teacher or is_admin):
        messages.error(request, 'You do not have permission to edit this item.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'Item "{item.name}" has been updated successfully.')
            return redirect('item_detail', pk=pk)
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/edit_item.html', {'form': form, 'item': item})

@login_required
def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Security check: Only teachers or admins can delete (students cannot delete)
    is_teacher = request.user.user_type == 'teacher'
    is_admin = request.user.user_type == 'admin' or request.user.is_staff

    if not (is_teacher or is_admin):
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" has been deleted successfully.')
        return redirect('my_items')

    # If GET request, show confirmation page
    return render(request, 'items/delete_item.html', {'item': item})

@login_required
def discard_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Security check: Only teachers or admins can discard
    is_teacher = request.user.user_type == 'teacher'
    is_admin = request.user.user_type == 'admin' or request.user.is_staff

    if not (is_teacher or is_admin):
        messages.error(request, 'You do not have permission to discard this item.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        # Get discard details from form
        discard_reason = request.POST.get('discard_reason', 'Manual discard by admin')
        discard_notes = request.POST.get('discard_notes', '')

        # Update item status and discard info
        item.status = 'discarded'
        item.discard_date = timezone.now()
        item.discard_reason = discard_reason
        item.discard_notes = discard_notes
        item.discarded_by = request.user
        item.save()

        # Notify the original reporter
        if item.submitted_by and item.submitted_by.email:
            send_item_discarded_email(item.submitted_by, item)

        # Also notify any claimant whose claim was pending/approved
        from claims.models import Claim
        active_claim = Claim.objects.filter(
            item=item, status__in=['pending', 'approved']
        ).select_related('claimant').first()
        if active_claim and active_claim.claimant != item.submitted_by and active_claim.claimant.email:
            send_item_discarded_email(active_claim.claimant, item)

        messages.success(request, f'Item "{item.name}" has been marked as discarded/donated.')
        return redirect('item_list')

    # If GET request, show confirmation page
    return render(request, 'items/discard_item.html', {'item': item})

@login_required
def approve_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Security check: Only teachers or admins can approve
    is_teacher = request.user.user_type == 'teacher'
    is_admin = request.user.user_type == 'admin' or request.user.is_staff

    if not (is_teacher or is_admin):
        messages.error(request, 'You do not have permission to approve items.')
        return redirect('item_detail', pk=pk)

    # Only approve items with 'reported' status
    if item.status != 'reported':
        messages.warning(request, 'This item has already been processed.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        # Get approval notes from form
        approval_notes = request.POST.get('approval_notes', '')

        # Update item status and approval info
        item.status = 'unclaimed'
        item.approval_date = timezone.now()
        item.approval_notes = approval_notes
        item.approved_by = request.user
        item.save()

        # Notify the reporter
        if item.submitted_by and item.submitted_by.email:
            send_item_approved_email(item.submitted_by, item)

        messages.success(request, f'Item "{item.name}" has been approved and is now available for claims.')
        return redirect('item_list')

    # If GET request, show confirmation page
    return render(request, 'items/approve_item.html', {'item': item})


@login_required
def reject_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    # Security check: Only teachers or admins can reject
    is_teacher = request.user.user_type == 'teacher'
    is_admin = request.user.user_type == 'admin' or request.user.is_staff

    if not (is_teacher or is_admin):
        messages.error(request, 'You do not have permission to reject items.')
        return redirect('item_detail', pk=pk)

    # Only reject items with 'reported' status
    if item.status != 'reported':
        messages.warning(request, 'This item has already been processed.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        rejection_notes = request.POST.get('rejection_notes', '')

        item.status = 'discarded'
        item.discard_date = timezone.now()
        item.discard_reason = 'Item report rejected by staff'
        item.discard_notes = rejection_notes
        item.discarded_by = request.user
        item.save()

        # Notify the reporter
        if item.submitted_by and item.submitted_by.email:
            send_item_rejected_email(item.submitted_by, item, notes=rejection_notes)

        messages.success(request, f'Item "{item.name}" report has been rejected.')
        return redirect('admin_claims')

    return render(request, 'items/reject_item.html', {'item': item})