#!/bin/bash

echo "Note that secret_key is not yet fully implemented"
python -c 'import os; print("".join([chr(ord(os.urandom(1))*(126-33)/255+33) for _ in range(32)]))' > secret_key
