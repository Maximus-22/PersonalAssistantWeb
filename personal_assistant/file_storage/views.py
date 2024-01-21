from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import boto3
from botocore.exceptions import NoCredentialsError
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q


@login_required
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                description = form.cleaned_data.get('description')
                file_instance = File(
                    file=request.FILES['file'],
                    title=request.FILES['file'].name,
                    description=description,
                    user=request.user
                )

                file_instance.save()

                messages.success(request, 'Файл успішно завантажено.')
                return redirect('file_storage:all_files')
            except Exception as e:
                print(f"Помилка при збереженні файла: {e}")
                messages.error(request, f'Помилка при завантаженні файла: {e}')
        else:
            messages.error(request, 'Форма недійсна. Будь ласка, перевірте дані.')
    else:
        form = FileUploadForm()

    return render(request, 'file_storage/upload.html', {'form': form})


@login_required
def delete_file(request, file_id):
    file = get_object_or_404(File, pk=file_id)

    if file.user != request.user:
        return redirect('file_storage:all_files')

    file.delete()

    try:
        s3 = boto3.client('s3')
        s3.delete_object(Bucket='personal-assistant-for-django-project-bucket', Key=file.file.name)
    except NoCredentialsError:
        return redirect('file_storage:all_files')

    return redirect('file_storage:all_files')


@login_required
def all_files(request):
    user_files = File.objects.filter(user=request.user)
    search_query = request.GET.get('search', '')

    if search_query:
        # user_files = user_files.filter(title__icontains=search_query)
        user_files = user_files.filter(Q(title__icontains=search_query) |
                                       Q(description__icontains=search_query))

    return render(request, "file_storage/all_files.html", {'files': user_files})

