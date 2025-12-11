def parse(input):

    devices = {}

    for line in open(input, 'r'):
        device, outputs = line.removesuffix('\n').split(': ')
        devices[device] = outputs.split(' ')

    return devices

class Devices:

    def __init__(self, devices):

        self.outputs = devices
        self.outputs['out'] = []

    def get_number_of_visit_paths(self, start='svr', end='out', visit=('dac', 'fft')):

        return
    
    def get_number_of_paths(self, start='you', end='out'):

        number_of_paths = 0
        queue = self.outputs[start]

        while len(queue) > 0:
            new_queue = []
            for device in queue:

                for output in self.outputs[device]:
                    if output == end:
                        number_of_paths += 1
                        continue

                    new_queue.append(output)

            queue = new_queue

        return number_of_paths

if __name__ == '__main__':

    devices = Devices(parse(input("Input File: ")))
    print(f"Number of paths from 'you' to 'out': {devices.get_number_of_paths()}")
    print(f"Number of paths from 'svr' to 'out' that visit 'dac' and 'fft': {devices.get_number_of_visit_paths()}")
