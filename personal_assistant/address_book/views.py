from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import AddressBook
from .forms import AddressBookForm, SearchContactForm
from django.utils import timezone
from django.db.models import Q


def all_contacts(request):
    return render(request, "address_book/all_contacts.html")


def contact_list(request):
    contacts = AddressBook.objects.all()
    return render(request, 'address_book/contact_list.html', {'contacts': contacts})


def contact_detail(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    return render(request, 'address_book/contact_detail.html', {'contact': contact})


def contact_add(request):
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            contact = form.save()
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = AddressBookForm()
    return render(request, 'address_book/contact_edit.html', {'form': form})


def contact_edit(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            return redirect('contact_detail', pk=contact.pk)
    else:
        form = AddressBookForm(instance=contact)
    return render(request, 'address_book/contact_edit.html', {'form': form})


def contact_delete(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    contact.delete()
    return redirect('contact_list')


def upcoming_birthdays(request, days=7):
    today = timezone.now()
    upcoming_birthdays = AddressBook.objects.filter(birthday__range=[today, today + timezone.timedelta(days=days)])
    return render(request, 'address_book/upcoming_birthdays.html', {'upcoming_birthdays': upcoming_birthdays})


def contact_search(request):
    if request.method == 'GET':
        form = SearchContactForm(request.GET)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']

            contacts = AddressBook.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(address__icontains=search_term) |
                Q(phone__icontains=search_term) |
                Q(email__icontains=search_term)
            )

            return render(request, 'address_book/contact_search_results.html',
                          {'contacts': contacts, 'search_term': search_term})
    else:
        form = SearchContactForm()

    return render(request, 'address_book/contact_search.html', {'form': form})
