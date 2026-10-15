from django import forms
from spk.models import Student, StudentAcademicData, TrainingRecord


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['nis', 'nama', 'kelas', 'tahun_ajaran', 'status_pengisian', 'status_prediksi']
        widgets = {
            'nis': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'placeholder': 'Contoh: 2024001'
            }),
            'nama': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'placeholder': 'Nama lengkap siswa'
            }),
            'kelas': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'placeholder': 'Contoh: XII IPA 1'
            }),
            'tahun_ajaran': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'placeholder': 'Contoh: 2024/2025'
            }),
            'status_pengisian': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm'
            }),
            'status_prediksi': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm'
            }),
        }


class AcademicDataForm(forms.ModelForm):
    class Meta:
        model = StudentAcademicData
        fields = [
            'nilai_matematika',
            'nilai_bahasa_indonesia',
            'nilai_bahasa_inggris',
            'nilai_ipa',
            'nilai_ips',
            'nilai_agama'
        ]
        widgets = {
            'nilai_matematika': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
            'nilai_bahasa_indonesia': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
            'nilai_bahasa_inggris': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
            'nilai_ipa': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
            'nilai_ips': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
            'nilai_agama': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-sm',
                'step': '0.1', 'min': '0', 'max': '100'
            }),
        }


class TrainingRecordForm(forms.Form):
    major_label = forms.CharField(
        label="Label Jurusan Target",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm',
            'placeholder': 'Contoh: Teknik Informatika'
        })
    )
    dataset_version = forms.CharField(
        label="Versi Dataset",
        max_length=50,
        initial='v1.0',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm'
        })
    )
    # Nilai Rapor
    nilai_matematika = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    nilai_bahasa_indonesia = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    nilai_bahasa_inggris = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    nilai_ipa = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    nilai_ips = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    nilai_agama = forms.FloatField(initial=80.0, min_value=0, max_value=100)
    # Minat (1.0 - 5.0)
    minat_teknologi = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)
    minat_sains = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)
    minat_bisnis = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)
    minat_sosial = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)
    minat_seni = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)
    minat_pendidikan = forms.FloatField(initial=3.0, min_value=1.0, max_value=5.0)


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="File CSV Data Latih",
        widget=forms.FileInput(attrs={
            'class': 'block w-full text-sm text-slate-500 file:mr-4 file:py-2.5 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100'
        })
    )
    dataset_version = forms.CharField(
        label="Versi Dataset",
        max_length=50,
        initial='v1.0',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm'
        })
    )


class ModelTrainForm(forms.Form):
    n_estimators = forms.IntegerField(
        label="Jumlah Pohon (n_estimators)",
        initial=100,
        min_value=10,
        max_value=1000,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm'
        })
    )
    max_depth = forms.IntegerField(
        label="Kedalaman Maksimum (max_depth)",
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm',
            'placeholder': 'Biarkan kosong untuk tanpa batas (None)'
        })
    )
    test_size = forms.FloatField(
        label="Proporsi Data Uji (Test Size)",
        initial=0.2,
        min_value=0.1,
        max_value=0.5,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm',
            'step': '0.05'
        })
    )
    random_state = forms.IntegerField(
        label="Random State",
        initial=42,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm'
        })
    )
