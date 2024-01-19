from datetime import date, timedelta

from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import AddressBook
from .forms import *
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



@login_required
def contact_list(request, page=1):
    if request.method == 'GET':
        contacts = AddressBook.objects.all()
        search_form = SearchContactForm(request.GET)
        birthday_form = BirthdayContactForm(request.POST)
        elem_per_page = 5
        paginator = Paginator(list(contacts), elem_per_page)
        contacts_on_page = paginator.page(page)
        return render(request, 'address_book/contact_list.html',
                    context={'contacts': contacts_on_page, 'search_form': search_form,
                            'birthday_form': birthday_form})


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    return render(request, 'address_book/contact_detail.html', {'contact': contact})


@login_required
def contact_add(request):
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.user = request.user
            contact.save()
            return redirect('address_book:contact_detail', pk=contact.id)
    else:
        form = AddressBookForm()
    return render(request, 'address_book/contact_add.html', {'form': form})


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(AddressBook, id=pk)
    print(type(contact.birthday), contact.birthday, end=" ; ")
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=contact)
        if request.user.is_authenticated and contact.user == request.user:
            if form.is_valid():
                updated_contact = form.save(commit=False)
                updated_contact.user = request.user
                updated_contact.save()
                messages.success(request, 'Контакт успішно оновлено.')
                return redirect(to='address_book:contact_list')
    else:
        form = AddressBookForm(instance=contact, initial={'birthday': contact.birthday})
    return render(request, 'address_book/contact_edit.html', {'form': form})


@login_required
def contact_delete(request, pk):
    contact = get_object_or_404(AddressBook, pk=pk)
    if request.method == 'POST':
        form = DeleteContactForm(request.POST)
        if request.user.is_authenticated and contact.user == request.user:
            if form['confirm_delete'].value() == "False":
                contact.delete()
                # messages.success(request, 'The Contact deleted successfully.')
                messages.success(request, 'Контакт успішно видалено.')
                return redirect(to='address_book:contact_list')
            else:
                # messages.warning(request, 'The Contact deletion cancelled.')
                messages.warning(request, 'Видалення Контакту скасовано.')
    else:
        form = DeleteContactForm()

    return render(request, 'address_book/contact_delete.html', {'pk': pk, 'contact': contact, 'form': form})


@login_required
def contact_search(request):
    if request.method == 'GET':
        form = SearchContactForm(request.GET)
        query = request.GET.get('query')

        if not query or len(query) < 3:
            messages.error(request, 'Мінімальна довжина запиту - 3 символи.')
            return redirect(to='address_book:contact_list')
        
        if form.is_valid():
            results = AddressBook.objects.filter(Q(first_name__icontains=query) |
                                                 Q(last_name__icontains=query) |
                                                 Q(address__icontains=query) |
                                                 Q(phone__icontains=query) |
                                                 Q(email__icontains=query))
            
            page = request.GET.get('page', 1)
            paginator = Paginator(results, 5)
            try:
                results_page = paginator.page(page)
            except PageNotAnInteger:
                results_page = paginator.page(1)
            except EmptyPage:
                results_page = paginator.page(paginator.num_pages)
            context = {'results': results_page, 'query': query}
            return render(request, 'address_book/contact_search.html', context)
    else:
        messages.warning(request, 'Параметри запиту пошуку незадовільні.')


@login_required
def upcoming_birthdays(request):

    if request.method == 'POST':
        form = BirthdayContactForm(request.POST)
        shift_day = request.POST.get('shift_day')

        if form.is_valid():
            today = date.today()
            end_date = today + timedelta(days=int(shift_day))

            if end_date.year == today.year:
                
                if end_date.month == today.month:
                    upcoming_birthdays_contacts = AddressBook.objects.filter(
                        Q(birthday__month=today.month, birthday__day__gte=today.day) &
                        Q(birthday__month=end_date.month, birthday__day__lte=end_date.day))
                
                else:
                    upcoming_birthdays_contacts = AddressBook.objects.filter(
                        Q(birthday__month=today.month, birthday__day__gte=today.day) |
                        Q(birthday__month__gt=today.month, birthday__month__lt=end_date.month) |
                        Q(birthday__month=end_date.month, birthday__day__lte=end_date.day))

            else:
                upcoming_birthdays_contacts = AddressBook.objects.filter(
                    Q(birthday__month=today.month, birthday__day__gte=today.day) |
                    Q(birthday__month__gt=today.month, birthday__month__lte=today.year) |
                    Q(birthday__month__lt=end_date.month) |
                    Q(birthday__month=end_date.month, birthday__day__lte=end_date.day))

            context = {'shift_day': shift_day, 'upcoming_birthdays_contacts': upcoming_birthdays_contacts}
            return render(request, 'address_book/upcoming_birthdays.html', context)
