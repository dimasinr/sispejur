"""
Management command untuk memperbaiki artifact_path di ModelVersion
dari absolute path (path lokal lama) menjadi relative path dari MEDIA_ROOT.

Jalankan di production server:
    python manage.py fix_model_paths
"""
import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from spk.models import ModelVersion


class Command(BaseCommand):
    help = 'Perbaiki artifact_path di ModelVersion dari absolute path ke relative path (dari MEDIA_ROOT)'

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        versions = ModelVersion.objects.all()

        if not versions.exists():
            self.stdout.write(self.style.WARNING('Tidak ada ModelVersion ditemukan di database.'))
            return

        fixed_count = 0
        skipped_count = 0

        for mv in versions:
            old_path = mv.artifact_path

            # Jika sudah relative path (tidak dimulai dari drive letter atau /), skip
            if not os.path.isabs(old_path):
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK] {mv.version_name}: sudah relative path -> {old_path}')
                )
                skipped_count += 1
                continue

            # Coba buat relative path dari MEDIA_ROOT
            try:
                old_path_obj = Path(old_path)
                # Ambil hanya bagian 'models/filename.joblib'
                # Cari 'models' folder dalam path
                parts = old_path_obj.parts
                if 'models' in parts:
                    models_idx = list(parts).index('models')
                    relative = Path(*parts[models_idx:])
                    new_path = str(relative).replace('\\', '/')
                else:
                    # Fallback: ambil nama file saja
                    new_path = f"models/{old_path_obj.name}"

                mv.artifact_path = new_path
                mv.save(update_fields=['artifact_path'])

                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [FIXED] {mv.version_name}:\n'
                        f'           Lama : {old_path}\n'
                        f'           Baru : {new_path}'
                    )
                )
                fixed_count += 1

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'  [ERROR] {mv.version_name}: {e}')
                )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Selesai. {fixed_count} path diperbaiki, {skipped_count} sudah benar.'
        ))
        self.stdout.write(
            f'MEDIA_ROOT production saat ini: {media_root}'
        )
        self.stdout.write(
            'Pastikan file .joblib sudah ada di folder media/models/ di server production!'
        )
