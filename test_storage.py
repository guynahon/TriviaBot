from storage import Storage


def test_add_coffee():
    db = Storage("shopping_cart_test", clear=True)
    doc = db.add_item(12345, "coffee")
    assert doc['items'] == ['coffee']