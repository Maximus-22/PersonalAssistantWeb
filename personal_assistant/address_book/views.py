from django.shortcuts import render


def all_contacts(request):
    return render(request, "address_book/all_contacts.html")
