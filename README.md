# Django Content Tracker: A Comprehensive Package for Tracking Views, Referrals, and User Activity
This package is designed to help developers track user interactions with content on a Django-based website. It provides a robust solution for recording views, referrals, device information, and more. Below is a detailed explanation of the package structure, its components, and how to use it effectively.

## Package Overview
The `django_content_tracker` package allows you to:

1- Track views of any content object (e.g., articles, products, pages) using Django's Generic Relations.

2- Capture user-specific details such as IP address, user agent, device type, browser, and operating system.

3- Prevent duplicate view recordings using session-based tracking.

4- Provide analytics for daily, weekly, and monthly views via mixins.

5- Integrate seamlessly into your Django project with middleware and admin integration.

## Installation

1- Clone or download the package source code.

2- Add the package to your Django project by including it in the INSTALLED_APPS setting:

```python
INSTALLED_APPS = [
    ...
    'django_content_tracker',
]
```
3- Run migrations to create the necessary database tables:

```bash
python manage.py migrate
```

## Components
1- **Models** (`models.py`)

The `ContentView` model is the core of this package. It records every interaction with a content object.

### Fields:
**Content Object** : Uses Django's Generic Relations (`content_type`, `object_id`, `content_object`) to associate the view with any model instance.

**User Information** : Captures the authenticated user (if available).

**Device and Browser Information** : Extracts details like IP address, user agent, referrer, device type, browser, and operating system.

**Timestamp** : Records when the view occurred.


### Example Usage:

```python
from django_content_tracker.models import ContentView

# Create a view record
ContentView.objects.create(
    content_object=my_article,
    user=request.user,
    ip_address="192.168.1.1",
    user_agent="Mozilla/5.0",
    referrer="https://example.com",
    device_type="Mobile",
    browser="Chrome",
    os="Android"
)
```

2- **Mixins** (`mixins.py`)

The `ContentTrackingMixin` provides convenient properties to calculate daily, weekly, and monthly views for any content object.


**Properties:**
- `daily_views`: Counts views that occurred today.
- `weekly_views`: Counts views in the last 7 days.
- `monthly_views`: Counts views in the last 30 days.

### Example Usage:
```python
class Article(models.Model, ContentTrackingMixin):
    title = models.CharField(max_length=255)
    content = models.TextField()

# Access view counts
article = Article.objects.first()
print(article.daily_views)  # e.g., 15
print(article.weekly_views)  # e.g., 120
print(article.monthly_views)  # e.g., 500
```

3- **Middleware** (`middleware.py`)

The `ContentViewMiddleware` automatically tracks views for content objects accessed via HTTP requests. It ensures no duplicate views are recorded by leveraging Django sessions.

**Key Features:**
- Detects the content_object from the request.

- Parses the user agent to extract device, browser, and OS details.

- Stores view data in the database.

**Middleware Configuration:**

Add the middleware to your `MIDDLEWARE` setting:

```python
MIDDLEWARE = [
    ...
    'django_content_tracker.middleware.ContentViewMiddleware',
]
```

4- **Admin Integration** (`admin.py`)

The `ContentViewAdmin` class provides a user-friendly interface in the Django admin panel to view and filter tracked data.

**Features:**

- Displays key fields like content_object, user, ip_address, and viewed_at.
- Filters by content_type, device_type, browser, os, and date.
- Prevents manual addition, deletion, or modification of records.

### Example:
Navigate to `/admin/django_content_tracker/contentview/` to view all tracked views.


5- App Configuration (`apps.py`)

The `ContentTrackerConfig` class defines the app configuration. It sets the default auto field and provides a human-readable name for the app.

6- **Session-Based Duplicate Prevention**

To avoid recording multiple views from the same user during a single session, the middleware uses a session key:

```python
session_key = f"content_viewed_{content_object.__class__.__name__}_{content_object.id}"
```

If the session key exists, the view is not recorded again.

## Dependencies
**Django** : Ensure you are using Django 3.2 or later.

`user_agents` Library : Install it to parse user agent strings:

```bash
pip install pyyaml ua-parser user-agents
```

## Best Practices

### Performance Optimization :
- Use database indexing on frequently queried fields like `viewed_at` and `content_type`.
- Consider caching view counts for high-traffic sites.

### Privacy Compliance :
- Ensure compliance with GDPR or other privacy regulations by anonymizing IP addresses if required.
- Allow users to opt out of tracking if necessary.

### Testing :
- Write unit tests to verify the functionality of the middleware, models, and mixins.
- Test edge cases like anonymous users, missing headers, and invalid content objects.

## Future Enhancements

1- **Analytics Dashboard** :
- Build a frontend dashboard to visualize view trends over time.
2- **Customizable Settings** :
- Allow developers to configure session timeout durations and duplicate prevention rules.
3- **Export Options** :
- Add support for exporting view data to CSV or JSON formats.

## Conclusion
The `django_content_tracker` package is a powerful tool for monitoring user interactions with your Django application's content. By combining models, mixins, middleware, and admin integration, it provides a comprehensive solution for tracking views, referrals, and device information. With proper optimization and adherence to best practices, this package can significantly enhance your application's analytics capabilities.

Feel free to contribute to the package or suggest improvements!
