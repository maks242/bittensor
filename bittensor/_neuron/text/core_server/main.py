import bittensor
import torch.multiprocessing as mp
import torch

def processfn(queue):
    tl = torch.randn(1024*1024*1, device='cuda:0')
    bittensor.neurons.core_server.neuron(queue=queue).run()

if __name__ == "__main__":
    mp.set_start_method("spawn")

    bittensor.utils.version_checking()
    
    server_model = bittensor.neurons.core_server.server()
    server_model = server_model.to(server_model.device)


    ctx = mp.get_context("spawn")
    queue = ctx.Queue()

    instances_count = 1
    instances = []
    for i in range(instances_count):
        queue.put(server_model)

        instance = mp.Process(target=processfn, args=(queue,))
        instances.append(instance)
        instance.start()

    for instance in instances:
        instance.join()
