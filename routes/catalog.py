from flask import Blueprint
from flask import flash
from flask import render_template
from flask import session
from flask import url_for

from models import Item
from models import User
Catalog = Blueprint('catalog', __name__)

@Catalog.route('/')
@Catalog.route('/catalog')
def full_catalog():
    """Lists out categories and latest items."""
    categories = Item.get_categories()
    latest = Item.get_latest(10)
    return render_template('catalog-full.html', categories=categories, latest=latest)


@Catalog.route('/catalog/add')
def create_item():
    """Add an item."""

    return render_template('catalog-add.html')


@Catalog.route('/catalog/<category_name>')
def list_category(category_name):
    """Lists the items of a category."""
    categories = Item.get_categories()
    category_items = Item.by_category(category_name)
    return render_template(
        'catalog-category.html', 
        categories=categories, 
        category_items=category_items)


@Catalog.route('/catalog/<category_name>/<item_name>')
def show_item(category_name, item_name):
    """Show description of item."""
    item = Item.by_name(category_name, item_name)
    return render_template('catalog-item.html', items=item)


@Catalog.route('/catalog/<category_name>/<item_name>/edit')
def edit_item(category_name, item_name):
    """Edit an item."""
    item = Item.by_name(category_name, item_name)
    return render_template('catalog-item-edit.html', item=item)


@Catalog.route('/catalog/<category_name>/<item_name>/delete')
def delete_item(category_name, item_name):
    """Delete an item."""
    item = Item.by_name(category_name, item_name)
    return render_template('catalog-item-delete.html', item=item)

