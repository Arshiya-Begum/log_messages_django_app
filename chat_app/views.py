from django.shortcuts import render
from django.http import HttpResponse
import re
from django.utils.timezone import datetime
from chat_app.models import LogMessage
from chat_app.forms import LogMessageForm
from django.shortcuts import redirect
from django.views.generic import ListView

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, Django!")

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = LogMessage

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        return context
    
def hello_there_notemplates(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return HttpResponse(content)

def hello_there(request, name):
    print(request.build_absolute_uri()) #optional
    return render(
        request,
        'chat_app/hello_there.html',
        {
            'name': name,
            'date': datetime.now()
        }
    )

def home(request):
    return render(request, "chat_app/home.html")

def about(request):
    return render(request, "chat_app/about.html")

def contact(request):
    return render(request, "chat_app/contact.html")

# Add this code elsewhere in the file:
def log_message(request):
    form = LogMessageForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            message = form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            return redirect("home")
    else:
        return render(request, "chat_app/log_message.html", {"form": form})
