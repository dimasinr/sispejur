"""
Management command untuk memperbaiki artifact_path di ModelVersion
dari absolute path (path lokal lama, baik Windows maupun Unix) menjadi
relative path dari MEDIA_ROOT agar portabel lintas environment.

Jalankan di production server:
    python manage.py fix_model_paths
"""
import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from spk.models import ModelVersion


def _extract_relative_path(raw_path):
    """
    Ekstrak relative path (dari segmen 'models/') dari berbagai format path:
    - Windows absolute: C:\\Users\\...\\media\\models\\file.joblib
    - Unix absolute   : /home/.../media/models/file.joblib
    - Relative (baru) : models/file.joblib
    Mengembalikan string relative path seperti 'models/file.joblib', atau None jika gagal.
    """
    norm = raw_path.replace('\\', '/')
    match = re.search(r'(models/[^/].+)$', norm)
    if match:
        return match.group(1)
    # Fallback: hanya filename
    name = Path(norm).name
    if name:
        return f'models/{name}'
    return None


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

            # Deteksi Windows absolute path (C:\ atau C:/) — tidak terdeteksi os.path.isabs di Linux
            is_windows_abs = bool(re.match(r'^[A-Za-z]:[/\\]', old_path))
            is_unix_abs = (not is_windows_abs) and os.path.isabs(old_path)

            # Jika sudah relative path, skip
            if not is_windows_abs and not is_unix_abs:
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK] {mv.version_name}: sudah relative path -> {old_path}')
                )
                skipped_count += 1
                continue

            # Ekstrak relative path
            new_path = _extract_relative_path(old_path)
            if not new_path:
                self.stdout.write(
                    self.style.ERROR(f'  [ERROR] {mv.version_name}: tidak bisa ekstrak relative path dari: {old_path}')
                )
                continue

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

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Selesai. {fixed_count} path diperbaiki, {skipped_count} sudah benar.'
        ))
        self.stdout.write(f'MEDIA_ROOT production saat ini: {media_root}')
        self.stdout.write(
            'Pastikan file .joblib sudah ada di folder media/models/ di server production!'
        )
