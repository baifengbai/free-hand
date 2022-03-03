from queue import Queue, LifoQueue, PriorityQueue
import time, threading

# 先进先出队列
q = Queue(maxsize=5)
# 后进先出队列
lq = LifoQueue(maxsize=6)
# 优先级队列
pq = PriorityQueue(maxsize=5)

for i in range(5):
    q.put(i)
    lq.put(i)
    pq.put(i)

print("先进先出队列：%s;是否为空：%s;多大, %s;是否满,%s"%(q.queue, q.empty(), q.qsize(), q.full()))
print("后进先出队列：%s;是否为空：%s;多大, %s;是否满,%s"%(lq.queue, lq.empty(), lq.qsize(), lq.full()))
print("优先级队列：%s;是否为空：%s;多大, %s;是否满,%s"%(pq.queue, pq.empty(), pq.qsize(), pq.full()))

print(q.get(), lq.get(), pq.get())

print("先进先出队列：%s;是否为空：%s;多大, %s;是否满,%s"%(q.queue, q.empty(), q.qsize(), q.full()))
print("后进先出队列：%s;是否为空：%s;多大, %s;是否满,%s"%(lq.queue, lq.empty(), lq.qsize(), lq.full()))
print("优先级队列：%s;是否为空：%s;多大, %s;是否满,%s"%(pq.queue, pq.empty(), pq.qsize(), pq.full()))

q = Queue(maxsize=0)
def product(name):
    count = 1
    while True:
        q.put('气球兵{}'.format(count))
        print('{}训练气球兵{}只'.format(name, count))
        count += 1
        time.sleep(5)
def consume(name):
    while True:
        print('{}使用了{}'.format(name, q.get()))
        time.sleep(1)
        q.task_done()
t1 = threading.Thread(target = product, args=('wpp',))
t2 = threading.Thread(target = consume, args=('ypp',))
t3 = threading.Thread(target = consume, args=('others',))
t1.start()
t2.start()
t3.start()
