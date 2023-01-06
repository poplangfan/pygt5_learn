import psutil


# cpu信息
def get_cpu_info():
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_info = "CPU使用率：%i%%" % cpu_percent
    print(cpu_info)
    # return cpu_info


# 内存信息
def get_memory_info():
    virtual_memory = psutil.virtual_memory()
    used_memory = virtual_memory.used / 1024 / 1024 / 1024
    free_memory = virtual_memory.free / 1024 / 1024 / 1024
    memory_percent = virtual_memory.percent
    memory_info = "内存使用：%0.2fG，使用率%0.1f%%，剩余内存：%0.2fG" % (used_memory, memory_percent, free_memory)
    print(memory_info)
    # return memory_info


get_cpu_info()
get_memory_info()
