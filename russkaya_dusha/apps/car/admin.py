from django.contrib import admin
from .models import CarBrand, CarModel, Equipment, ModelImage, EquipmentFeature, Car
from django.utils.html import format_html

class EquipmentFeatureInline(admin.TabularInline):
    model = EquipmentFeature
    extra = 1

class EquipmentInline(admin.StackedInline):
    model = Equipment
    extra = 1
    show_change_link = True

class ModelImageInline(admin.TabularInline):
    model = ModelImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Предпросмотр'

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'base_price', 'is_popular', 'is_new')
    list_filter = ('brand', 'is_popular', 'is_new', 'body_type')
    search_fields = ('name', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [EquipmentInline, ModelImageInline]

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_model', 'price', 'equipment_type')
    list_filter = ('car_model', 'equipment_type')
    search_fields = ('name', 'car_model__name')
    inlines = [EquipmentFeatureInline, ModelImageInline]

@admin.register(ModelImage)
class ModelImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'car_model', 'equipment', 'is_main', 'image_preview')
    list_filter = ('car_model', 'equipment', 'is_main')
    search_fields = ('title', 'car_model__name')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Предпросмотр'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'model', 'year', 'color', 'price', 'is_available')
    list_filter = ('model', 'year', 'is_available', 'transmission', 'fuel_type')
    search_fields = ('model__name', 'vin')
