from django.shortcuts import render, get_object_or_404
from .models import Car, CarModel, Equipment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max
import json

def services(request):
    cars_list = Car.objects.all()
    years = Car.objects.values_list('year', flat=True).distinct().order_by('-year')
    
    # Apply filters
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    
    if year_from:
        cars_list = cars_list.filter(year__gte=year_from)
    if year_to:
        cars_list = cars_list.filter(year__lte=year_to)
    
    equipment = request.GET.get('equipment')
    if equipment:
        cars_list = cars_list.filter(equipment_display=equipment)
    
    body_types = request.GET.getlist('body_type')
    if body_types:
        cars_list = cars_list.filter(body_type__in=body_types)
    
    colors = request.GET.getlist('color')
    if colors:
        color_mapping = {
            'white': 'Белый',
            'black': 'Черный',
            'silver': 'Серебристый',
            'gray': 'Серый',
            'red': 'Красный',
            'blue': 'Синий',
            'green': 'Зеленый',
            'brown': 'Коричневый'
        }
        db_colors = [color_mapping.get(color, color) for color in colors if color in color_mapping]
        cars_list = cars_list.filter(color__in=db_colors)
    
    fuel_types = request.GET.getlist('fuel_type')
    if fuel_types:
        cars_list = cars_list.filter(fuel_type__in=fuel_types)
    
    transmissions = request.GET.getlist('transmission')
    if transmissions:
        cars_list = cars_list.filter(transmission__in=transmissions)
    
    price_from = request.GET.get('price_from')
    price_to = request.GET.get('price_to')
    
    if price_from:
        cars_list = cars_list.filter(price__gte=price_from)
    if price_to:
        cars_list = cars_list.filter(price__lte=price_to)
    
    is_available = request.GET.get('is_available')
    if is_available == 'true':
        cars_list = cars_list.filter(is_available=True)
    
    is_new = request.GET.get('is_new')
    if is_new == 'true':
        cars_list = cars_list.filter(is_new=True)
    
    # Pagination
    paginator = Paginator(cars_list, 9)
    page = request.GET.get('page')
    
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)
    
    price_range = Car.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    context = {
        'cars': cars,
        'years': years,
        'price_range': price_range,
        'body_types': Car.BODY_TYPE_CHOICES,
        'equipment_types': Car.EQUIPMENT_CHOICES,
        'fuel_types': Car.FUEL_CHOICES,
        'transmission_types': Car.TRANSMISSION_CHOICES,
    }
    
    return render(request, 'services.html', context)


def car_detail(request, slug):
    car_model = get_object_or_404(CarModel, slug=slug)
    equipments = Equipment.objects.filter(car_model=car_model).prefetch_related('features', 'images')
    similar_models = CarModel.objects.filter(brand=car_model.brand).exclude(id=car_model.id)[:3]
    available_cars = Car.objects.filter(model=car_model, is_available=True)

    equipments_data = {}
    
    # Получаем общие изображения модели, если они есть
    model_images = [img.image.url for img in car_model.images.filter(equipment__isnull=True)]
    if car_model.image:
        model_images.insert(0, car_model.image.url)

    for eq in equipments:
        eq_images = [img.image.url for img in eq.images.all()]
        
        features_by_category = {}
        for feature in eq.features.all():
            category_display = feature.get_category_display()
            if category_display not in features_by_category:
                features_by_category[category_display] = []
            features_by_category[category_display].append(feature.name)

        equipments_data[eq.id] = {
            'id': eq.id,
            'name': eq.name,
            'price': f"{eq.price:,.0f}".replace(",", " "),
            'description': eq.description or '',
            'engine_volume': f"{eq.engine_volume or car_model.engine_volume}",
            'power': eq.power or car_model.power,
            'transmission': eq.get_transmission_display() if eq.transmission else car_model.get_transmission_display(),
            'acceleration': f"{eq.acceleration or car_model.acceleration}",
            'images': eq_images if eq_images else model_images,
            'features': features_by_category,
            'fuel_type': car_model.get_fuel_type_display(),
            'max_speed': car_model.max_speed,
            'fuel_consumption_city': f"{car_model.fuel_consumption_city}" if hasattr(car_model, 'fuel_consumption_city') and car_model.fuel_consumption_city is not None else 'N/A',
            'fuel_consumption_highway': f"{car_model.fuel_consumption_highway}" if hasattr(car_model, 'fuel_consumption_highway') and car_model.fuel_consumption_highway is not None else 'N/A',
            'fuel_consumption': f"{car_model.fuel_consumption}" if car_model.fuel_consumption is not None else 'N/A',
        }
    
    initial_images = []
    first_equipment = equipments.first()
    if first_equipment:
        # Получаем изображения из первой комплектации
        initial_images = [img.image.url for img in first_equipment.images.all()]
    
    if not initial_images:
        # Если у первой комплектации нет изображений, используем общие изображения модели
        initial_images = model_images
        
    return render(request, 'car_detail.html', {
        'car_model': car_model,
        'equipments': equipments,
        'similar_models': similar_models,
        'available_cars': available_cars,
        'equipments_data_json': json.dumps(equipments_data),
        'initial_images': initial_images,
    })