import socket
import csv


class DataExchangeServer:
    def __init__(self):
        sock_ip = 'localhost'
        sock_port = 800
        self._sock = socket.socket()
        self._sock.connect((sock_ip, sock_port))

    def send_data(self, mmt_data):
        """Receive fake Momentum data (1 or 2) and read data from file to send out for analysis

        :param mmt_data: 1 or 2
        :return: 1 or 0 to represent if is outlier
        """
        is_outlier = False

        data_msg = self._get_fake_data(mmt_data)

        # send the data to the command centre
        self._sock.sendall(bytes(data_msg, 'utf-8'))

        # wait for the command centre to analyse the data
        # cmd_response = self._sock.recv(1024).decode('utf-8')
        #
        # is_outlier = int(cmd_response)

        return is_outlier

    def _get_fake_data(self, data_set):
        """Construct a fake data string msg according to the data set number

        :param data_set: data set number
        :return: whole data set in string
        """
        data_set1_path = 'HPLC_data/Result_Export2909.csv'
        data_set2_path = 'HPLC_data/Result_Export2889.csv'

        if data_set == 1:
            data_path = data_set1_path
        elif data_set == 2:
            data_path = data_set2_path

        ts = []
        data = []
        with open(data_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')

            next(csv_reader, None)
            next(csv_reader, None)

            for row in csv_reader:
                ts.append(row[0])
                data.append(row[1])

        data_msg = "$\n"
        for i in range(len(ts)):
            data_msg += str(ts[i]) + ' ' + str(data[i]) + '\n'

        data_msg += "#"

        return data_msg


if __name__ == '__main__':
    exchange_server = DataExchangeServer()

    exchange_server.send_data(mmt_data=2)
