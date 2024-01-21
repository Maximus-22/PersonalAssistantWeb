from datetime import datetime, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views import View
from django.db.models import Q

from .forms import NotebookForm, DeleteNoteForm, SearchNoteForm
from .models import Notebook, Tag, NotebookTag


def format_created_at(created_at):
    now = datetime.now()
    delta = now - created_at

    if delta < timedelta(minutes=60):
        return f"Created at: {delta.seconds // 60} minutes ago"
    elif delta < timedelta(hours=24):
        return f"Created at: today"
    elif delta < timedelta(days=7):
        return f"Created at: {delta.days} days ago"
    elif delta < timedelta(days=30):
        return f"Created at: {delta.days // 7} weeks ago"
    else:
        return f"Created at: {delta.days // 30} months ago"


@login_required
def notebook_list(request):
    notebooks = Notebook.objects.all()
    search_form = SearchNoteForm(request.GET)
    elem_per_page = 5
    paginator = Paginator(notebooks, elem_per_page)
    page = request.GET.get('page', 1)

    try:
        notebooks_on_page = paginator.page(page)
    except PageNotAnInteger:
        notebooks_on_page = paginator.page(1)
    except EmptyPage:
        notebooks_on_page = paginator.page(paginator.num_pages)

    return render(request, "notebook/notebook_list.html",
                  context={"notebooks": notebooks_on_page, "search_form": search_form})


@login_required
def add_note(request):
    if request.method == 'POST':
        note_form = NotebookForm(request.POST)
        if request.user.is_authenticated:
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.user = request.user
                note.save()
                tags = note_form.cleaned_data['tags']
                tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
                note.tags.set(tag_objects)
                return redirect(to='notebook:all_notes')
    else:
        note_form = NotebookForm()

    return render(request, 'notebook/add_note.html', {'note_form': note_form})


@login_required
def search_notes(request):
    if request.method == 'GET':
        search_form = SearchNoteForm(request.GET)
        query = request.GET.get('query', '')

        if not query or len(query) < 3:
            messages.error(request, 'Мінімальна довжина запиту - 3 символи.')
            return redirect(to='notebook:all_notes')

        if search_form.is_valid():
            results = Notebook.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            elem_per_page = 5
            paginator = Paginator(results, elem_per_page)
            page = request.GET.get('page', 1)
            try:
                results_page = paginator.page(page)
            except PageNotAnInteger:
                results_page = paginator.page(1)
            except EmptyPage:
                results_page = paginator.page(paginator.num_pages)

            context = {'results': results_page, 'query': query}
            return render(request, 'notebook/search_notes.html', context)
        else:
            # messages.warning(request, 'The Query search parameters are wrong.')
            messages.warning(request, 'Параметри запиту пошуку незадовільні.')


@login_required
def update_note(request, notebook_id):
    note = get_object_or_404(Notebook, id=notebook_id)
    if request.method == 'POST':
        note_form = NotebookForm(request.POST, instance=note)
        # print(form)
        if request.user.is_authenticated and note.user == request.user:
            if note_form.is_valid():

                updated_note = note_form.save(commit=False)
                updated_note.user = request.user
                updated_note.save()

                tags_str = note_form.cleaned_data['tags']
                # print(tags_str)
                tag_objects = [Tag.objects.get_or_create(name=tag)[0] for tag in tags_str]
                updated_note.tags.set(tag_objects)

                messages.success(request, 'Нотатку успішно оновлено.')
                return redirect(to='notebook:all_notes')
            else:
                messages.warning(request, 'Оновлення нотатки скасовано.')
        else:
            messages.warning(request, 'У вас немає прав для оновлення цієї нотатки.')
    else:
        note_form = NotebookForm(instance=note)
    return render(request, 'notebook/update_note.html',
                  {'notebook_id': notebook_id, 'note': note, 'note_form': note_form})


@login_required
def delete_note(request, notebook_id):
    note = get_object_or_404(Notebook, id=notebook_id)

    if request.method == 'POST':
        form = DeleteNoteForm(request.POST)
        # print(form)
        if request.user.is_authenticated and note.user == request.user:
            if form['confirm_delete'].value() == "False":
                note.delete()
                # messages.success(request, 'The Note deleted successfully.')
                messages.success(request, 'Нотатку успішно видалено.')
                return redirect(to='notebook:all_notes')
            else:
                # messages.warning(request, 'The Note deletion cancelled.')
                messages.warning(request, 'Видалення Нотатки скасовано.')
    else:
        form = DeleteNoteForm()

    return render(request, 'notebook/delete_note.html', {'notebook_id': notebook_id, 'note': note, 'form': form})


class TagNotesView(View):
    template_name = 'notebook/tag_notes.html'
    notebooks_per_page = 5

    def get(self, request, *args, **kwargs):
        # Тут ключ ['tag_name'] тому, що у файлi urls.py заданий шлях <str:tag_name>
        tag_name = kwargs['tag_name']
        tag = Tag.objects.get(name=tag_name)
        notebooks_with_tag = Notebook.objects.filter(tags=tag)
        paginator = Paginator(list(notebooks_with_tag), self.notebooks_per_page)
        page = request.GET.get('page')
        try:
            notebooks_per_page = paginator.page(page)
        except PageNotAnInteger:
            notebooks_per_page = paginator.page(1)
        except EmptyPage:
            notebooks_per_page = paginator.page(paginator.num_pages)

        context = {'tag_name': tag_name,
                   'notebooks_with_tag': notebooks_per_page, }

        return render(request, self.template_name, context)
