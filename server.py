import socket
import threading
import pickle
import random
from aco_core import build_graph, deposit_pheromone

HOST = 'localhost'
PORT = 9000
NUM_CLIENTS = 1
NUM_ITERATIONS = 10

random.seed(42)  # Semente fixa para gerar sempre o mesmo grafo
NODES = [(random.uniform(-100, 100), random.uniform(-100, 100)) for _ in range(10)]

INITIAL_PHEROMONE = 1.0
RHO = 0.1

clients = []
client_connections = []
best_tour = None
best_distance = float('inf')

def handle_client(conn, addr, edges, start_barrier):
    global best_tour, best_distance
    print(f"[COORD] Cliente conectado: {addr}")
    start_barrier.wait()
    print(f"[COORD] Cliente {addr} iniciando execução")
    for iteration in range(NUM_ITERATIONS):
        data = pickle.dumps((edges, iteration))
        conn.sendall(data)

        result = conn.recv(4096)
        tour, distance = pickle.loads(result)

        print(f"[COORD] Iteração {iteration} de {addr}: Distância = {distance:.2f}")

        if distance < best_distance:
            best_distance = distance
            best_tour = tour

        deposit_pheromone(edges, tour, distance, RHO)

    conn.close()
    print(f"[COORD] Cliente {addr} finalizou.")

def start_server():
    edges = build_graph(NODES, INITIAL_PHEROMONE)
    start_barrier = threading.Barrier(NUM_CLIENTS)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[COORD] Servidor escutando em {HOST}:{PORT}")

        for _ in range(NUM_CLIENTS):
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, edges, start_barrier))
            thread.start()
            clients.append(thread)

        for thread in clients:
            thread.join()

        print("\n[COORD] Melhor solução encontrada:")
        print(" -> ".join(str(i) for i in best_tour))
        print(f"Distância total: {best_distance:.2f}")
    
    with open("aco_result.pkl", "wb") as f:
        pickle.dump((NODES, best_tour, best_distance), f)

if __name__ == '__main__':
    start_server()