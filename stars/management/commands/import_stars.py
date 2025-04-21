import json
from django.core.management.base import BaseCommand
from constellations.models import Constellation
from stars.models import Star


class Command(BaseCommand):
    help = 'Load constellations and stars from JSON files'

    def add_arguments(self, parser):
        parser.add_argument('constellations_file', type=str,
                            help='Path to constellations.json')
        parser.add_argument('stars_file', type=str, help='Path to stars.json')

    def handle(self, *args, **options):
        with open(options['constellations_file'], encoding='utf-8') as f:
            constellations_data = json.load(f)

        with open(options['stars_file'], encoding='utf-8') as f:
            stars_data = json.load(f)

        constellation_map = {}

        # 1. Create constellations
        for c in constellations_data:
            constellation, _ = Constellation.objects.get_or_create(
                name=c['name'],
                defaults={
                    'description': c.get('description', ''),
                    'connections': c.get('connections', [])
                }
            )
            constellation_map[constellation.name] = constellation
            self.stdout.write(self.style.SUCCESS(
                f"✅ Constellation: {constellation.name}"))

        # 2. Create stars
        for s in stars_data:
            constellation = constellation_map.get(s['constellation'])
            if not constellation:
                self.stdout.write(self.style.ERROR(
                    f"❌ 별자리를 찾을 수 없음: {s['constellation']}"))
                continue

            star, created = Star.objects.get_or_create(
                name=s['name'],
                constellation=constellation,
                defaults={
                    'ra': s['ra'],
                    'dec': s['dec'],
                    'magnitude': s.get('magnitude'),
                    'spectral_type': s.get('spectral_type'),
                }
            )
            status = "🆕 created" if created else "⚠️ exists"
            self.stdout.write(
                f"{status} ⭐ {star.name} in {constellation.name}")
