# Sources, Citations, and Documentation
This document lists all external resources, libraries, tutorials, and references used in the development of ReFind.


## Frameworks & Libraries

### Django Framework
- **Name:** Django
- **Version:** 5.2.8
- **URL:** https://www.djangoproject.com/
- **License:** BSD-3-Clause
- **Purpose:** Main web framework for backend development
- **Citation:** Django Software Foundation. (2025). Django: The Web framework for perfectionists with deadlines. Retrieved from https://www.djangoproject.com/
- Used **Python 3.14** to develop with this framework

### Font Awesome
- **Name:** Font Awesome
- **Version:** 7.1.0
- **URL:** https://fontawesome.com/
- **License:** Font Awesome Free License
- **Purpose:** Icons throughout the application
- **Citation:** Fonticons, Inc. (2025). Font Awesome. Retrieved from https://fontawesome.com/

### Pillow (PIL)
- **Name:** Pillow
- **Version:** 12.1
- **URL:** https://python-pillow.org/
- **License:** HPND License
- **Purpose:** Image processing and validation
- **Citation:** Clark, A. (2025). Pillow: The friendly PIL fork. Retrieved from https://python-pillow.org/

### boto3

- **Name**: boto3
- **Version**: 1.34.0
- **URL**: https://aws.amazon.com/sdk-for-python/
- **License**: Apache License 2.0
- **Purpose**: Amazon Web Services (AWS) SDK for Python, used to connect the application to Amazon S3 buckets for secure storage.
- **Citation**: Amazon Web Services, Inc. (2026). AWS SDK for Python (Boto3). Retrieved from https://aws.amazon.com/sdk-for-python/

### django-storages

- **Name**: django-storages
- **Version**: 1.14.0
- **URL**: https://django-storages.readthedocs.io/
- **License**: BSD-3-Clause
- **Purpose**: Custom storage backend engine that routes Django's FileField and ImageField uploads directly to AWS S3.
- **Citation**: Schneier, J., Larlet, D., & Contributors. (2026). django-storages: Custom storage backends for Django. Retrieved from https://django-storages.readthedocs.io/

### psycopg2-binary

- **Name**: psycopg2-binary
- **Version**: 2.9.12
- **URL**: https://pypi.org/project/psycopg2-binary/
- **License**: LGPL-3.0 (with exceptions)
- **Purpose**: PostgreSQL database adapter for Python. It allows the Django application to communicate natively with the Amazon RDS PostgreSQL instance.
- **Citation**: Di Gregorio, F., & Varrazzo, D. (2026). psycopg2-binary: PostgreSQL database adapter for Python. Retrieved from https://pypi.org/project/psycopg2-binary/

---

## Documentation References

### Django Official Documentation
- **URL:** https://docs.djangoproject.com/
- **Sections Used:**
  - Authentication system
  - File uploads
  - Forms and validation
  - Database models
- **Citation:** Django Software Foundation. (2025). Django documentation. Retrieved from https://docs.djangoproject.com/

### Python Official Documentation
- **URL:** https://docs.python.org/3/
- **Sections Used:**
  - datetime module
  - os module
  - File handling
- **Citation:** Python Software Foundation. (2025). Python documentation. Retrieved from https://docs.python.org/3/

### AWS Amazon S3 Official Documentation

- **URL**: https://docs.aws.amazon.com/s3/
- **Sections Used**:
  - Creating and configuring S3 buckets
  - IAM (Identity and Access Management) policies for application access
  - Object lifecycle management for item images
- **Citation**: Amazon Web Services, Inc. (2026). Amazon Simple Storage Service (S3) documentation. Retrieved from https://docs.aws.amazon.com/s3/

### AWS Amazon EC2 Official Documentation

- **URL**: https://docs.aws.amazon.com/ec2/
- **Sections Used**:
  - Linux virtual machine configuration (Ubuntu/Amazon Linux)
  - Security Groups and inbound/outbound firewall rules for port 8000/443
  - Application hosting environment setup
- **Citation**: Amazon Web Services, Inc. (2026). Amazon Elastic Compute Cloud (EC2) documentation. Retrieved from https://docs.aws.amazon.com/ec2/

### AWS Amazon RDS Official Documentation

- **URL**: https://docs.aws.amazon.com/rds/
- **Sections Used**:
  - PostgreSQL instance provisioning
  - Database subnet groups and security connectivity
  - Environment string extraction for live database linking
- **Citation**: Amazon Web Services, Inc. (2026). Amazon Relational Database Service (RDS) documentation. Retrieved from https://docs.aws.amazon.com/rds/

---

## Tutorials & Learning Resources

### Django Tutorial by Mozilla
- **Title:** Django Web Framework (Python)
- **URL:** https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django
- **Purpose:** Learning Django basics
- **Citation:** Mozilla Contributors. (2025). Django Web Framework. MDN Web Docs. Retrieved from https://developer.mozilla.org/

### Real Python - Django Tutorials
- **URL:** https://realpython.com/tutorials/django/
- **Specific Articles Used:**
  - "Get Started With Django"
  - "Django Migrations"
  - "Django User Authentication"
- **Citation:** Real Python Team. (2025). Django tutorials. Real Python. Retrieved from https://realpython.com/

---

## Design Resources

### Color Palette
- **Tool:** Coolors.co
- **URL:** https://coolors.co/
- **Purpose:** Color scheme selection
- **Citation:** Coolors. (2025). Color scheme generator. Retrieved from https://coolors.co/

### UI/UX Inspiration
- **Source:** Dribbble
- **URL:** https://dribbble.com/
- **Search Terms:** "lost and found interface", "school management system."
- **Purpose:** Design inspiration for user interface

---

## Code Snippets & Stack Overflow

### File Upload Validation
- **URL:** https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
- **Date Accessed:** December 2025
- **Purpose:** Learning how to validate file sizes in Django
- **Modified for our specific needs**
  
### Image Processing
- **URL:** https://stackoverflow.com/questions/6350602/django-how-to-resize-uploaded-images
- **Date Accessed:** December 2025
- **Purpose:** Understanding PIL/Pillow image handling

### Django S3 Cloud Storage Integration

- **URL**: https://stackoverflow.com/questions/4364443/how-to-use-django-storages-with-amazon-s3
- **Date Accessed**: June 2026
- **Purpose**: Learning how to structure settings.py environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_STORAGE_BUCKET_NAME) to authenticate the app safely.
- **Modified configuration blocks to utilize secure environment variables**

### Django Managed Database Connection Configuration

- **URL**: https://stackoverflow.com/questions/42220465/connecting-django-to-amazon-rds-postgresql
- **Date Accessed**: January 2026
- **Purpose**: Learning how to safely configure the DATABASES setting dictionary in settings.py to reference an external AWS RDS endpoint, database port, and authentication tokens via environment variables.
- **Modified code to prevent exposing structural database credentials in version control**

---

## Database Design Resources

### Database Schema Design
- **Resource:** Draw.io (diagrams.net)
- **URL:** https://www.diagrams.net/
- **Purpose:** Creating entity-relationship diagrams

### SQL Best Practices
- **Resource:** Django ORM Documentation
- **URL:** https://docs.djangoproject.com/en/5.0/topics/db/
- **Purpose:** Database optimization and query design

---

## Testing Resources

### Django Testing Documentation
- **URL:** https://docs.djangoproject.com/en/5.0/topics/testing/
- **Purpose:** Learning Django's testing framework
- **Sections Used:**
  - Writing and running tests
  - Testing tools
  - Advanced testing topics

---

## Security Resources

### OWASP Web Security
- **URL:** https://owasp.org/
- **Purpose:** Security best practices
- **Specific Resources:**
  - OWASP Top 10
  - Authentication cheat sheet
  - File upload cheat sheet
- **Citation:** OWASP Foundation. (2025). OWASP Top 10. Retrieved from https://owasp.org/

### Django Security Documentation
- **URL:** https://docs.djangoproject.com/en/5.0/topics/security/
- **Purpose:** Framework-specific security practices

---

## Additional Resources

### GitHub Documentation
- **URL:** https://docs.github.com/
- **Purpose:** Version control best practices
- **Citation:** GitHub, Inc. (2025). GitHub Docs. Retrieved from https://docs.github.com/

### Markdown Guide
- **URL:** https://www.markdownguide.org/
- **Purpose:** Documentation formatting
- **Citation:** Cone, M. (2025). Markdown Guide. Retrieved from https://www.markdownguide.org/

---

## FBLA Resources

### FBLA Competitive Events Guidelines
- **Title:** Coding & Programming Event Guidelines
- **Year:** 2025-2026
- **Publisher:** Future Business Leaders of America 
- **URL:** https://www.fbla.org/
- **Purpose:** Project requirements and judging criteria

---

## Image Assets

### Stock Photos
- **Source:** Unsplash
- **URL:** https://unsplash.com/
- **License:** Unsplash License (Free to use)
- **Images Used:** [List specific images]

### Icons
- **All icons:** Font Awesome 6.4.0 (cited above)
- **License:** Font Awesome Free License

---



**Last Updated:** June 25, 2026
**Project:** ReFind
**Event:** FBLA Website Coding & Development 2025-2026
