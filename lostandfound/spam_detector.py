import re
import hashlib
from datetime import timedelta
from django.utils import timezone

DISPOSABLE_DOMAINS = {
    'guerrillamail', 'tempmail', 'mailinator', 'throwam', 'yopmail',
    'sharklasers', 'trashmail', 'dispostable', 'spamgourmet', 'getairmail',
    'mailnull', 'fakeinbox', 'spam4', 'grr', 'spammotel', 'maildrop',
    'discard', 'trashmail', 'tempinbox', 'throwaway', 'spambox',
}

FILLER_PHRASES = {
    "it is mine", "it's mine", "its mine", "i lost it", "belongs to me",
    "my item", "its my", "it's my", "i own it", "my stuff", "this is mine",
}

GENERIC_NAMES = {
    'item', 'thing', 'stuff', 'object', 'lost', 'found', 'misc',
    'miscellaneous', 'unknown', 'something', 'anything', 'test',
}

KEYBOARD_ROWS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm']

SPAM_THRESHOLD = 61
SUSPICIOUS_THRESHOLD = 31


def get_client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


def hash_photo(photo_file):
    try:
        photo_file.seek(0)
        digest = hashlib.md5(photo_file.read()).hexdigest()
        photo_file.seek(0)
        return digest
    except Exception:
        return ''


def _is_keyboard_mash(text):
    t = text.lower().replace(' ', '')
    if not t:
        return False
    for row in KEYBOARD_ROWS:
        for i in range(len(t) - 3):
            if all(c in row for c in t[i:i + 4]):
                return True
    if re.search(r'(.)\1{3,}', t):
        return True
    return False


def _consonant_ratio(text):
    letters = re.sub(r'[^a-zA-Z]', '', text.lower())
    if len(letters) < 4:
        return 0.0
    vowels = sum(1 for c in letters if c in 'aeiou')
    return 1.0 - (vowels / len(letters))


def _has_excessive_symbols(text):
    if not text:
        return False
    special = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return (special / len(text)) > 0.3


def score_item(item):
    from items.models import Item

    score = 0
    reasons = []

    if Item.objects.filter(
        name__iexact=item.name,
        location_found__iexact=item.location_found,
    ).exclude(pk=item.pk).exists():
        score += 55
        reasons.append('Duplicate report — same name and location already exists')

    desc = item.description.strip()
    if len(desc) < 15:
        score += 25
        reasons.append('Description too short')

    if _is_keyboard_mash(desc) or _is_keyboard_mash(item.name):
        score += 40
        reasons.append('Keyboard mash or repeated characters detected')

    if _has_excessive_symbols(desc):
        score += 20
        reasons.append('Excessive symbols or special characters in description')

    if item.name.strip().lower() in GENERIC_NAMES or len(item.name.strip()) < 4:
        score += 20
        reasons.append('Generic or very short item name')

    if item.submitted_by_id:
        recent = Item.objects.filter(
            submitted_by_id=item.submitted_by_id,
            created_at__gte=timezone.now() - timedelta(hours=1),
        ).exclude(pk=item.pk).count()
        if recent >= 3:
            score += 35
            reasons.append(f'User submitted {recent} other reports in the last hour')

        age = timezone.now() - item.submitted_by.date_joined
        if age.total_seconds() < 86400:
            total = Item.objects.filter(submitted_by_id=item.submitted_by_id).exclude(pk=item.pk).count()
            if total >= 2:
                score += 30
                reasons.append('Multiple reports from an account less than 24 hours old')

    if item.submitter_ip:
        ip_count = Item.objects.filter(
            submitter_ip=item.submitter_ip,
            created_at__gte=timezone.now() - timedelta(hours=1),
        ).exclude(pk=item.pk).count()
        if ip_count >= 3:
            score += 35
            reasons.append(f'{ip_count} other reports from the same IP in the last hour')

    if item.photo_hash:
        if Item.objects.filter(photo_hash=item.photo_hash).exclude(pk=item.pk).exists():
            score += 40
            reasons.append('Same photo used in a previous report')

    return min(score, 100), '; '.join(reasons)


def score_claim(claim):
    from claims.models import Claim

    score = 0
    reasons = []

    desc = claim.description.strip()

    if len(desc) < 20:
        score += 35
        reasons.append('Proof of ownership too short')

    desc_lower = desc.lower()
    for phrase in FILLER_PHRASES:
        if phrase in desc_lower:
            score += 50
            reasons.append('Vague ownership proof detected')
            break

    if _is_keyboard_mash(desc):
        score += 40
        reasons.append('Keyboard mash or repeated characters in proof')

    if Claim.objects.filter(
        claimant_id=claim.claimant_id,
        description__iexact=claim.description,
    ).exclude(pk=claim.pk).exists():
        score += 55
        reasons.append('Identical proof text used in a previous claim by this user')

    recent = Claim.objects.filter(
        claimant_id=claim.claimant_id,
        created_at__gte=timezone.now() - timedelta(hours=24),
    ).exclude(pk=claim.pk).count()
    if recent >= 2:
        score += 30
        reasons.append(f'User submitted {recent} other claims in the last 24 hours')

    same_cat = Claim.objects.filter(
        claimant_id=claim.claimant_id,
        item__category=claim.item.category,
        created_at__gte=timezone.now() - timedelta(days=30),
    ).exclude(pk=claim.pk).count()
    if same_cat >= 3:
        score += 25
        reasons.append(f'User claimed {same_cat} items in the same category this month')

    return min(score, 100), '; '.join(reasons)


def score_user(user):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    score = 0
    reasons = []

    email = user.email.lower()
    username = user.username.lower()

    if '@' in email:
        domain_root = email.split('@')[1].split('.')[0]
        if domain_root in DISPOSABLE_DOMAINS:
            score += 60
            reasons.append('Disposable or temporary email domain')

    local = email.split('@')[0] if '@' in email else ''
    if '+' in local:
        score += 35
        reasons.append('Plus-tag email variant detected')

    if _consonant_ratio(username) > 0.75 and len(re.sub(r'[^a-z]', '', username)) >= 5:
        score += 30
        reasons.append('Username appears to be random characters')

    if _is_keyboard_mash(username):
        score += 40
        reasons.append('Keyboard mash pattern in username')

    base = re.sub(r'\d+$', '', username)
    if base and base != username:
        if User.objects.filter(username__startswith=base).exclude(pk=user.pk).count() >= 1:
            score += 45
            reasons.append('Username is a numbered variant of an existing account')

    full = (user.first_name + user.last_name).strip()
    if full and _consonant_ratio(full) > 0.75 and len(re.sub(r'[^a-zA-Z]', '', full)) >= 4:
        score += 25
        reasons.append('Name fields appear to be gibberish')

    if User.objects.filter(email=user.email, approval_status='rejected').exclude(pk=user.pk).exists():
        score += 50
        reasons.append('Email was previously used by a rejected account')

    if getattr(user, 'registration_ip', None):
        recent = User.objects.filter(
            registration_ip=user.registration_ip,
            date_joined__gte=timezone.now() - timedelta(hours=1),
        ).exclude(pk=user.pk).count()
        if recent >= 3:
            score += 40
            reasons.append(f'{recent} other accounts registered from the same IP in the last hour')

    return min(score, 100), '; '.join(reasons)
