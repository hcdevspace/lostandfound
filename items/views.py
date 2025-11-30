from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Item
from .forms import ItemForm

# Create your views here.
@login_required
def report_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.submitted_by = request.user
            item.save()
            messages.success(request, 'Item reported successfully!')
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'items/report_item.html', {'form': form})    

def item_list(request):
    items = Item.objects.filter(status='available')

    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    return render(request, 'items/item_list.html', {'items': items})

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

    # Security check: Only owner or staff can edit
    if request.user != item.submitted_by and not request.user.is_staff:
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

    # Security check: Only owner or staff can delete
    if request.user != item.submitted_by and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('item_detail', pk=pk)

    if request.method == 'POST':
        item_name = item.name
        item.delete()
        messages.success(request, f'Item "{item_name}" has been deleted successfully.')
        return redirect('my_items')

    # If GET request, show confirmation page
    return render(request, 'items/delete_item.html', {'item': item})