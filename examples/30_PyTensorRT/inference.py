#!/usr/bin/env python3
import time
from concurrent import futures
import py_yais as yais
import numpy as np

def random_data(*, count=1000, shape=(3,224,224)):
    for i in range(count):
        yield i

def main(data):
    manager = yais.InferenceManager(8)
    flowers = manager.register_tensorrt_engine("/work/models/ResNet-50-b8-int8.engine", "flowers")
    manager.allocate_resources()
    def infer(input):
        batch_id, data = input
        results = flowers.pyinfer(data).get()
        #results = flowers.compute().get()
        print("finished batch {}".format(batch_id))
    start = time.time()
    with futures.ThreadPoolExecutor(max_workers=20) as pool:
        results = pool.map(infer, enumerate(data))
    end = time.time()
    elapsed = end - start
    print(elapsed)

if __name__ == "__main__":
    print("Generating Random Data")
    data = [np.random.random_sample(size=(8,3,224,224)) for _ in range(1000)]
    print("Starting Inference Loop")
    main(data)
   
#    with futures.ThreadPoolExecutor(max_workers=100) as pool:
#        results = pool.map(flowers.infer, random_data(count=1000))
