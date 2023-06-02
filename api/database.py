from mongoengine import connect

db_name = "uitcommerce"

connect(
    db=db_name,
    host='mongodb+srv://uitcommerce:uitcommerce@uitcommerce.oyuchwj.mongodb.net/'
)
