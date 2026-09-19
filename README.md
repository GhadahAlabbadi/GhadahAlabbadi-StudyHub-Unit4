# StudyHub — Learning Resources Portal

A Django web application built for the Unit 4 project. StudyHub lets users browse a catalog of learning resources, view resource details through tabs, save favorites using sessions, switch between light and dark themes using cookies, and submit feedback through a validated form.

## Project Structure

```
studyhub-unit4/
└── studyhub_project/            # Django project root (contains manage.py)
    ├── manage.py
    ├── db.sqlite3
    ├── studyhub_project/        # Project settings package
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   └── asgi.py
    ├── core/                    # Main application
    │   ├── views.py             # All view logic
    │   ├── urls.py              # App-level URL patterns
    │   ├── forms.py             # FeedbackForm with custom validation
    │   ├── models.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── tests.py
    │   ├── migrations/
    │   └── templates/core/      # App-level templates
    │       ├── home.html
    │       ├── resource_list.html
    │       ├── resource_detail.html
    │       ├── favorites.html
    │       ├── preferences.html
    │       ├── feedback.html
    │       └── feedback_thanks.html
    ├── templates/                # Project-level templates
    │   ├── base.html             # Shared layout (header, nav, footer)
    │   └── 404.html              # Custom "page not found" template
    ├── static/
    │   ├── css/
    │   │   ├── base.css          # Shared layout and component styles
    │   │   ├── light.css         # Light theme variables
    │   │   └── dark.css          # Dark theme variables
    │   └── images/
    │       ├── logo.png
    │       └── sample_resource.jpg
    └── media/                    # Reserved for user-uploaded files (unused)
```

## URLs

All routes are defined in `core/urls.py` under the `core` namespace and included from the project's `studyhub_project/urls.py`.

| URL                    | Name                   | Description                                                                                        |
| ---------------------- | ---------------------- | -------------------------------------------------------------------------------------------------- |
| `/`                    | `core:home`            | Landing page with a link into the resource catalog                                                 |
| `/resources/`          | `core:resource_list`   | Lists all available learning resources                                                             |
| `/resources/<int:id>/` | `core:resource_detail` | Shows one resource; supports `?tab=details` and `?tab=source`; POST adds the resource to favorites |
| `/favorites/`          | `core:favorites`       | Lists the resources saved in the current session; POST with `remove_id` removes one                |
| `/preferences/`        | `core:preferences`     | Shows the current theme; POST sets the `theme` cookie                                              |
| `/feedback/`           | `core:feedback`        | Feedback form (GET shows it, POST validates and submits)                                           |
| `/feedback/thanks/`    | `core:feedback_thanks` | Confirmation page after a successful feedback submission                                           |

Requesting an unknown resource ID or any undefined URL returns a custom 404 page (`templates/404.html`), which only renders when `DEBUG = False`.

## Templates

Templates use Django's inheritance system. `templates/base.html` defines the shared header, navigation, content block, and footer. Every page in `core/templates/core/` extends it with `{% extends 'base.html' %}` and fills in the `{% block content %}` block. This keeps the header, navigation, and footer consistent across the whole site and lets the theme (light or dark) be applied from one place.

## Static and Media Files

Static files (CSS and images) are served from the project-level `static/` folder, configured through `STATICFILES_DIRS` in `settings.py`. `base.css` holds shared layout rules that reference CSS variables; `light.css` and `dark.css` each define the same set of variables with different values, and the correct one is loaded based on the current theme.

`MEDIA_URL` and `MEDIA_ROOT` are configured for user-uploaded content, but this project does not currently accept file uploads, so `media/` is present but empty.

## Cookies

The `/preferences/` page lets a user choose a light or dark theme. Submitting the form sends a POST request that sets a `theme` cookie with `max_age` set to one year. On every request, `get_theme()` in `views.py` reads this cookie and falls back to `"light"` if it is missing or holds an unexpected value. The chosen theme is passed into every template's context so the correct stylesheet is loaded consistently across the whole site, not just on the preferences page.

## Sessions

Favorites are stored in the session rather than the database. Posting to a resource's detail page adds its ID to `request.session["favorites"]`; the `/favorites/` page reads that list back and displays the matching resources. Removing a favorite posts a `remove_id` back to `/favorites/`, which updates the session list and redirects. Since this relies on Django's session framework, the `django_session` table must exist, which requires running `python manage.py migrate` once after setup.

## Forms

The feedback form (`core/forms.py`) is a plain `forms.Form`, not a `ModelForm`. It collects a name, an email address, a message, and an optional rating. The message field has a custom `clean_message()` validator that requires at least 20 characters. Fields are rendered manually in `feedback.html` rather than with `{{ form.as_p }}`, so that each field's error message can be shown directly beneath it and invalid fields can be highlighted with a CSS class. A valid submission redirects to `/feedback/thanks/` following the Post/Redirect/Get pattern, so refreshing the confirmation page does not resubmit the form.

## Known Limitations

- Favorites are tied to the browser session, so they are lost if the session expires or the user switches browsers or devices.
- Feedback submissions are not stored anywhere; they are validated and then discarded after showing the confirmation page.
- There is no user authentication, so preferences and favorites cannot be tied to a specific person.
- The resource catalog is hardcoded in `views.py` rather than stored in the database.

## Possible Future Improvements

- Move the resource catalog into a database model so resources can be added or edited without changing code.
- Add user accounts so favorites and feedback persist across sessions and devices.
- Store submitted feedback in the database and add an admin view to read it.
- Add search and filtering to the resource list.

## Setup

```
python -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
pip install django
cd studyhub_project
python manage.py migrate
python manage.py runserver
```

Then open `http://127.0.0.1:8000/` in a browser.
