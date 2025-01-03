from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ClickRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    module = models.CharField(max_length=50)
    button = models.CharField(max_length=50)  # Yeni düymə sahəsi əlavə edilir
    click_time = models.FloatField(null=True,blank=True)  # Saniyə olaraq klik zamanı
    click_date = models.DateTimeField(default=timezone.now)
    video_index = models.IntegerField(null=True, blank=True)
    audio_index = models.IntegerField(null=True, blank=True)
    audio_file = models.ForeignKey('AudioFile', null=True, blank=True, on_delete=models.SET_NULL)  # Səs faylı
    answers = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f'{self.user.username} - {self.module} - {self.button} - {self.click_time} saniyə'



class AudioFile(models.Model):
    title = models.CharField(max_length=255)  # Səs faylının adı
    audio = models.FileField(upload_to='module_audios/')  # Səs faylı yükləmə sahəsi
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VideoFile(models.Model):
    title = models.CharField(max_length=255)  # Video faylının adı
    video = models.FileField(upload_to='module_videos/')  # Video faylı yükləmə sahəsi
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class CompletedModule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    module_name = models.CharField(max_length=100)  # Modulun adı
    completed = models.BooleanField(default=False)  # Modul bitib-bitmədiyini saxlamaq üçün
    completion_date = models.DateTimeField(auto_now_add=True)  # Tamamlanma tarixi
    result = models.TextField(null=True, blank=True)  # Modul nəticələri (təhlil)

    def __str__(self):
        return f"{self.user.username} - Həftə: {self.week} - {self.module_name} - Bitirildi: {self.completed}"




class WeekResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    completed = models.BooleanField(default=False)

    def to_json(self):
        return {'week': self.week, 'completed': self.completed}

class ModuleResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    date = models.DateTimeField()
    audio_url = models.URLField(blank=True, null=True)
    details = models.TextField()

    def to_json(self):
        return {'id': self.id, 'name': self.name, 'status': self.status, 'date': self.date.strftime('%Y-%m-%d')}

    def to_detailed_json(self):
        return {'name': self.name, 'status': self.status, 'date': self.date.strftime('%Y-%m-%d %H:%M:%S'), 'details': self.details, 'audio_url': self.audio_url}



from django.db import models

class ModuleMedia(models.Model):
    week = models.IntegerField()
    module_name = models.CharField(max_length=100)
    task_text = models.TextField(null=True, blank=True)
    audio_files = models.ManyToManyField(AudioFile, blank=True)  # Çoxlu səs faylı üçün
    video_files = models.ManyToManyField(VideoFile, blank=True)  # Çoxlu video faylı üçün

    def __str__(self):
        return f"Həftə {self.week} - {self.module_name}"

class KarmasikCalismaClickRecord(models.Model):
    week = models.IntegerField()
    module= models.CharField(max_length=100)  # Modul adı üçün
    video_1_clicks = models.IntegerField(default=0)  # 1-ci videonun klik sayı
    video_2_clicks = models.IntegerField(default=0)  # 2-ci videonun klik sayı
    video_3_clicks = models.IntegerField(default=0)  # 3-cü videonun klik sayı
    click_date = models.DateTimeField(auto_now_add=True)  # Klik tarixi
    video_file_id = models.ForeignKey(VideoFile, null=True, blank=True, on_delete=models.SET_NULL)  # boş ola bilər
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # İstifadəçi

    def __str__(self):
        return f"Həftə {self.week} - Modul {self.module} - {self.user.username}"


class KarmasikCalismaAudioRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    module = models.CharField(max_length=255, default='karmaşik_calisma')
    audio_file = models.FileField(upload_to='karmasik_calisma_audio/')
    recorded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Həftə {self.week} - {self.module}"
    

class BasitCalismaAudioRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    module = models.CharField(max_length=255, default='basit_calisma')
    audio_file = models.FileField(upload_to='basit_calisma_audio/')
    recorded_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Həftə {self.week} - {self.module}"
    
class IsitselZeminAudioRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()  # Həftə məlumatı
    module_name = models.CharField(max_length=100)  # Modul adı
    ses1 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 1 üçün fayl
    ses2 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 2 üçün fayl
    ses3 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 3 üçün fayl
    ses4 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 4 üçün fayl
    ses5 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 5 üçün fayl
    ses6 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 6 üçün fayl
    ses7 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 7 üçün fayl
    ses8 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 8 üçün fayl
    ses9 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 9 üçün fayl
    ses10 = models.FileField(upload_to='isitsel_zemin_audio_records/', blank=True, null=True)  # Səs 10 üçün fayl
    recorded_at = models.DateTimeField(auto_now_add=True)  # Qeyd olunma tarixi

    def __str__(self):
        return f"{self.user.username} - {self.module_name} - Həftə {self.week} - {self.recorded_at}" 
    


class IsitselBellekAudioRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()  # Həftə məlumatı
    module_name = models.CharField(max_length=100)  # Modul adı
    ses1 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 1 üçün fayl
    ses2 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 2 üçün fayl
    ses3 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 3 üçün fayl
    ses4 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 4 üçün fayl
    ses5 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 5 üçün fayl
    ses6 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 6 üçün fayl
    ses7 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 7 üçün fayl
    ses8 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 8 üçün fayl
    ses9 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 9 üçün fayl
    ses10 = models.FileField(upload_to='isitsel_bellek_audio_records/', blank=True, null=True)  # Səs 10 üçün fayl
    recorded_at = models.DateTimeField(auto_now_add=True)  # Qeyd olunma tarixi

    def __str__(self):
        return f"{self.user.username} - {self.module_name} - Həftə {self.week} - {self.recorded_at}" 
    



class VerbalMemoryRecording(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    week = models.IntegerField()
    module_name = models.CharField(max_length=100)  # Modulun adı
    phase = models.IntegerField()  # 1, 2, və ya 3-cü aşama
    audio_file = models.FileField(upload_to='verbal_memory_recordings/')
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.module_name} - Week {self.week} - Phase {self.phase}"
    



class Question(models.Model):
    week = models.IntegerField()
    module_name = models.CharField(max_length=50)
    question_text = models.TextField()
    audio_file = models.ForeignKey(AudioFile, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"{self.module_name} - Həftə {self.week} - Audio: {self.audio_index}: {self.question_text}"
