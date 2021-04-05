from django.shortcuts import render, redirect
import markdown2
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages 

from . import util

class SearchForm(forms.Form):
    requested_article = forms.CharField(label='Search', max_length=100)

class AddEntryForm(forms.Form):
    title = forms.CharField(label='title', max_length=100)
    info = forms.CharField(label='info', widget=forms.Textarea(attrs={"rows":20, "cols":10}))

class EditPageForm(forms.Form):
    pagename = forms.CharField(label="Title",disabled = False,required = False,
    widget= forms.HiddenInput
    (attrs={'class':'col-sm-12','style':'bottom:1rem'}))
   
    body = forms.CharField(label="Markdown content",help_text="<p class='text-secondary'>Please refer <a class='text-info' href = https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax> GitHub’s Markdown guide</a> </p>",
    widget= forms.Textarea
    (attrs={"rows":20, "cols":80,'class':'col-sm-11','style':'top:2rem'}))

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

def add_entry(request):
    if request.method == 'POST':
        form = AddEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title in util.list_entries():
                search_form = SearchForm()
                return render(request, "encyclopedia/create_entry.html", {
                "entry_form": form,
                "message": "Title already exist. Try another.",
                "form": search_form
                 })
            else:
                info = form.cleaned_data['info']
                util.save_entry(title, info)
                # HttpResponseRedirect('url index')
                return HttpResponseRedirect(reverse('index'))
    else:    
        entry_form = AddEntryForm()
        search_form = SearchForm()
        return render(request, "encyclopedia/create_entry.html", {
            "entry_form": entry_form,
            "form": search_form
        })

def edit_entry(request, entry):
    if request.method == 'POST':
        form = AddEntryForm(request.POST)
        title = form.cleaned_data['title']
        info = form.cleaned_data['info']
        util.save_entry(title, info)

        return HttpResponseRedirect(reverse('index'))
    else:
        content = util.get_entry(entry)
        # edit_form = AddEntryForm()
        return render(request, "encyclopedia/edit.html", {
            # "edit_form": edit_form,
            "title": entry,
            "content": content
        })
            
def edit(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "Can't save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect(index)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})

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