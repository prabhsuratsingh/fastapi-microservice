from main import Order, redis
import time

key = 'refund_order'
group = 'payment-group'

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
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(str(e))
    
    time.sleep(1) 