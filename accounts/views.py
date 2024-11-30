from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home_view(request):
    # İstifadəçi login olubsa onu week_selection səhifəsinə yönləndir
    if request.user.is_authenticated:
        return redirect('week_selection')
    # Əks halda login səhifəsinə yönləndir
    return redirect('login')

# Login görünüşü (POST sorğusu ilə login olarsa week_selection-a yönləndir)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
import bleach  # XSS təhlükəsinə qarşı filtrasiya

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        # 1. Inputları filtr edin
        username = bleach.clean(request.POST.get('username', ''))
        password = bleach.clean(request.POST.get('password', ''))

        # 2. Autentifikasiya
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # İstifadəçini daxil edin
            login(request, user)
            return redirect('week_selection')  # Müvafiq yönləndirmə
        else:
            # Yanlış giriş cəhdi
            return render(request, 'login.html', {
                'error': 'Kullanıcı adı ve ya şifre hatalı'
            })
    else:
        return render(request, 'login.html')


def week_selection(request):
    return render(request, 'week_selection.html')

@login_required
def week_modules(request, week):
    return render(request, 'week_modules.html', {
        'week': week,
        'user': request.user,
    })




from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ClickRecord, CompletedModule, AudioFile, ModuleMedia
from django.contrib.auth.decorators import login_required
import json

# views.py
from django.shortcuts import render, get_object_or_404
from .models import ModuleMedia

@login_required
def attention_module(request, week):
    # Həftə və modul adına uyğun olaraq səs fayllarını yükləyirik
    module_media = ModuleMedia.objects.filter(week=week, module_name="İşitsel Dikkat Modülü").first()
    audio_urls = [audio_file.audio.url for audio_file in module_media.audio_files.all()] if module_media else []

    # Attention modulu tamamlanıbsa, `completed_message.html` səhifəsinə yönləndiririk
    attention_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name="İşitsel Dikkat Modülü").first()
    if attention_completed and attention_completed.completed:
        return render(request, 'completed_message.html', {
            'message': 'Modül tamamlandı',
            'week': week
        })

    # Əks halda `attention_module.html` şablonuna yönləndiririk
    return render(request, 'attention_module.html', {
        'audio_urls': audio_urls,
        'week': week,
        'user': request.user,
        'media_url': settings.MEDIA_URL,
        'attention_completed': attention_completed.completed if attention_completed else False,
    })





from django.utils import timezone
from django.http import JsonResponse
import json 

@login_required
def save_click_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        week = data['week']
        module = data['module']
        button = data['button']  # Düyməni JSON sorğudan alırıq
        click_time = data['click_time']
        
        # Əgər səs faylı varsa onu əlavə edirik, yoxdursa null saxlayırıq
        audio_file = AudioFile.objects.last()  # Dinamik olaraq seçilə bilər

        # Mövcud qeyd varsa, onu silirik
        ClickRecord.objects.filter(user=user, week=week, module=module, button=button).delete()

        # Yeni qeydi əlavə edirik
        ClickRecord.objects.create(
            user=user,
            week=week,
            module=module,
            button=button,
            click_time=click_time,
            click_date=timezone.now(),
            audio_file=audio_file
        )

        return JsonResponse({'status': 'success'})







# İstifadəçinin həftələri göstərən görünüş
def user_weeks(request, user_id):
    user = User.objects.get(id=user_id)
    weeks = ClickRecord.objects.filter(user=user).values('week').distinct()
    return render(request, 'user_weeks.html', {'user': user, 'weeks': weeks})

# İstifadəçinin müəyyən həftədəki modulları göstərən görünüş
def user_week_modules(request, user_id, week):
    user = User.objects.get(id=user_id)
    modules = ClickRecord.objects.filter(user=user, week=week).values('module').distinct()
    return render(request, 'user_week_modules.html', {'user': user, 'week': week, 'modules': modules})

# İstifadəçinin bir modulda etdiyi hərəkətləri (loglar)
def user_module_logs(request, user_id, week, module):
    user = User.objects.get(id=user_id)
    logs = ClickRecord.objects.filter(user=user, week=week, module=module)
    return render(request, 'user_module_logs.html', {'user': user, 'week': week, 'module': module, 'logs': logs})






import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import CompletedModule, ClickRecord

@login_required
def complete_module(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        week = data['week']
        module_name = data['module']
        click_data = data.get('click_data', None)  # Klik məlumatlarını yoxla, olmaya bilər

        # Həmin həftədə və moduldakı bitirmə vəziyyətini qeyd edirik
        completed_module, created = CompletedModule.objects.get_or_create(user=user, week=week, module_name=module_name)
        completed_module.completed = True
        completed_module.save()

        # Əgər klik məlumatları mövcuddursa, onları qeyd edirik
        if click_data:
            for click in click_data:
                ClickRecord.objects.create(
                    user=user,
                    week=week,
                    module=module_name,
                    click_time=click.get('click_time', 0),  # Default olaraq 0 yazırıq
                    button=click.get('button', 'N/A'),  # Default olaraq "N/A" yazırıq
                    video_index=click.get('video_index')
                )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)






from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CompletedModule, AudioFile

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import ModuleMedia, CompletedModule

@login_required
def verbal_memory_module(request, week):
    # Həftə və modul adına uyğun olaraq video fayllarını yükləyirik
    module_media = ModuleMedia.objects.filter(week=week, module_name="İşitsel sıralama modulü").first()
    
    # Debug: Video fayl sayını yoxlamaq üçün
    if module_media:
        video_count = module_media.video_files.count()
        print(f"Debug: Video fayl sayı -> {video_count}")  # Terminalda video fayl sayını göstərəcək
    
    video_urls = [video_file.video.url for video_file in module_media.video_files.all()] if module_media else []

    # Modulu tamamlayıb-tamamlamadığını yoxlayırıq
    completed_module = CompletedModule.objects.filter(user=request.user, week=week, module_name="İşitsel sıralama modulü").first()

    # Əgər modul tamamlanıbsa, `completed_message.html` səhifəsinə yönləndiririk
    if completed_module and completed_module.completed:
        return render(request, 'completed_message.html', {
            'message': 'Modül tamamlandı',
            'week': week
        })

    # Əks halda `verbal_memory_module` modul səhifəsini göstəririk
    return render(request, 'verbal_memory_module.html', {
        'video_urls': video_urls,
        'week': week,
        'user': request.user,
    })






from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt  # CSRF tokeni olmayan üçün istifadə olunur
def save_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        file_path = default_storage.save(f"audio_records/{audio_file.name}", audio_file)
        
        return JsonResponse({'status': 'success', 'file_path': file_path})
    return JsonResponse({'status': 'error', 'message': 'Səs qeydi alınmadı.'}, status=400)


from django.http import HttpResponse
from django.conf import settings
import os

@login_required
def işitsel_sozel_module_view(request, week):
    # Media qovluğundakı səs faylının URL-i
    # audio_url = os.path.join(settings.MEDIA_URL, 'audio/Sinan_Akçıl__Ferah_Zeydan_-_Hadi_Yavrum_J2nu8Rw.mp3')  # Səs faylını buraya əlavə edirsən

    # Modulun tamamlanma vəziyyətini yoxlayırıq
    completed_module = CompletedModule.objects.filter(user=request.user, week=week, module_name='İşitsel-sözel modulü').first()
    
    # Əgər modul tamamlanıbsa, `complete_message.html` səhifəsinə yönləndiririk
    if completed_module and completed_module.completed:
        return render(request, 'completed_message.html', {
            'message': 'Modül tamamlandı',
            'week': week  # `week` dəyərini şablona göndəririk ki, geri dönmək üçün istifadə olunsun
        })

    # Əks halda `işitsel_sozel` modul səhifəsini göstəririk
    return render(request, 'auditory_verbal.html', { 
        # 'audio_url': audio_url,  # Audio faylının URL-i
        'week': week,  # Həftə dəyəri
        'user': request.user,  # İstifadəçi məlumatı
    })




from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from .models import CompletedModule

# Çalışma Belleği ana səhifəsi
from django.conf import settings
import os

@login_required
def calisma_bellegi_view(request, week):
    # Basit və Karmaşık modulları üçün tamamlanmış vəziyyəti yoxlayırıq
    basit_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='Basit Çalışma Belleği Modülü').first()
    karmaşik_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='Karmaşık Çalışma Belleği Modülü').first()
    
    return render(request, 'working_memory.html', {
        'week': week,
        'basit_completed': basit_completed.completed if basit_completed else False,
        'karmaşik_completed': karmaşik_completed.completed if karmaşik_completed else False,
        'video_url': '/media/video/video.mp4'  # Video üçün media yolu
    })

@login_required
def basit_calisma_view(request, week):
    basit_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='Basit Çalışma Belleği Modülü').first()
    if basit_completed and basit_completed.completed:
        return render(request, 'completed_message.html', {'message': 'Modül tamamlandı'})

    return render(request, 'basit_calisma.html', {'week': week})

@login_required
def karmasik_calisma_view(request, week):
    # Həftə və modul adına uyğun olaraq video fayllarını yükləyirik
    module_media = ModuleMedia.objects.filter(week=week, module_name="Karmaşık Çalışma Belleği Modülü").first()
    video_urls = [video_file.video.url for video_file in module_media.video_files.all()] if module_media else []

    # Modulu tamamlayıb-tamamlamadığını yoxlayırıq
    karmaşik_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='Karmaşık Çalışma Belleği Modülü').first()
    if karmaşik_completed and karmaşik_completed.completed:
        return render(request, 'completed_message.html', {'message': 'Modül tamamlandı'})

    return render(request, 'karmasik_calisma.html', {
        'week': week,
        'video_urls': video_urls  # Video URL-ləri şablona ötürürük
    })




def işitsel_bellek_view(request, week):
    # İşitsel Bellek modulu tamamlanıbsa yoxlayırıq
    işitsel_bellek_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='İşitsel-bellek modülü').first()

    if işitsel_bellek_completed and işitsel_bellek_completed.completed:
        return render(request, 'completed_message.html', {
            'message': 'Modül tamamlandı',
            'week': week
        })

    # İşitsel Bellek Modulu üçün səs fayllarını yükləyirik
    module_media = ModuleMedia.objects.filter(week=week, module_name="İşitsel-bellek modülü").first()
    
    if module_media:
        audio_urls = [audio_file.audio.url for audio_file in module_media.audio_files.all()]
    else:
        audio_urls = []

    return render(request, 'işitsel_bellek.html', {
        'audio_urls': audio_urls,
        'week': week,
        'user': request.user,
        'işitsel_bellek_completed': işitsel_bellek_completed.completed if işitsel_bellek_completed else False,

    })






@login_required
def işitsel_zemin_view(request, week):
    # İşitsel Zemin modulu tamamlanıbsa yoxlayırıq
    işitsel_zemin_completed = CompletedModule.objects.filter(user=request.user, week=week, module_name='Figür-zemin modülü').first()
    
    if işitsel_zemin_completed and işitsel_zemin_completed.completed:
        return render(request, 'completed_message.html', {
            'message': 'Modül tamamlandı',
            'week': week  # `week` parametrini şablona göndəririk
        })

    # İşitsel Zemin Modulu üçün səs fayllarını yükləyirik
    module_media = ModuleMedia.objects.filter(week=week, module_name="Figür-zemin modülü").first()
    
    if module_media:
        audio_urls = [audio_file.audio.url for audio_file in module_media.audio_files.all()]
    else:
        audio_urls = []

    return render(request, 'işitsel_zemin.html', {
        'audio_urls': audio_urls,
        'week': week,
        'user': request.user,
        'işitsel_zemin_completed': işitsel_zemin_completed.completed if işitsel_zemin_completed else False,
    })




#####admin####

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Yalnız admin (staff) istifadəçilər giriş edə bilər
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "İcazəsiz giriş və ya yalnış məlumat.")
    return render(request, 'admin_login.html')


from django.contrib import messages

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "Bu səhifəyə daxil olmaq icazəniz yoxdur.")
        return redirect('admin_login')
    
    return render(request, 'admin_dashboard.html')


from .models import User
@login_required
def users_list(request):
    users = User.objects.all()  # Bütün istifadəçiləri çəkirik
    return render(request, 'user_management.html', {'users': users})

from django.shortcuts import get_object_or_404, redirect, render
@csrf_exempt
@login_required
def create_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({'status': 'success', 'message': 'İstifadəçi yaradıldı'})
        else:
            return JsonResponse({'status': 'error', 'message': 'İstifadəçi adı və şifrə tələb olunur'})

    return JsonResponse({'status': 'error', 'message': 'Yalnış metod'})

# İstifadəçi düzəlişi funksiyası
@csrf_exempt
@login_required
def edit_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        data = json.loads(request.body)
        username = data.get('username', user.username)
        password = data.get('password', None)

        user.username = username
        if password:
            user.set_password(password)  # şifrəni yenilə
        user.save()

        return JsonResponse({'status': 'success', 'message': 'İstifadəçi yeniləndi'})

    return JsonResponse({'status': 'error', 'message': 'Yalnış metod'})

# İstifadəçi silmə funksiyası
@csrf_exempt
@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return JsonResponse({'status': 'success', 'message': 'İstifadəçi silindi'})

    return JsonResponse({'status': 'error', 'message': 'Yalnış metod'})



from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import User, ModuleResult, WeekResult
from .models import ModuleResult


def module_results(request):
    users = User.objects.all()
    return render(request, 'module_results.html', {"users": users})

def user_weeks(request, user_id):
    user = get_object_or_404(User, id=user_id)
    weeks = [{"number": i, "status": "completed" if i % 2 == 0 else "incomplete"} for i in range(1, 9)]
    return JsonResponse({"weeks": weeks})

# # week_modules_admin funksiyasını yenidən tərtib edin ki, həm `completedmodule` cədvəlindən, həm də `moduleresult` cədvəlindən məlumatları alsın.
# def week_modules_admin(request, user_id, week):
#     user = get_object_or_404(User, id=user_id)
#     # Həm completedmodule, həm də moduleresult cədvəlindəki məlumatları çəkin
#     modules = ModuleResult.objects.filter(user=user, week=week)
#     completed_modules = CompletedModule.objects.filter(user=user, week=week)

#     # Hər iki cədvəldən məlumatları birləşdirin
#     modules_data = [{"id": module.id, "name": module.name, "status": module.status, "user_id": user.id} for module in modules]
#     completed_data = [{"id": module.id, "name": module.module_name, "status": "Tamamlandı", "user_id": user.id} for module in completed_modules]


    
#     # Birləşdirilmiş siyahını qaytarın
#     return JsonResponse({"modules": modules_data + completed_data})
def week_modules_admin(request, user_id, week):
    """Admin üçün həftəlik modulları qaytarır."""
    user = get_object_or_404(User, id=user_id)
    modules = get_modules_for_week(user_id, week)
    return JsonResponse({"modules": modules})






from django.template.loader import render_to_string
import pdfkit
def download_results_pdf(request, user_id):
    user = get_object_or_404(User, id=user_id)
    module_results = ModuleResult.objects.filter(user=user)
    html = render_to_string("module_results_pdf.html", {"user": user, "module_results": module_results})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="module_results_{user.username}.pdf"'
    return response


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ModuleMedia, AudioFile, VideoFile
from django.contrib.auth.decorators import login_required

@login_required
def audio_and_video_change(request):
    if request.method == 'POST':
        week = request.POST.get('week')
        module_name = request.POST.get('module_name')
        
        # Müəyyən həftə və modul üçün media obyektini əldə edin və ya yaradın
        media, _ = ModuleMedia.objects.get_or_create(week=week, module_name=module_name)

        # Bu modul üçün mövcud olan bütün köhnə səsləri silirik
        if media.audio_files.count() > 0:
            for audio in media.audio_files.all():
                # Faylı fiziki olaraq silirik
                if audio.audio:
                    audio.audio.delete(save=False)
                # Database-dən səs obyektini silirik
                audio.delete()
            media.audio_files.clear()

        # Yeni audio faylları əlavə edirik
        for i in range(1, 11):  # Maksimum 10 səs faylı üçün
            audio_file = request.FILES.get(f'audio_file_{i}')
            if audio_file:
                audio_instance = AudioFile.objects.create(audio=audio_file)
                media.audio_files.add(audio_instance)

        # Video faylları üçün köhnə videoları silirik
        if media.video_files.count() > 0:
            for video in media.video_files.all():
                if video.video:
                    video.video.delete(save=False)
                video.delete()
            media.video_files.clear()

        # Yeni video faylları əlavə edirik
        for i in range(1, 5):  # Maksimum 3 video faylı üçün
            video_file = request.FILES.get(f'video_file_{i}')
            if video_file:
                video_instance = VideoFile.objects.create(video=video_file)
                media.video_files.add(video_instance)

        media.save()
        messages.success(request, f"{module_name} modulu üçün media faylları uğurla yeniləndi!")

        return redirect('audio_and_video_change')

    # Seçim üçün mövcud həftə və modullar
    weeks = ModuleMedia.objects.values_list('week', flat=True).distinct().order_by('week')
    modules = [
        'İşitsel dikkat modülü',
        'İşitsel sıralama modulü',
        'Karmaşık Çalışma Belleği Modülü',
        'İşitsel-bellek modülü',
        'Figür-zemin modülü'
    ]

    return render(request, 'audio_and_video_change.html', {
        'weeks': weeks,
        'modules': modules,
    })




from .models import ModuleMedia

def populate_modulemedia():
    module_names = [
        'İşitsel dikkat modülü',
        'İşitsel sıralama modulü',
        'Çalışma belleği modülü',
        'İşitsel-bellek modülü',
        'Figür-zemin modülü'
    ]
    
    weeks = range(1, 9)  # Hər həftə üçün

    # Hər həftə üçün lazımlı modulları yarat
    for week in weeks:
        for module_name in module_names:
            ModuleMedia.objects.get_or_create(week=week, module_name=module_name)
    
    print("ModuleMedia cədvəli yenidən yaradıldı və məlumatlarla dolduruldu.")


from django.http import JsonResponse
from .models import KarmasikCalismaClickRecord

@login_required
def save_click_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        week = data['week']
        module_name = data['module']
        video_1_clicks = data.get('video_1_clicks', 0)
        video_2_clicks = data.get('video_2_clicks', 0)
        video_3_clicks = data.get('video_3_clicks', 0)

        # Yeni klik məlumatlarını saxlayırıq
        KarmasikCalismaClickRecord.objects.create(
            week=week,
            module=module_name,
            video_1_clicks=video_1_clicks,
            video_2_clicks=video_2_clicks,
            video_3_clicks=video_3_clicks,
            user=request.user
        )

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)




from .models import KarmasikCalismaAudioRecord
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def save_audio_karmasik(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        week = request.POST.get('week', 1)  # Həftə dəyərini POST məlumatından alın
        audio_file = request.FILES['audio']
        
        # Səs qeydini bazaya əlavə et
        audio_record = KarmasikCalismaAudioRecord.objects.create(
            user=request.user,
            week=week,
            audio_file=audio_file
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Səs qeydi əlavə olunmadı.'})


from .models import BasitCalismaAudioRecord
@csrf_exempt
@login_required
def save_basit_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        week = request.POST.get('week', 1)  # Həftə dəyərini POST məlumatından alın
        audio_file = request.FILES['audio']
        
        # Səs qeydini bazaya əlavə et
        audio_record = BasitCalismaAudioRecord.objects.create(
            user=request.user,
            week=week,
            audio_file=audio_file
        )
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Səs qeydi əlavə olunmadı.'})


from .models import IsitselZeminAudioRecord

from django.http import JsonResponse
from .models import IsitselZeminAudioRecord
from django.contrib.auth.decorators import login_required

@login_required
def save_audio_zemin(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        week = request.POST.get('week')
        module_name = request.POST.get('module_name')
        audio_file = request.FILES['audio']
        ses_index = int(request.POST.get('ses_index'))  # Dinlənən səsin nömrəsi (1-10 arası)
        user = request.user

        # Mövcud `IsitselZeminAudioRecord` qeydini əldə edin və ya yaradın
        audio_record, _ = IsitselZeminAudioRecord.objects.get_or_create(
            user=user, week=week, module_name=module_name
        )

        # Səsi dəyişmədən əvvəl eyni `ses_index` üçün köhnə faylı silirik
        field_name = f"ses{ses_index}"
        existing_audio = getattr(audio_record, field_name)
        if existing_audio:
            # Köhnə faylı həm serverdən, həm də modeldən silirik
            existing_audio.delete(save=False)

        # Yeni faylı uyğun sahəyə əlavə edirik və yadda saxlayırıq
        setattr(audio_record, field_name, audio_file)
        audio_record.save()

        return JsonResponse({'status': 'success', 'message': f'Səs {ses_index} qeydi saxlanıldı.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Səs qeydi alınmadı.'})


from .models import IsitselBellekAudioRecord
@login_required
def save_audio_isitsel_bellek(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        week = request.POST.get('week')
        module_name = request.POST.get('module_name')
        audio_file = request.FILES['audio']
        ses_index = int(request.POST.get('ses_index'))  # Dinlənən səsin nömrəsi (1-10 arası)
        user = request.user

        # Mövcud `IsitselZeminAudioRecord` qeydini əldə edin və ya yaradın
        audio_record, _ = IsitselBellekAudioRecord.objects.get_or_create(
            user=user, week=week, module_name=module_name
        )

        # Səsi dəyişmədən əvvəl eyni `ses_index` üçün köhnə faylı silirik
        field_name = f"ses{ses_index}"
        existing_audio = getattr(audio_record, field_name)
        if existing_audio:
            # Köhnə faylı həm serverdən, həm də modeldən silirik
            existing_audio.delete(save=False)

        # Yeni faylı uyğun sahəyə əlavə edirik və yadda saxlayırıq
        setattr(audio_record, field_name, audio_file)
        audio_record.save()

        return JsonResponse({'status': 'success', 'message': f'Səs {ses_index} qeydi saxlanıldı.'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Səs qeydi alınmadı.'})
    



from .models import VerbalMemoryRecording

@login_required
def save_verbal_audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        print("Audio faylı daxil oldu:", request.FILES['audio'])
        print("POST məlumatları:", request.POST)
        user = request.user
        week = request.POST.get('week')
        module_name = request.POST.get('module_name')  # Modulun adı
        phase = request.POST.get('phase')  # Hər faza üçün nömrə
        audio_file = request.FILES['audio']
        print("Audio file:", audio_file)
        print("User:", user)
        print("Week:", week)
        print("Module Name:", module_name)
        print("Phase:", phase)

        # VerbalMemoryRecording modelinə audio faylını əlavə edirik
        VerbalMemoryRecording.objects.create(
            user=user,
            week=week,
            module_name=module_name,
            phase=phase,
            audio_file=audio_file
        )
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})
    


# views.py

from django.http import JsonResponse, HttpResponseNotFound
from django.contrib.auth.models import User
from django.views.decorators.http import require_GET

@require_GET
def search_users(request):
    query = request.GET.get('q', '').strip()
    if query:
        users = User.objects.filter(username__icontains=query).values('id', 'username')
        results = list(users)
    else:
        results = list(User.objects.values('id', 'username'))  # bütün istifadəçiləri göstərir

    return JsonResponse({'results': results})



# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotFound
from .models import (
    ClickRecord, CompletedModule, VerbalMemoryRecording,
    BasitCalismaAudioRecord, KarmasikCalismaAudioRecord,
    KarmasikCalismaClickRecord, IsitselBellekAudioRecord,
    IsitselZeminAudioRecord
)

# Modul adlarının xəritəsi
MODULE_MAPPING = {
        1: 'İşitsel Dikkat Modülü',
        2: 'İşitsel sıralama modulü',
        3: 'İşitsel-sözel modulü',
        4: 'Basit Çalışma Belleği Modülü',
        5: 'Karmaşık Çalışma Belleği Modülü',
        6: 'İşitsel-Bellek Modülü',
        7: 'Figür-Zemin Modülü',
}

def get_module_name(module_id):
    """Modul ID-dən adını qaytarır."""
    return MODULE_MAPPING.get(module_id, 'Bilinməyən Modul')

def module_details(request, user_id, week, module_id):
    module_name = get_module_name(module_id)

    if module_name == 'Bilinməyən Modul':
        return HttpResponseNotFound("Modul tapılmadı")

    # Tamamlanma tarixini tap
    completion_info = CompletedModule.objects.filter(
        user_id=user_id, week=week, module_name=module_name
    ).first()

    # Məlumatlar konteksi
    context = {
        'module_name': module_name,
        'module_id': module_id,
        'week': week,
        'completion_date': completion_info.completion_date if completion_info else None,
    }

    # Modul növlərinə görə məlumatlar
    if module_id in [1, 2]:  # İşitsel Dikkat Modülü və İşitsel sıralama modulü
        clicks = ClickRecord.objects.filter(user_id=user_id, week=week, module=module_name)
        context['clicks'] = clicks

    # İşitsel-sözel modulü
    if module_id == 3:
        phase_1_audios = VerbalMemoryRecording.objects.filter(user_id=user_id, week=week, phase=1)
        phase_2_audios = VerbalMemoryRecording.objects.filter(user_id=user_id, week=week, phase=2)
        context['phase_1_audios'] = phase_1_audios
        context['phase_2_audios'] = phase_2_audios

    # Çalışma Belleği Modülü
    if module_id == 4:
        audio_files = BasitCalismaAudioRecord.objects.filter(user_id=user_id, week=week)
        context['audio_files'] = audio_files

    # Karmaşık çalışma belleği modulü
    if module_id == 5:
        audio_files = KarmasikCalismaAudioRecord.objects.filter(user_id=user_id, week=week, module='karmaşik_calisma')
        print("Debug: Audio files:", [audio.audio_file.url for audio in audio_files])
        click_data = KarmasikCalismaClickRecord.objects.filter(user_id=user_id, week=week).first()
        context['audio_files'] = audio_files
        context['click_data'] = click_data


    # İşitsel-Bellek Modülü
    if module_id == 6:
        audio_records = IsitselBellekAudioRecord.objects.filter(user_id=user_id, week=week)
        context['audio_records'] = audio_records

    # Figür-Zemin Modülü
    if module_id == 7:
        audio_records = IsitselZeminAudioRecord.objects.filter(user_id=user_id, week=week)
        context['audio_records'] = audio_records

    # Modulun tamamlanma tarixini əlavə edin
    completion_info = CompletedModule.objects.filter(user_id=user_id, week=week, module_name=module_name).first()
    context['completion_date'] = completion_info.completion_date if completion_info else None

    return render(request, 'module_result_detail.html', context)





def get_modules_for_week(user_id, week):
    """Həftə və istifadəçiyə görə mövcud modulları qaytarır."""
    MODULE_MAPPING = {
        1: 'İşitsel Dikkat Modülü',
        2: 'İşitsel sıralama modulü',
        3: 'İşitsel-sözel modulü',
        4: 'Basit Çalışma Belleği Modülü',
        5: 'Karmaşık Çalışma Belleği Modülü',
        6: 'İşitsel-Bellek Modülü',
        7: 'Figür-Zemin Modülü',
    }

    modules = []
    for module_id, module_name in MODULE_MAPPING.items():
        status = "Tamamlandı" if CompletedModule.objects.filter(user_id=user_id, week=week, module_name=module_name).exists() else "Tamamlanmayıb"
        modules.append({
            "id": module_id,
            "name": module_name,
            "status": status,
        })

    return modules


def get_modules(request, user_id, week):
    """Həftə və istifadəçiyə görə modulları qaytarır."""
    modules = get_modules_for_week(user_id, week)
    return JsonResponse({'modules': modules})
