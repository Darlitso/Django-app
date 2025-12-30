
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView 
from django.contrib.auth.views import LogoutView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth import login

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from django.shortcuts import redirect
    
import json

from matplotlib.pyplot import title
from shtab import complete


from .models import Task          


# Create views here

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__' 
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True 
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['completed'] = context['tasks'].filter(complete=True).count()
        context['total'] = context['tasks'].count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context 
    
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        title = request.POST.get('title').capitalize()
        if title:
            Task.objects.create(user=request.user, title=title)
        return redirect('tasks')  # Make sure 'tasks' matches URL name

    @csrf_exempt
    def delete_task(request, pk):
        if request.method == 'POST':
            task = Task.objects.get(id=pk, user=request.user)
            task.delete()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'error': 'Invalid request'}, status=400)

    # def post(self, request, *args, **kwargs):
    #     title = request.POST.get('title')
    #     if title:
    #         Task.objects.create(user=request.user, title=title)
    #     return redirect('task_list')  # or your dashboard URL name
    
    # def post(self, request):
    #     if 'task_id' in request.POST:
    #         Handle task update
    #         task_id = request.POST.get('task_id')
    #         title = request.POST.get('title')
    #         task = get_object_or_404(Task, id=task_id, user=request.user)
    #         task.title = title
    #         task.save()
    #     else:
    #         # Handle new task creation
    #         title = request.POST.get('title')
    #         if title:
    #             Task.objects.create(user=request.user, title=title)
        
    #     return redirect('task_list')  # Or whatever your dashboard URL name is




class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task 
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
    

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

# If you want a function-based delete view, define it outside the class:
# def delete_task(request, id):
   # task = get_object_or_404(Task, id=id)
    # if request.method == 'POST':
      #  task.delete()
      # return redirect('tasks')  # or wherever your list view is
    # return redirect('tasks')

# 
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Task

@csrf_exempt
def update_task(request, pk):
    if request.method == 'POST':
        data = json.loads(request.body)
        task = Task.objects.get(id=pk)
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.complete = data.get('complete', task.complete)
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'}, status=400)

# @csrf_exempt
# def update_task(request, pk):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             task = Task.objects.get(id=pk, user=request.user)  # Optional: restrict to user
#             task.title = data.get('title', task.title)
#             task.description = data.get('description', task.description)
#             task.complete = data.get('complete', task.complete)
#             task.save()
#             return JsonResponse({'status': 'success'})
#         except Exception as e:
#             return JsonResponse({'status': 'fail', 'error': str(e)}, status=400)
#     return JsonResponse({'status': 'fail'}, status=400)


