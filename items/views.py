from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    return render(request, 'items/item_list.html', {'items': items})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {'item': item})

@login_required
def my_items(request):
    items = Item.ob.filter(submitted_by=request.user)
    return render(request, 'items/my_items.html', {'items': items})