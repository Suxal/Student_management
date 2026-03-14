from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required 
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm

@login_required
def student_list(request):
    query = request.GET.get('q', '')        # grab ?q= from URL

    students = Student.objects.filter(
        Q(first_name__icontains=query)  |
        Q(last_name__icontains=query)   |
        Q(roll_number__icontains=query) |
        Q(course__icontains=query)
    ).order_by('-enrolled_at')

    paginator = Paginator(students, 10)     # 10 students per page
    page      = request.GET.get('page')
    students  = paginator.get_page(page)    # handles invalid page numbers gracefully

    return render(request, 'students/list.html', {
        'students': students,
        'query': query,
    })

@login_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('student-list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Add Student'})

@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student-list')
    return render(request, 'students/form.html', {'form': form, 'title': 'Edit Student'})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student-list')
    return render(request, 'students/confirm_delete.html', {'student': student})