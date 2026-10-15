from django.contrib import admin
from spk.models import (
    Student,
    StudentAcademicData,
    InterestQuestion,
    StudentInterestResponse,
    TrainingRecord,
    ModelVersion,
    PredictionRun,
    RecommendationResult
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('nis', 'nama', 'kelas', 'status_pengisian', 'status_prediksi', 'created_at')
    search_fields = ('nis', 'nama')
    list_filter = ('status_pengisian', 'status_prediksi', 'kelas')


@admin.register(StudentAcademicData)
class StudentAcademicDataAdmin(admin.ModelAdmin):
    list_display = ('student', 'nilai_matematika', 'nilai_bahasa_indonesia', 'nilai_bahasa_inggris', 'nilai_ipa', 'nilai_ips', 'nilai_agama')
    search_fields = ('student__nis', 'student__nama')


@admin.register(InterestQuestion)
class InterestQuestionAdmin(admin.ModelAdmin):
    list_display = ('kode_pertanyaan', 'kelompok_minat', 'is_active', 'urutan')
    list_filter = ('kelompok_minat', 'is_active')
    search_fields = ('kode_pertanyaan', 'teks_pertanyaan')


@admin.register(StudentInterestResponse)
class StudentInterestResponseAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer_value', 'submitted_at')
    search_fields = ('student__nis', 'question__kode_pertanyaan')


@admin.register(TrainingRecord)
class TrainingRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'major_label', 'dataset_version', 'created_at')
    search_fields = ('major_label', 'dataset_version')
    list_filter = ('major_label', 'dataset_version')


@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ('version_name', 'algorithm', 'dataset_version', 'is_active', 'trained_at')
    list_filter = ('is_active', 'algorithm')


@admin.register(PredictionRun)
class PredictionRunAdmin(admin.ModelAdmin):
    list_display = ('student', 'model_version', 'status', 'completed_at')
    list_filter = ('status',)
    search_fields = ('student__nis', 'student__nama')


@admin.register(RecommendationResult)
class RecommendationResultAdmin(admin.ModelAdmin):
    list_display = ('prediction_run', 'rank', 'major_label', 'score')
    list_filter = ('rank', 'major_label')
