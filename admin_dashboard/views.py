from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from users.models import CustomUser

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def dashboard_admin(request):
    total_users = CustomUser.objects.count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    return render(request, 'admin_dashboard/dashboard.html', {
        'total_users': total_users,
        'active_users': active_users
    })

@user_passes_test(is_superuser)
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/user_list.html', {'users': users})

@user_passes_test(is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'admin_dashboard/user_detail.html', {'user': user})

@user_passes_test(is_superuser)
def toggle_active(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    user.is_active = not user.is_active
    user.save()
    return redirect('user_list')

@user_passes_test(is_superuser)
def subscription_list(request):
    users = CustomUser.objects.filter(plan__isnull=False)
    return render(request, 'admin_dashboard/subscription_list.html', {'users': users})
