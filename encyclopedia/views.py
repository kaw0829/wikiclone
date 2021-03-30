from django.shortcuts import render
import markdown2
from django import forms

from . import util

class SearchForm(forms.Form):
    requested_article = forms.CharField(label='Search', max_length=100)

def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        #if data is valid for this form
        if form.is_valid():
            #clean the data and strip out the submitted post data then append to task global list
            search_param = form.cleaned_data['requested_article']
            entry = util.get_entry(search_param)
            # return entry page with correct match
            if (entry):
                form1 = SearchForm()
                entry = markdown2.markdown(entry)
                return render(request, "encyclopedia/entry_page.html", {
                "entry_title": search_param,
                "entry_info": entry,
                "form": form1
        })
        # return results from partial string match
            else:
                matching_list = util.search_entries(search_param)
                print(matching_list)
                return render(request, "encyclopedia/search.html", {
                "list_matches": matching_list,
                "search_word": search_param
                })
        else:
            # return form with invalid data to be corrected
            return render(request, "encyclopedia/search.html", {
            "form": form
            })
    # return initial home page with blank search
    else:
        form = SearchForm()
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'form': form
        })

def get_entry(request, title):
    # checks for entry and either returns error page if not found or returns correct entry
    entry = util.get_entry(title)
    form = SearchForm()
    if entry != None:
        entry = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry_page.html", {
            "entry_title": title,
            "entry_info": entry,
            "form": form
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "form": form
        })



# def get_name(request):
#     # if this is a POST request we need to process the form data
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             return HttpResponseRedirect('/thanks/')

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()

#     return render(request, 'name.html', {'form': form})