import random
from django.core.management.base import BaseCommand
from shop.models import Category, Brand, Product

class Command(BaseCommand):
    help = 'Seeds the database with premium eyewear data in Russian'

    def handle(self, *args, **options):
        self.stdout.write('Очистка существующих данных...')
        Product.objects.all().delete()
        Brand.objects.all().delete()
        Category.objects.all().delete()
        
        self.stdout.write('Создание категорий...')
        categories_data = [
            {'name': 'СОЛНЦЕЗАЩИТНЫЕ ОЧКИ', 'slug': 'sunglasses', 'order': 1},
            {'name': 'ОПРАВЫ', 'slug': 'optical', 'order': 2},
            {'name': 'АКСЕССУАРЫ', 'slug': 'accessories', 'order': 3},
        ]
        
        categories = {}
        for data in categories_data:
            cat = Category.objects.create(**data)
            categories[data['slug']] = cat

        self.stdout.write('Создание премиальных брендов...')
        brands_data = [
            {'name': 'Jacques Marie Mage', 'slug': 'jacques-marie-mage'},
            {'name': 'DITA', 'slug': 'dita'},
            {'name': 'MYKITA', 'slug': 'mykita'},
            {'name': 'Oliver Peoples', 'slug': 'oliver-peoples'},
            {'name': 'Tom Ford', 'slug': 'tom-ford'},
            {'name': 'Matsuda', 'slug': 'matsuda'},
        ]
        
        brands = {}
        for data in brands_data:
            brand = Brand.objects.create(**data)
            brands[data['slug']] = brand

        self.stdout.write('Создание товаров...')
        
        products_data = [
            # Jacques Marie Mage
            {
                'name': 'DEALAN NOIR 9',
                'slug': 'dealan-noir-9',
                'category': categories['sunglasses'],
                'brand': brands['jacques-marie-mage'],
                'price': 89000,
                'is_hit': True,
                'description': 'Ручная работа из Японии. Оммаж смелым очкам, которые носил Боб Дилан в середине 60-х. Оправа из 10-мм выдержанного ацетата целлюлозы с кастомными дужками.',
                'specifications': {
                    'Материал': '10-мм черный полированный ацетат',
                    'Фурнитура': 'Стерлинговое серебро',
                    'Линзы': 'Jet Black CR39',
                    'Происхождение': 'Ручная работа, Япония',
                },
            },
            {
                'name': 'ZEPHIRIN 47',
                'slug': 'zephirin-47',
                'category': categories['optical'],
                'brand': brands['jacques-marie-mage'],
                'price': 95000,
                'is_new': True,
                'description': 'Отличается калибровкой времен до Второй мировой войны и безупречной отделкой. Обновленная версия оригинальной модели Zephirin с чуть более широкой посадкой.',
                'specifications': {
                    'Материал': 'Ацетат цвета "Гавана"',
                    'Фурнитура': 'Золото 18к',
                    'Форма': 'Квадратная',
                    'Происхождение': 'Ручная работа, Япония',
                },
            },
            
            # DITA
            {
                'name': 'GRANDMASTER-FIVE',
                'slug': 'grandmaster-five',
                'category': categories['sunglasses'],
                'brand': brands['dita'],
                'price': 105000,
                'description': 'Дань максимализму хип-хоп сцены конца 70-х. Титановая оправа с искусной ромбовидной гравировкой.',
                'specifications': {
                    'Оправа': 'Титан и ацетат',
                    'Линзы': 'Защита UVA/UVB',
                    'Отделка': 'Позолота 18к',
                    'Происхождение': 'Сделано в Японии',
                },
            },
            {
                'name': 'MACH-SIX',
                'slug': 'mach-six',
                'category': categories['sunglasses'],
                'brand': brands['dita'],
                'price': 115000,
                'is_hit': True,
                'description': 'Лишена орнаментов в пользу изысканного минималистичного шасси. Вдохновлена автомобильным дизайном и современной скоростью.',
                'specifications': {
                    'Оправа': 'Титан',
                    'Линзы': 'Градиентный серый',
                    'Стиль': 'Авиатор',
                    'Происхождение': 'Сделано в Японии',
                },
            },

            # MYKITA
            {
                'name': 'LEICA ML07',
                'slug': 'leica-ml07',
                'category': categories['sunglasses'],
                'brand': brands['mykita'],
                'price': 78000,
                'description': 'Коллаборация с Leica Camera. Минималистичная конструкция из нержавеющей стали с фирменными деталями Leica и премиальной оптикой.',
                'specifications': {
                    'Материал': 'Нержавеющая сталь',
                    'Линзы': 'Leica Eyecare',
                    'Технология': 'Спиральный шарнир',
                    'Происхождение': 'Ручная работа, Берлин',
                },
            },
            
            # Tom Ford
            {
                'name': 'Snowdon Sunglasses',
                'slug': 'snowdon-sunglasses',
                'category': categories['sunglasses'],
                'brand': brands['tom-ford'],
                'price': 42000,
                'old_price': 55000,
                'description': 'Как в фильме "Спектр". Массивная оправа из ацетата в винтажном стиле с фирменным логотипом T на дужках.',
                'specifications': {
                    'Материал': 'Ацетат',
                    'Линзы': 'Поляризационные',
                    'Стиль': 'Вайфарер',
                    'Происхождение': 'Сделано в Италии',
                },
            },
            {
                'name': 'Blue Block Round',
                'slug': 'blue-block-round',
                'category': categories['optical'],
                'brand': brands['tom-ford'],
                'price': 38000,
                'description': 'Изысканная круглая оправа с линзами Blue Block для снижения нагрузки на глаза при работе с цифровыми устройствами.',
                'specifications': {
                    'Материал': 'Ацетат',
                    'Технология': 'Линзы Blue Block',
                    'Форма': 'Круглая',
                    'Происхождение': 'Сделано в Италии',
                },
            },
            
            # Matsuda
            {
                'name': 'M3023 Aviator',
                'slug': 'm3023-aviator',
                'category': categories['sunglasses'],
                'brand': brands['matsuda'],
                'price': 65000,
                'is_hit': True,
                'description': 'Обновленная форма авиаторов из титана и ацетата. Фирменная гравировка M на ободке.',
                'specifications': {
                    'Материал': 'Античный золотой титан',
                    'Линзы': 'Стекло G-15',
                    'Детали': 'Ручная гравировка',
                    'Происхождение': 'Ручная работа, Япония',
                },
            },
        ]

        for data in products_data:
            Product.objects.create(**data)
            self.stdout.write(f'  Создано: {data["name"]}')

        self.stdout.write(self.style.SUCCESS(f'\nГотово! База данных заполнена: {Product.objects.count()} премиальных товаров.'))
