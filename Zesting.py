import time

start = time.perf_counter()

time.sleep(3)

end = time.perf_counter()

print(f"Response time adalah {end - start}")