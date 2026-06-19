# Weighted Signal Algorithm for Spam Detection

## What is it?

The Lost & Found platform uses a **deterministic, rule-based weighted scoring system** to flag likely spam submissions — fake item reports, bogus claims, and fraudulent account registrations — without relying on machine learning.

Each submission accumulates points from independent signals. The total score (capped at 100) determines how the submission is classified:

| Score Range | Classification |
|---|---|
| 0–30 | Clean |
| 31–60 | Suspicious |
| 61–100 | Spam |

This logic lives in `lostandfound/spam_detector.py` and is called from the views right after an item, claim, or user account is created.

---

## Why rule-based instead of machine learning?

- **No training data exists yet** — a fresh school deployment has no labeled spam/clean dataset to train a model on
- **Explainable** — every flagged submission stores a human-readable list of *why* it was flagged (`spam_reasons`), so staff can verify the decision instead of trusting a black box
- **Fast to build and tune** — thresholds and point values can be adjusted directly without retraining anything

---

## Scoring: Item Reports — `score_item()`

| Signal | Points |
|---|---|
| Duplicate name + location already reported | +55 |
| Description under 15 characters | +25 |
| Keyboard-mash or repeated-character text (name or description) | +40 |
| Excessive symbols (over 30% non-alphanumeric characters) | +20 |
| Generic or very short item name (e.g. "thing", "stuff") | +20 |
| Same user submitted 3+ reports in the last hour | +35 |
| Account under 24 hours old with 2+ reports already | +30 |
| Same IP address submitted 3+ reports in the last hour | +35 |
| Identical photo hash reused from a previous report | +40 |

```python
from lostandfound.spam_detector import score_item

sp_score, sp_reasons = score_item(item)
item.spam_score = sp_score
item.spam_reasons = sp_reasons
item.save(update_fields=['spam_score', 'spam_reasons'])
```

---

## Scoring: Claims & Inquiries — `score_claim()`

| Signal | Points |
|---|---|
| Proof-of-ownership description under 20 characters | +35 |
| Vague filler phrase detected ("it is mine", "i lost it") | +50 |
| Keyboard-mash or repeated-character text in proof | +40 |
| Identical proof text reused by the same user on a different claim | +55 |
| 2+ claims submitted by the same user in the last 24 hours | +30 |
| 3+ claims by the same user in the same category within 30 days | +25 |

---

## Scoring: Account Registrations — `score_user()`

| Signal | Points |
|---|---|
| Disposable/temporary email domain (mailinator, tempmail, etc.) | +60 |
| Plus-tag email variant (`user+test@domain.com`) | +35 |
| Username is high-consonant-ratio gibberish | +30 |
| Keyboard-mash pattern in username | +40 |
| Username is a numbered variant of an existing account (`john`, `john2`) | +45 |
| First/last name fields appear to be gibberish | +25 |
| Email previously used by a rejected account | +50 |
| 3+ accounts registered from the same IP in the last hour | +40 |

---

## Supporting Helper Functions

```python
def _is_keyboard_mash(text):
    """Detects 4+ consecutive same-row keyboard characters (qwer, asdf)
    or 4+ repeated characters in a row."""

def _consonant_ratio(text):
    """Returns the fraction of letters that are consonants.
    A high ratio (> 0.75) suggests random/gibberish text."""

def _has_excessive_symbols(text):
    """Returns True if more than 30% of characters are
    non-alphanumeric and non-whitespace."""

def hash_photo(photo_file):
    """Returns the MD5 hash of an uploaded image file,
    used to detect reused/duplicate photos across reports."""

def get_client_ip(request):
    """Extracts the submitter's IP address, checking the
    X-Forwarded-For header first (set by nginx), falling back
    to REMOTE_ADDR."""
```

---

## Admin Moderation Workflow

Flagged submissions are excluded from the normal review queue and surfaced in a dedicated **Spam** tab on the admin pages (`admin_claims.html`, `pending_users.html`). Each flagged entry displays:

```
Spam • 78/100
⚠ Disposable email domain; Keyboard mash name; Generic filler username
```

Admins can take bulk action on selected items/claims/users:

- **Approve** — overrides the spam flag and processes normally
- **Reject** — denies the submission
- **Mark as Spam** — manually flags a submission with `spam_score = 99`
- **Restore from Spam** — clears the flag (`spam_score = 0`, `spam_reasons = ''`)
- **Delete** — permanently removes the submission

```python
claims_qs.update(spam_score=99, spam_reasons='Manually marked as spam by admin')
claims_qs.update(spam_score=0, spam_reasons='')
```

---

## Tuning the Thresholds

```python
# lostandfound/spam_detector.py
SPAM_THRESHOLD = 61
SUSPICIOUS_THRESHOLD = 31
```

Raising `SPAM_THRESHOLD` makes the system more lenient (fewer false positives, but more spam slips through). Lowering it makes the system stricter. Individual signal weights can also be tuned independently — for example, increasing the duplicate-photo penalty if reused stock images become a common spam pattern.

---

## Resources

- [Django Model Fields Reference](https://docs.djangoproject.com/en/stable/ref/models/fields/) — for `spam_score` / `spam_reasons` field definitions
- [hashlib — MD5 Hashing](https://docs.python.org/3/library/hashlib.html) — used for photo duplicate detection
