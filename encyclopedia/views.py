from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })

def get_entry(request, title):
    # add some checking for get entry in case it returns none
    entry = util.get_entry(title)
    entry = markdown2.markdown(entry)
    return render(request, "encyclopedia/entry_page.html", {
        "entry_title": title,
        "entry_info": entry
    })
