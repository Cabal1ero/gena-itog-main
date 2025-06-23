from django.core.management.base import BaseCommand
from apps.car.models import CarBrand, CarModel, Equipment, EquipmentFeature, ModelImage, Car
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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Lada_Granta_2018_IMG_20210410_124849.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2b/Lada_Granta_2018_IMG_20210410_124900.jpg',
                ]
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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Lada_Granta_2018_IMG_20210410_124849.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2b/Lada_Granta_2018_IMG_20210410_124900.jpg',
                ]
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
                    'Мультимедиа': ['Мультимедийная система с 7" экраном'],
                    'Экстерьер': ['Литые диски 15"'],
                },
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/7/7e/Lada_Granta_2018_IMG_20210410_124849.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2b/Lada_Granta_2018_IMG_20210410_124900.jpg',
                ]
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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_002.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_003.jpg',
                ]
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
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_002.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_003.jpg',
                ]
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
                    'Мультимедиа': ['Мультимедийная система с 7" экраном'],
                    'Экстерьер': ['Литые диски 15"'],
                },
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_002.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2d/Lada_Kalina_II_2012_IMG_003.jpg',
                ]
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
                'price': 1200000,
                'power': 90,
                'features': {
                    'Комфорт': ['Электростеклоподъемники всех дверей'],
                    'Безопасность': ['ABS', 'Подушка безопасности водителя'],
                    'Мультимедиа': ['Аудиоподготовка'],
                },
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153015.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153016.jpg',
                ]
            },
            {
                'name': 'Comfort',
                'equipment_type': 'comfort',
                'price': 1350000,
                'power': 106,
                'features': {
                    'Комфорт': ['Кондиционер', 'Подогрев передних сидений'],
                    'Безопасность': ['ABS', '2 подушки безопасности'],
                    'Мультимедиа': ['Аудиосистема с USB'],
                },
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153015.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153016.jpg',
                ]
            },
            {
                'name': 'Enjoy',
                'equipment_type': 'luxury',
                'price': 1500000,
                'power': 106,
                'transmission': 'automatic',
                'features': {
                    'Комфорт': ['Климат-контроль', 'Круиз-контроль', 'Датчики парковки'],
                    'Безопасность': ['ABS, ESP', '4 подушки безопасности'],
                    'Мультимедиа': ['Мультимедийная система с 7" экраном'],
                    'Экстерьер': ['Литые диски 16"'],
                },
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153015.jpg',
                'extra_images': [
                    'https://upload.wikimedia.org/wikipedia/commons/2/2a/Lada_Largus_Cross_IMG_20210612_153016.jpg',
                ]
            }
        ])

        # --- СОЗДАНИЕ НЕСКОЛЬКИХ АВТОМОБИЛЕЙ ---
        # Примерные данные для автомобилей
        cars_to_create = [
            # Vesta
            {
                'model': car_model,
                'equipment': car_model.equipments.filter(name='Comfort').first(),
                'year': 2023,
                'color': 'Белый',
                'price': 1700000,
                'mileage': 0,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'body_type': 'sedan',
                'equipment_display': 'comfort',
                'engine_volume': 1.6,
                'power': 106,
                'description': 'LADA Vesta Comfort, новый автомобиль.',
                'is_available': True,
                'is_new': True,
            },
            # Granta
            {
                'model': granta_model,
                'equipment': granta_model.equipments.filter(name='Life').first(),
                'year': 2022,
                'color': 'Серый',
                'price': 1250000,
                'mileage': 5000,
                'transmission': 'automatic',
                'fuel_type': 'petrol',
                'body_type': 'sedan',
                'equipment_display': 'luxury',
                'engine_volume': 1.6,
                'power': 106,
                'description': 'LADA Granta Life, с небольшим пробегом.',
                'is_available': True,
                'is_new': False,
            },
            # Kalina
            {
                'model': kalina_model,
                'equipment': kalina_model.equipments.filter(name='Luxe').first(),
                'year': 2021,
                'color': 'Красный',
                'price': 1100000,
                'mileage': 15000,
                'transmission': 'automatic',
                'fuel_type': 'petrol',
                'body_type': 'wagon',
                'equipment_display': 'luxury',
                'engine_volume': 1.6,
                'power': 106,
                'description': 'LADA Kalina Luxe, ухоженный автомобиль.',
                'is_available': True,
                'is_new': False,
            },
            # Largus
            {
                'model': largus_model,
                'equipment': largus_model.equipments.filter(name='Enjoy').first() or largus_model.equipments.first(),
                'year': 2023,
                'color': 'Синий',
                'price': 1400000,
                'mileage': 0,
                'transmission': 'manual',
                'fuel_type': 'petrol',
                'body_type': 'wagon',
                'equipment_display': 'comfort',
                'engine_volume': 1.6,
                'power': 106,
                'description': 'LADA Largus Comfort, новый автомобиль.',
                'is_available': True,
                'is_new': True,
            },
        ]
        for car_data in cars_to_create:
            # Получаем equipment_display из комплектации, если она есть
            equipment = car_data['equipment']
            equipment_display = equipment.equipment_type if equipment else car_data.get('equipment_display', 'standard')
            car, created = Car.objects.get_or_create(
                model=car_data['model'],
                equipment=equipment,
                year=car_data['year'],
                color=car_data['color'],
                defaults={
                    'price': car_data['price'],
                    'mileage': car_data['mileage'],
                    'transmission': car_data['transmission'],
                    'fuel_type': car_data['fuel_type'],
                    'body_type': car_data['body_type'],
                    'equipment_display': equipment_display,
                    'engine_volume': car_data['engine_volume'],
                    'power': car_data['power'],
                    'description': car_data['description'],
                    'is_available': car_data['is_available'],
                    'is_new': car_data['is_new'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created Car: {car}'))
            else:
                self.stdout.write(f'Car "{car}" already exists.')

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
                    'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Lada_Vesta_2015_IMG_1087.jpg',
                    'extra_images': [
                        'https://upload.wikimedia.org/wikipedia/commons/7/7d/Lada_Vesta_2015_IMG_1090.jpg',
                    ]
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
                    'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Lada_Vesta_2015_IMG_1087.jpg',
                    'extra_images': [
                        'https://upload.wikimedia.org/wikipedia/commons/7/7d/Lada_Vesta_2015_IMG_1090.jpg',
                    ]
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
                    'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Lada_Vesta_2015_IMG_1087.jpg',
                    'extra_images': [
                        'https://upload.wikimedia.org/wikipedia/commons/7/7d/Lada_Vesta_2015_IMG_1090.jpg',
                    ]
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
                    category_key = next((key for key, value in EquipmentFeature.FEATURE_CATEGORY_CHOICES if value == category_name), 'other')
                    for feature_name in features_list:
                        EquipmentFeature.objects.create(equipment=equipment, category=category_key, name=feature_name)
                self.stdout.write(f'    - Added features for {equipment.name}')
            else:
                self.stdout.write(f'  - Equipment "{equipment.name}" for {car_model.name} already exists.') 