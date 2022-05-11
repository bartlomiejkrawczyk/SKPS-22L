from matplotlib import pyplot as plt
from pathlib import Path


def main():
    servers = []
    for directory in Path('./histograms').iterdir():
        print(directory.name)

        if directory.is_file():
            continue

        task = int(directory.name[0])
        if task in [4, 5]:
            clients = []
            number_of_clients = int(directory.name[2])

            for num in range(number_of_clients):
                with directory.joinpath(f'cli_{num}.txt').open(mode='r') as file:
                    clients.append(
                        [int(line.split(' ')[3])
                         for line in file if line]
                    )

            print(clients)
            plt.hist(clients, label=[
                f'Client {num}' for num in range(number_of_clients)],
                bins=20)
            plt.legend()
            plt.xlabel('Delivery Time [us]')
            plt.ylabel('Number of Occurrences')
            plt.savefig(directory / 'histogram.png')
            plt.clf()
        else:
            with directory.joinpath(f'server.txt').open(mode='r') as file:
                servers.append(
                    [int(line.split(' ')[2])
                     for line in file if line][1:]
                )

    plt.hist(servers, label=['Original', 'Modified'], bins=50)
    plt.xlabel('Delivery Time [us]')
    plt.ylabel('Number of Occurrences')
    plt.legend()
    plt.savefig('./histograms/histogram_6.png')


if __name__ == '__main__':
    main()
