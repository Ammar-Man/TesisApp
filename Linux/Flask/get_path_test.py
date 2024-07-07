import http.server
import socketserver
import os

# Get the current working directory
current_path = os.getcwd()
print(f"Current path is: {current_path}")

# Define the new target path
target_path = os.path.join(os.path.dirname(current_path), 'Tablet')

# Change the working directory to the new target path
os.chdir(target_path)

# Verify the change
new_path = os.getcwd()
print(f"New path is: {new_path}")