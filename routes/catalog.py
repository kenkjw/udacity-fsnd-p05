from flask import Blueprint

catalog = Blueprint('catalog', __name__)

@catalog.route('/')
@catalog.route('/catalog')
def full_catalog():
    """Lists out categories and latest items."""
    return 'Catalog'


@catalog.route('/catalog/add')
def create_item():
    """Add an item."""
    return 'Add an item'


@catalog.route('/catalog/<category_name>')
def list_category(catalog_name):
    """Lists the items of a category."""
    return 'Catalog Items'


@catalog.route('/catalog/<category_name>/<item_name>')
def show_item(catalog_name, item_name):
    """Show description of item."""
    return 'Item Description'


@catalog.route('/catalog/<category_name>/<item_name>/edit')
def edit_item(catalog_name, item_name):
    """Edit an item."""
    return 'Update Items'


@catalog.route('/catalog/<category_name>/<item_name>/delete')
def delete_item(catalog_name, item_name):
    """Delete an item."""
    return 'Delete Items'

