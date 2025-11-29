from main import Product, redis
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group, id='0', mkstream=True)
except:
    print("Group already exists")

while True:
    try:
        results = redis.xreadgroup(
            groupname=group,
            consumername=key,
            streams={key: '>'},
            count=None
        )
        if results != []:
            for result in results:
                obj = result[1][0][1]
                product = Product.get(obj['product_id'])
                print(f"Product: {product}")
                product.quantity = product.quantity - int(obj['quantity'])
                product.save()

    except Exception as e:
        print(str(e))
    
    time.sleep(1) 