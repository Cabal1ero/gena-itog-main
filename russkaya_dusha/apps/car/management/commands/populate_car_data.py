from django.core.management.base import BaseCommand
from apps.car.models import CarBrand, CarModel, Equipment, EquipmentFeature, ModelImage
from django.core.files.base import ContentFile
import requests

class Command(BaseCommand):
    help = 'Populates the database with a car model and three equipments'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to populate the database...")

        # 1. Создание марки LADA
        brand, created = CarBrand.objects.get_or_create(
            name='LADA',
            defaults={
                'description': 'Российская марка автомобилей, производящаяся на АвтоВАЗе.',
                'country': 'Россия'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created CarBrand: {brand.name}'))
        else:
            self.stdout.write(f'CarBrand "{brand.name}" already exists.')

        # 2. Создание модели LADA Vesta
        car_model, created = CarModel.objects.get_or_create(
            brand=brand,
            name='Vesta',
            defaults={
                'body_type': 'sedan',
                'base_price': 1500000,
                'engine_volume': 1.6,
                'power': 106,
                'transmission': 'manual',
                'fuel_type': 'petrol',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created CarModel: {car_model}'))
            # Добавим основное изображение для модели
            try:
                response = requests.get("http://placehold.co/600x400/cccccc/000000?text=LADA+Vesta", stream=True)
                if response.status_code == 200:
                    car_model.image.save('vesta_main.png', ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  - Added main image for {car_model.name}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Could not download image: {e}"))

        else:
            self.stdout.write(f'CarModel "{car_model}" already exists.')

        # 3. Создание комплектаций
        self.create_equipments(car_model)

        # --- LADA Granta ---
        granta_model, created = CarModel.objects.get_or_create(
            brand=brand,
            name='Granta',
            defaults={
                'body_type': 'sedan',
                'base_price': 900000,
                'engine_volume': 1.6,
                'power': 90,
                'transmission': 'manual',
                'fuel_type': 'petrol',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created CarModel: {granta_model}'))
            try:
                response = requests.get("http://placehold.co/600x400/cccccc/000000?text=LADA+Granta", stream=True)
                if response.status_code == 200:
                    granta_model.image.save('granta_main.png', ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  - Added main image for {granta_model.name}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Could not download image: {e}"))
        else:
            self.stdout.write(f'CarModel "{granta_model}" already exists.')
        self.create_equipments(granta_model, [
            {
                'name': 'Standard',
                'equipment_type': 'standard',
                'price': 950000,
                'power': 90,
                'features': {
                    'Комфорт': ['Электростеклоподъемники передние'],
                    'Безопасность': ['ABS', '2 подушки безопасности'],
                    'Мультимедиа': ['Аудиоподготовка'],
                },
                'image_url': 'http://placehold.co/600x400/E0E0E0/000000?text=Granta+Standard'
            },
            {
                'name': 'Classic',
                'equipment_type': 'comfort',
                'price': 1050000,
                'power': 90,
                'features': {
                    'Комфорт': ['Кондиционер', 'Подогрев передних сидений'],
                    'Безопасность': ['ABS', '2 подушки безопасности'],
                    'Мультимедиа': ['Аудиосистема с USB'],
                },
                'image_url': 'http://placehold.co/600x400/A0A0A0/FFFFFF?text=Granta+Classic'
            },
            {
                'name': 'Life',
                'equipment_type': 'luxury',
                'price': 1200000,
                'power': 106,
                'transmission': 'automatic',
                'features': {
                    'Комфорт': ['Климат-контроль', 'Подогрев руля'],
                    'Безопасность': ['ABS, ESP', '4 подушки безопасности'],
                    'Мультимедиа': ['Мультимедийная система с 7\" экраном'],
                    'Экстерьер': ['Литые диски 15\"'],
                },
                'image_url': 'http://placehold.co/600x400/FFCC00/000000?text=Granta+Life'
            }
        ])

        # --- LADA Kalina ---
        kalina_model, created = CarModel.objects.get_or_create(
            brand=brand,
            name='Kalina',
            defaults={
                'body_type': 'wagon',
                'base_price': 850000,
                'engine_volume': 1.6,
                'power': 87,
                'transmission': 'manual',
                'fuel_type': 'petrol',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created CarModel: {kalina_model}'))
            try:
                response = requests.get("http://placehold.co/600x400/cccccc/000000?text=LADA+Kalina", stream=True)
                if response.status_code == 200:
                    kalina_model.image.save('kalina_main.png', ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  - Added main image for {kalina_model.name}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Could not download image: {e}"))
        else:
            self.stdout.write(f'CarModel "{kalina_model}" already exists.')
        self.create_equipments(kalina_model, [
            {
                'name': 'Standard',
                'equipment_type': 'standard',
                'price': 870000,
                'power': 87,
                'features': {
                    'Комфорт': ['Электроусилитель руля', 'Регулировка рулевой колонки по высоте'],
                    'Безопасность': ['ABS', 'Подушка безопасности водителя'],
                    'Мультимедиа': ['Бортовой компьютер'],
                },
                'image_url': 'http://placehold.co/600x400/E0E0E0/000000?text=Kalina+Standard'
            },
            {
                'name': 'Comfort',
                'equipment_type': 'comfort',
                'price': 950000,
                'power': 98,
                'features': {
                    'Комфорт': ['Кондиционер', 'Обогрев передних сидений'],
                    'Безопасность': ['ABS', '2 подушки безопасности'],
                    'Мультимедиа': ['Аудиосистема с USB'],
                },
                'image_url': 'http://placehold.co/600x400/A0A0A0/FFFFFF?text=Kalina+Comfort'
            },
            {
                'name': 'Luxe',
                'equipment_type': 'luxury',
                'price': 1050000,
                'power': 106,
                'transmission': 'automatic',
                'features': {
                    'Комфорт': ['Климат-контроль', 'Подогрев руля', 'Датчики дождя и света'],
                    'Безопасность': ['ABS, ESP', '4 подушки безопасности'],
                    'Мультимедиа': ['Мультимедийная система с 7\" экраном'],
                    'Экстерьер': ['Литые диски 15\"'],
                },
                'image_url': 'http://placehold.co/600x400/FFCC00/000000?text=Kalina+Luxe'
            }
        ])

        # --- LADA Largus ---
        largus_model, created = CarModel.objects.get_or_create(
            brand=brand,
            name='Largus',
            defaults={
                'body_type': 'wagon',
                'base_price': 1200000,
                'engine_volume': 1.6,
                'power': 90,
                'transmission': 'manual',
                'fuel_type': 'petrol',
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully created CarModel: {largus_model}'))
            try:
                response = requests.get("http://placehold.co/600x400/cccccc/000000?text=LADA+Largus", stream=True)
                if response.status_code == 200:
                    largus_model.image.save('largus_main.png', ContentFile(response.content), save=True)
                    self.stdout.write(self.style.SUCCESS(f'  - Added main image for {largus_model.name}'))
            except requests.exceptions.RequestException as e:
                self.stdout.write(self.style.ERROR(f"Could not download image: {e}"))
        else:
            self.stdout.write(f'CarModel "{largus_model}" already exists.')
        self.create_equipments(largus_model, [
            {
                'name': 'Classic',
                'equipment_type': 'standard',
                'price': 1250000,
                'power': 90,
                'features': {
                    'Комфорт': ['Электростеклоподъемники всех дверей', 'Кондиционер'],
                    'Безопасность': ['ABS', 'Подушка безопасности водителя'],
                    'Мультимедиа': ['Аудиосистема'],
                },
                'image_url': 'http://placehold.co/600x400/E0E0E0/000000?text=Largus+Classic'
            },
            {
                'name': 'Comfort',
                'equipment_type': 'comfort',
                'price': 1400000,
                'power': 106,
                'features': {
                    'Комфорт': ['Подогрев передних сидений', 'Электропривод и обогрев зеркал'],
                    'Безопасность': ['ABS', '2 подушки безопасности'],
                    'Мультимедиа': ['Мультимедийная система с экраном'],
                },
                'image_url': 'http://placehold.co/600x400/A0A0A0/FFFFFF?text=Largus+Comfort'
            },
            {
                'name': 'Enjoy',
                'equipment_type': 'luxury',
                'price': 1600000,
                'power': 106,
                'features': {
                    'Комфорт': ['Климат-контроль', 'Круиз-контроль', 'Датчики парковки'],
                    'Безопасность': ['ABS, ESP', '4 подушки безопасности'],
                    'Мультимедиа': ['Мультимедийная система с 7\" экраном'],
                    'Экстерьер': ['Литые диски 16\"'],
                },
                'image_url': 'http://placehold.co/600x400/FFCC00/000000?text=Largus+Enjoy'
            }
        ])

        self.stdout.write(self.style.SUCCESS('Database population complete!'))

    def create_equipments(self, car_model, equipments_data=None):
        if equipments_data is None:
            equipments_data = [
                {
                    'name': 'Comfort',
                    'equipment_type': 'comfort',
                    'price': 1700000,
                    'power': 106,
                    'features': {
                        'Комфорт': ['Кондиционер', 'Подогрев передних сидений', 'Электростеклоподъемники передние'],
                        'Безопасность': ['ABS', '2 подушки безопасности'],
                        'Мультимедиа': ['Аудиосистема с USB и Bluetooth'],
                    },
                    'image_url': 'http://placehold.co/600x400/E0E0E0/000000?text=Vesta+Comfort'
                },
                {
                    'name': 'Luxe',
                    'equipment_type': 'luxury',
                    'price': 1950000,
                    'power': 113,
                    'transmission': 'automatic',
                    'features': {
                        'Комфорт': ['Климат-контроль', 'Подогрев руля', 'Обогрев лобового стекла', 'Круиз-контроль'],
                        'Безопасность': ['ABS, ESP', '4 подушки безопасности', 'Парктроники задние'],
                        'Мультимедиа': ['Мультимедийная система с 7" экраном'],
                        'Экстерьер': ['Литые диски 16"'],
                    },
                    'image_url': 'http://placehold.co/600x400/A0A0A0/FFFFFF?text=Vesta+Luxe'
                },
                {
                    'name': 'Sportline',
                    'equipment_type': 'sport',
                    'price': 2200000,
                    'power': 125,
                    'acceleration': 9.8,
                    'features': {
                        'Комфорт': ['Климат-контроль', 'Камера заднего вида', 'Датчики дождя и света'],
                        'Безопасность': ['ABS, ESP', 'Боковые подушки безопасности', 'Система контроля слепых зон'],
                        'Мультимедиа': ['Яндекс.Авто с 9" экраном'],
                        'Экстерьер': ['Спортивный обвес', 'Литые диски 17"', 'Спойлер'],
                        'Интерьер': ['Спортивные сиденья с красной прострочкой'],
                    },
                    'image_url': 'http://placehold.co/600x400/FF0000/FFFFFF?text=Vesta+Sportline'
                }
            ]

        for data in equipments_data:
            equipment, created = Equipment.objects.get_or_create(
                car_model=car_model,
                name=data['name'],
                defaults={
                    'equipment_type': data['equipment_type'],
                    'price': data['price'],
                    'power': data.get('power'),
                    'transmission': data.get('transmission'),
                    'acceleration': data.get('acceleration'),
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'  - Created Equipment: {equipment.name}'))

                # Добавление опций
                for category_name, features_list in data['features'].items():
                    # Находим ключ категории по значению
                    category_key = next((key for key, value in EquipmentFeature.FEATURE_CATEGORY_CHOICES if value == category_name), 'other')
                    for feature_name in features_list:
                        EquipmentFeature.objects.create(equipment=equipment, category=category_key, name=feature_name)
                self.stdout.write(f'    - Added features for {equipment.name}')
                
                # Добавление изображения для комплектации
                try:
                    response = requests.get(data['image_url'], stream=True)
                    if response.status_code == 200:
                        ModelImage.objects.create(
                            car_model=car_model,
                            equipment=equipment,
                            image=ContentFile(response.content, name=f'{car_model.name}_{equipment.name}.png'),
                            title=f'{car_model.name} {equipment.name}'
                        )
                        self.stdout.write(self.style.SUCCESS(f'    - Added image for {equipment.name}'))
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"    - Could not download image for {equipment.name}: {e}"))
            else:
                self.stdout.write(f'  - Equipment "{equipment.name}" for {car_model.name} already exists.') 