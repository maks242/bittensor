import bittensor
import torch.multiprocessing as mp


def processfn(queue, config):
    bittensor.neurons.core_server.neuron(queue=queue, config=config).run()

if __name__ == "__main__":
    bittensor.utils.version_checking()
    
    server_model = bittensor.neurons.core_server.server()
    server_model = server_model.to(server_model.device)
    server_model.share_memory()

    ctx = mp.get_context("spawn")
    queue = ctx.Queue()

    instances_count = 4
    instances = []
    for i in range(instances_count):
        queue.put(server_model)

        config = server_model.config
        config.update_with_kwargs({'wallet','hw' + i})

        instance = mp.Process(target=processfn, args=(queue, config))
        instances.append(instance)
        instance.start()

    for instance in instances:
        instance.join()
