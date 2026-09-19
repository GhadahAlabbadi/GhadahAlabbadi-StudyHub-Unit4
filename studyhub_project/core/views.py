from django.core.files.storage import default_storage
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import FeedbackForm

RESOURCES = [
    {
        "id": 1,
        "title": "Django Official Documentation",
        "type": "Article",
        "description": "The official Django docs — the best reference for how any part of the framework works.",
        "url": "https://docs.djangoproject.com/",
    },
    {
        "id": 2,
        "title": "Python Data Structures Crash Course",
        "type": "Video",
        "description": "A video walkthrough of lists, tuples, sets, and dictionaries with practical examples.",
        "url": "https://example.com/python-data-structures",
    },
    {
        "id": 3,
        "title": "MDN Web Docs: HTML Basics",
        "type": "Article",
        "description": "A clear introduction to HTML structure, elements, and semantics.",
        "url": "https://developer.mozilla.org/",
    },
    {
        "id": 4,
        "title": "CSS Flexbox Guide",
        "type": "Link",
        "description": "A visual guide covering every Flexbox property with interactive examples.",
        "url": "https://example.com/flexbox-guide",
    },
    {
        "id": 5,
        "title": "Understanding HTTP Requests",
        "type": "Video",
        "description": "A short video explaining the request-response cycle between browsers and servers.",
        "url": "https://example.com/http-requests",
    },
    {
        "id": 6,
        "title": "Git and GitHub for Beginners",
        "type": "Article",
        "description": "Covers the core Git commands and how GitHub fits into a typical workflow.",
        "url": "https://example.com/git-github-beginners",
    },
]

VALID_TABS = ("details", "source")
VALID_THEMES = ("light", "dark")


def get_theme(request):
    """Read the theme cookie, falling back to 'light' if missing or invalid."""
    theme = request.COOKIES.get("theme")
    return theme if theme in VALID_THEMES else "light"


def get_resource(id):
    return next((r for r in RESOURCES if r["id"] == id), None)


def home(request):
    return render(request, "core/home.html", {"theme": get_theme(request)})


def resource_list(request):
    return render(request, "core/resource_list.html", {
        "resources": RESOURCES,
        "theme": get_theme(request),
    })


def resource_detail(request, id):
    resource = get_resource(id)
    if resource is None:
        raise Http404("Resource not found.")

    if request.method == "POST":
        favorites = request.session.get("favorites", [])
        if resource["id"] not in favorites:
            favorites.append(resource["id"])
            request.session["favorites"] = favorites
        return redirect("core:resource_detail", id=id)

    tab = request.GET.get("tab", "details")
    if tab not in VALID_TABS:
        tab = "details"

    favorites = request.session.get("favorites", [])

    return render(request, "core/resource_detail.html", {
        "resource": resource,
        "tab": tab,
        "theme": get_theme(request),
        "is_favorite": resource["id"] in favorites,
    })


def favorites_view(request):
    if request.method == "POST":
        try:
            remove_id = int(request.POST.get("remove_id", ""))
        except ValueError:
            remove_id = None

        if remove_id is not None:
            favorites = request.session.get("favorites", [])
            if remove_id in favorites:
                favorites.remove(remove_id)
                request.session["favorites"] = favorites
        return redirect("core:favorites")

    favorite_ids = request.session.get("favorites", [])
    favorite_resources = [r for r in RESOURCES if r["id"] in favorite_ids]

    return render(request, "core/favorites.html", {
        "resources": favorite_resources,
        "theme": get_theme(request),
    })


def preferences(request):
    if request.method == "POST":
        theme = request.POST.get("theme")
        if theme not in VALID_THEMES:
            theme = "light"
        response = redirect("core:preferences")
        response.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365)
        return response

    return render(request, "core/preferences.html", {"theme": get_theme(request)})


def feedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.cleaned_data.get("attachment")
            attachment_url = None
            if attachment:
                saved_path = default_storage.save(f"feedback_attachments/{attachment.name}", attachment)
                attachment_url = default_storage.url(saved_path)
            request.session["last_feedback_attachment"] = attachment_url
            return redirect("core:feedback_thanks")
        for field_name in form.errors:
            form.fields[field_name].widget.attrs["class"] = "is-invalid"
    else:
        form = FeedbackForm()

    return render(request, "core/feedback.html", {
        "form": form,
        "theme": get_theme(request),
    })


def feedback_thanks(request):
    attachment_url = request.session.pop("last_feedback_attachment", None)
    return render(request, "core/feedback_thanks.html", {
        "theme": get_theme(request),
        "attachment_url": attachment_url,
    })