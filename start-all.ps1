# start_distributed_aco.ps1

# Caminho do diretório onde estão os arquivos
$path = "D:\Distributed-AntCollony"  # Substitua pelo caminho real

Start-Process powershell -ArgumentList "cd '$path'; python server.py"
Start-Sleep -Seconds 1
Start-Process powershell -ArgumentList "cd '$path'; python client.py"
Start-Process powershell -ArgumentList "cd '$path'; python client.py"
