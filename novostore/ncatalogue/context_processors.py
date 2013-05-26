from models import Category

def categories_context(context):
    categories = Category.objects.filter(is_operating = True, shop=context.shop)
    return { 'categories' : categories }