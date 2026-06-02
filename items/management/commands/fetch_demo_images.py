"""
Downloads real images for demo items and updates their photo fields.
Usage: python manage.py fetch_demo_images
"""
import urllib.request
import urllib.error
import os
import time
from django.core.management.base import BaseCommand
from django.conf import settings
from items.models import Item

ITEM_IMAGES = {
    'Blue Water Bottle':    'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop',
    'Black Backpack':       'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
    'iPhone 13':            'https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=400&h=300&fit=crop',
    'Red Hoodie':           'https://images.unsplash.com/photo-1509942774463-acf339cf87d5?w=400&h=300&fit=crop',
    'Graphing Calculator':  'https://images.unsplash.com/photo-1564466809058-bf4114d55352?w=400&h=300&fit=crop',
    'Student ID Card':      'https://images.unsplash.com/photo-1586861203927-800a5acdcc4d?w=400&h=300&fit=crop',
    'Silver Necklace':      'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=400&h=300&fit=crop',
    'Basketball':           'https://images.unsplash.com/photo-1519861531473-9200262188bf?w=400&h=300&fit=crop',
    'Wireless Earbuds':     'https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?w=400&h=300&fit=crop',
    'Chemistry Textbook':   'https://images.unsplash.com/photo-1532012197267-da84d127e765?w=400&h=300&fit=crop',
    'Car Keys':             'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
    'Denim Jacket':         'https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=300&fit=crop',
    'Lunch Box':            'https://images.unsplash.com/photo-1584278860047-22db9ff82bed?w=400&h=300&fit=crop',
    'USB-C Charger':        'https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400&h=300&fit=crop',
    'Volleyball':           'https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=400&h=300&fit=crop',
    'Prescription Glasses': 'https://images.unsplash.com/photo-1574258495973-f010dfbb5371?w=400&h=300&fit=crop',
    'Spiral Notebook':      'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=300&fit=crop',
    'Gray Sweatpants':      'https://images.unsplash.com/photo-1585487000160-6ebcfceb0d03?w=400&h=300&fit=crop',
    'Portable Speaker':     'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop',
}

class Command(BaseCommand):
    help = 'Downloads real images for demo items'

    def handle(self, *args, **kwargs):
        items_dir = os.path.join(settings.MEDIA_ROOT, 'items')
        os.makedirs(items_dir, exist_ok=True)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        updated = 0
        failed = []

        for item_name, url in ITEM_IMAGES.items():
            try:
                item = Item.objects.filter(name=item_name).first()
                if not item:
                    self.stdout.write(f'  Skipped (not in DB): {item_name}')
                    continue

                filename = item_name.lower().replace(' ', '_') + '.jpg'
                filepath = os.path.join(items_dir, filename)

                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    with open(filepath, 'wb') as f:
                        f.write(response.read())

                item.photo = f'items/{filename}'
                item.save(update_fields=['photo'])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'  Downloaded: {item_name}'))
                time.sleep(0.3)

            except Exception as e:
                failed.append(item_name)
                self.stdout.write(self.style.WARNING(f'  Failed: {item_name} — {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone: {updated} images downloaded.'))
        if failed:
            self.stdout.write(self.style.WARNING(f'Failed ({len(failed)}): {", ".join(failed)}'))
