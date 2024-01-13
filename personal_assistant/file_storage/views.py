from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import File
from django.contrib.auth.decorators import login_required


# @login_required
def file_upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                file_instance = File(
                    file=request.FILES['file'],
                    title=request.FILES['file'].name,
                    user=request.user
                )
                file_instance.save()
                messages.success(request, 'Файл успішно завантажено.')
                return redirect('file_storage:all_files')
            except Exception as e:
                messages.error(request, f'Помилка при завантаженні файла: {e}')
        else:
            messages.error(request, 'Форма недійсна. Будь ласка, перевірте дані.')
    else:
        form = FileUploadForm()

    return render(request, 'file_storage/upload.html', {'form': form})


@login_required
def all_files(request):
    files = File.objects.filter(user=request.user)
    return render(request, "file_storage/all_files.html", {'files': files})
