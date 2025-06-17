# client.py

import socket
import pickle
import sys
from aco_core import Ant, clone_edges

HOST = 'localhost'
PORT = 9000
ALPHA = 1.0
BETA = 3.0


def run_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"[CLIENTE] Conectado ao servidor {HOST}:{PORT}")

        while True:
            try:
                data = b""
                while True:
                    packet = s.recv(4096)
                    if not packet:
                        return
                    data += packet
                    try:
                        edges, iteration = pickle.loads(data)
                        break
                    except:
                        continue

                print(f"[CLIENTE] Iteração {iteration}: executando formiga...")
                edges_copy = clone_edges(edges)
                num_nodes = len(edges_copy)

                ant = Ant(ALPHA, BETA, num_nodes, edges_copy)
                tour, distance = ant.find_tour()

                print(f"[CLIENTE] Iteração {iteration}: Tour concluído com distância = {distance:.2f}")
                result = pickle.dumps((tour, distance))
                s.sendall(result)

            except Exception as e:
                print(f"[CLIENTE] Erro: {e}")
                break

if __name__ == '__main__':
    run_client()
