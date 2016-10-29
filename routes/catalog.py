from flask import Blueprint
from flask import flash
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from models import Item
from models import User
from utils import token
from utils import signed_in

Catalog = Blueprint('catalog', __name__)


@Catalog.route('/')
@Catalog.route('/catalog')
@Catalog.route('/catalog.<type>')
def full_catalog(type='html'):
    """Lists out categories and latest items.

    Accepts GET method.
    Does not require authentication.
    If the optional type parameter is set and is equal to JSON,
    return a JSON response with all catalog items
    """
    categories = Item.get_categories()
    latest = Item.get_latest(10)
    if type.lower() == 'json':
        catalog = dict()
        for category in categories:
            category_items = Item.by_category(category)
            catalog[category] = [i.serialize for i in category_items]
        return jsonify(catalog=catalog)
    return render_template(
        'catalog-full.html',
        categories=categories,
        latest=latest)


@Catalog.route('/catalog/add', methods=['GET', 'POST'])
def create_item():
    """Add an item.

    Accepts GET and POST methods.
    Redirect if user is not signed in.

    """
    if not signed_in():
        flash('You must be logged in to add an item.')
        return redirect(url_for('catalog.full_catalog'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        csrftoken = request.form.get('csrftoken')
        if csrftoken != session['csrf']:
            flash('Invalid CSRF token.')
        elif not name or not description or not category:
            flash('All fields must be filled.')
        else:
            # Everything valid. Create item.
            del session['csrf']
            item = Item.create_item(name, description,
                                    category, session['user_id'])
            if item:
                flash('Item successfully updated.')
                return redirect(url_for(
                    'catalog.show_item',
                    category_name=item.category,
                    item_name=item.name))
    categories = Item.get_categories()
    session['csrf'] = token()
    return render_template('catalog-add.html', categories=categories)


@Catalog.route('/catalog/<category_name>')
@Catalog.route('/catalog/<category_name>.<type>')
def list_category(category_name, type='html'):
    """Lists the items of a category.

    Accepts GET method.
    Does not require authentication.
    If the optional type parameter is set and is equal to JSON,
    return a JSON response with all items with category=category_name.

    Parameters:
        category_name: category name of items to search for
    """
    categories = Item.get_categories()
    category_items = Item.by_category(category_name)

    if type.lower() == 'json':
        return jsonify(category_items=[i.serialize for i in category_items])
    return render_template(
        'catalog-category.html',
        categories=categories,
        category_items=category_items)


@Catalog.route('/catalog/<category_name>/<item_name>')
@Catalog.route('/catalog/<category_name>/<item_name>.<type>')
def show_item(category_name, item_name, type='html'):
    """Show description of item.

    Accepts GET method.
    Does not require authentication.
    If the optional type parameter is set and is equal to JSON,
    return a JSON response with item=item_name with category=category_name.

    Parameters:
        category_name: category name of item
        item_name: name of the item
    """

    item = Item.by_name(category_name, item_name)
    if not item:
        flash('Could not find item: {}.'.format(item_name))
        return redirect('/')

    categories = Item.get_categories()
    category_items = Item.by_category(category_name)
    if type.lower() == 'json':
        return jsonify(item=item.serialize)
    return render_template('catalog-item.html',
                           item=item,
                           categories=categories,
                           category_items=category_items)


@Catalog.route(
    '/catalog/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
def edit_item(category_name, item_name):
    """Edit an item.

    Accepts GET and POST methods.
    Redirect to show_item page if user is not authenticated/authorized.

    Parameters:
        category_name: category name of item to edit
        item_name: name of the item to edit
    """
    item = Item.by_name(category_name, item_name)
    if not item:
        flash('Could not find item: {}.'.format(item_name))
        return redirect('/')

    if not signed_in():
        flash('You must be logged in to edit an item.')
        return redirect(url_for(
            'catalog.show_item',
            category_name=item.category,
            tem_name=item.name))

    if not item.is_owned_by(session['user_id']):
        flash('You do not have permission to edit this item.')
        return redirect(url_for(
            'catalog.show_item',
            category_name=item.category,
            item_name=item.name))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        csrftoken = request.form.get('csrftoken')
        if csrftoken != session['csrf']:
            flash('Invalid CSRF token.')
        elif not name or not description or not category:
            flash('All fields must be filled.')
        else:
            del session['csrf']
            item.name = name
            item.description = description
            item.category = category
            flash('Item successfully updated.')
            return redirect(url_for(
                'catalog.show_item',
                category_name=item.category,
                item_name=item.name))

    categories = Item.get_categories()
    category_items = Item.by_category(category_name)
    session['csrf'] = token()
    return render_template(
        'catalog-item-edit.html',
        item=item,
        categories=categories,
        category_items=category_items)


@Catalog.route(
    '/catalog/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
def delete_item(category_name, item_name):
    """Delete an item.

    Accepts GET and POST methods.
    Redirect to show_item page if user is not authenticated/authorized.

    Parameters:
        category_name: category name of item to delete
        item_name: name of the item to delete
    """
    item = Item.by_name(category_name, item_name)
    if not item:
        flash('Could not find item: {}.'.format(item_name))
        return redirect('/')

    if not signed_in():
        flash('You must be logged in to delete an item.')
        return redirect(url_for(
            'catalog.show_item',
            category_name=item.category,
            item_name=item.name))

    if not item.is_owned_by(session['user_id']):
        flash('You do not have permission to delete this item.')
        return redirect(url_for(
            'catalog.show_item',
            category_name=item.category,
            item_name=item.name))

    if request.method == 'POST':
        csrftoken = request.form.get('csrftoken')
        if csrftoken != session['csrf']:
            flash('Invalid CSRF token.')
        else:
            del session['csrf']
            item.delete()
            flash('Item successfully deleted.')
            return redirect('/')

    categories = Item.get_categories()
    category_items = Item.by_category(category_name)
    session['csrf'] = token()
    return render_template(
        'catalog-item-delete.html',
        item=item,
        categories=categories,
        category_items=category_items)
