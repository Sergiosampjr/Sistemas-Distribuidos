#!/bin/bash

PYTHON=/home/sergio_nunes/Documentos/GitHub/Sistemas-Distribuidos/venv/bin/python3

for i in {1..10}
do

```
PORT=$((5000+i))

NODES=""

for j in {1..10}
do
    if [ $i -ne $j ]; then
        NODES="$NODES http://10.0.0.$j:$((5000+j))"
    fi
done

MODE="none"
RATE="0.0"

# Escolha os drones bizantinos aqui
if [ $i -eq 3 ]; then
    MODE="byzantine"
    RATE="1.0"
fi

h$i $PYTHON bft_drone.py drone$i $PORT $MODE $RATE $NODES &
```

done
