from django.shortcuts import render
from .models import ClickRecord
from django.contrib.auth.models import User

def admin_view_click_times(request, user_id, week):
    # Seçilmiş istifadəçinin klik məlumatları
    user = User.objects.get(id=user_id)
    click_records = ClickRecord.objects.filter(user=user, week=week, module='attention').order_by('click_time')

    return render(request, 'admin_click_times.html', {
        'user': user,
        'week': week,
        'click_records': click_records
    })
