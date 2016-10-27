from flask import Blueprint
from flask import flash
from flask import render_template
from flask import session

Catalog = Blueprint('catalog', __name__)

@Catalog.route('/')
@Catalog.route('/catalog')
def full_catalog():
    """Lists out categories and latest items."""
    return 'Catalog'


@Catalog.route('/catalog/add')
def create_item():
    """Add an item."""
    return 'Add an item'


@Catalog.route('/catalog/<category_name>')
def list_category(catalog_name):
    """Lists the items of a category."""
    return 'Catalog Items'


@Catalog.route('/catalog/<category_name>/<item_name>')
def show_item(catalog_name, item_name):
    """Show description of item."""
    return 'Item Description'


@Catalog.route('/catalog/<category_name>/<item_name>/edit')
def edit_item(catalog_name, item_name):
    """Edit an item."""
    return 'Update Items'


@Catalog.route('/catalog/<category_name>/<item_name>/delete')
def delete_item(catalog_name, item_name):
    """Delete an item."""
    return 'Delete Items'

