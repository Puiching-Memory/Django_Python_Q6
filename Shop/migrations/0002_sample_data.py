from decimal import Decimal

from django.db import migrations


def CreateSampleData(apps, schema_editor):
    Category = apps.get_model("Shop", "Category")
    Product = apps.get_model("Shop", "Product")

    categories = [
        ("教材资料", "books", "课程教材、考研资料、四六级资料", 1),
        ("数码设备", "digital", "耳机、键盘、平板等校园常用设备", 2),
        ("生活用品", "daily", "宿舍收纳、小家电、日常用品", 3),
        ("运动户外", "sports", "球拍、瑜伽垫、骑行用品", 4),
    ]

    category_map = {}
    for name, slug, description, sort_order in categories:
        category, _ = Category.objects.get_or_create(
            Slug=slug,
            defaults={
                "Name": name,
                "Description": description,
                "SortOrder": sort_order,
            },
        )
        category_map[slug] = category

    products = [
        ("Python编程教材", "books", "李同学", "九成新", Decimal("36.00"), 5, "book_python.svg", "适合 Python 入门课程使用，书页干净，附带课后练习重点标注。"),
        ("计算机网络复习资料", "books", "王同学", "八成新", Decimal("18.00"), 8, "network_notes.svg", "包含课堂笔记、章节思维导图和期末复习题，适合网络专业复习。"),
        ("无线蓝牙耳机", "digital", "陈同学", "九成新", Decimal("89.00"), 2, "earbuds.svg", "续航稳定，适合自习室和通勤使用，附原装充电盒。"),
        ("机械键盘 87 键", "digital", "赵同学", "八成新", Decimal("128.00"), 1, "keyboard.svg", "青轴手感清脆，键帽完整，适合编程和日常办公。"),
        ("宿舍收纳箱", "daily", "刘同学", "九成新", Decimal("22.00"), 6, "storage_box.svg", "透明可叠放，适合衣物和书籍整理，宿舍自提。"),
        ("小型电煮锅", "daily", "周同学", "七成新", Decimal("45.00"), 3, "cooker.svg", "1.5L 容量，可煮面和热汤，功能正常。"),
        ("羽毛球拍", "sports", "孙同学", "八成新", Decimal("58.00"), 4, "badminton.svg", "轻量拍身，适合体育课和课后运动，附拍套。"),
        ("瑜伽垫", "sports", "黄同学", "九成新", Decimal("30.00"), 5, "yoga_mat.svg", "防滑材质，适合寝室拉伸和健身训练。"),
    ]

    for name, slug, seller, condition, price, stock, image_name, description in products:
        Product.objects.get_or_create(
            Name=name,
            defaults={
                "Category": category_map[slug],
                "SellerName": seller,
                "Condition": condition,
                "Price": price,
                "Stock": stock,
                "ImageName": image_name,
                "Description": description,
            },
        )


def DeleteSampleData(apps, schema_editor):
    Product = apps.get_model("Shop", "Product")
    Category = apps.get_model("Shop", "Category")
    Product.objects.filter(
        Name__in=[
            "Python编程教材",
            "计算机网络复习资料",
            "无线蓝牙耳机",
            "机械键盘 87 键",
            "宿舍收纳箱",
            "小型电煮锅",
            "羽毛球拍",
            "瑜伽垫",
        ]
    ).delete()
    Category.objects.filter(Slug__in=["books", "digital", "daily", "sports"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("Shop", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(CreateSampleData, DeleteSampleData),
    ]
