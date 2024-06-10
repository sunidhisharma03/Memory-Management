import csv
import matplotlib.pyplot as plt

# Define the file path
file_path = './pages/memory_log.csv'

# Initialize variables to store memory and partitions data
buddy_memory, dynamic_memory, fixed_memory = 0, 0, 0
buddy_partition, dynamic_partition, fixed_partition = 0, 0, 0

# Read the data from the CSV file
with open(file_path, 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row

    for row in reader:
        if row[0] == "buddy":
            buddy_memory = int(row[1])
            buddy_partition = int(row[2])
        elif row[0] == "dynamic":
            dynamic_memory = int(row[1])
            dynamic_partition = int(row[2])
        elif row[0] == "fixed":
            fixed_memory = int(row[1])
            fixed_partition = int(row[2])

# Calculate efficiency
effi_buddy = ((1024 - buddy_memory) / 1024) * 100
effi_dynamic = ((1024 - dynamic_memory) / 1024) * 100
effi_fixed = ((1024 - fixed_memory) / 1024) * 100

# Print efficiency values
print(f"Buddy Efficiency: {effi_buddy}%")
print(f"Dynamic Efficiency: {effi_dynamic}%")
print(f"Fixed Efficiency: {effi_fixed}%")

# Create bar graph for efficiency
efficiencies = [effi_buddy, effi_dynamic, effi_fixed]
labels = ['Buddy', 'Dynamic', 'Fixed']
plt.figure(figsize=(10, 5))
plt.bar(labels, efficiencies, color=['blue', 'green', 'red'])
plt.xlabel('Memory Management Type')
plt.ylabel('Efficiency (%)')
plt.title('Memory Management Efficiency')
plt.show()

# Create line graph for partitions
partitions = [buddy_partition, dynamic_partition, fixed_partition]
plt.figure(figsize=(10, 5))
plt.plot(labels, partitions, marker='o', linestyle='-', color='purple')
plt.xlabel('Memory Management Type')
plt.ylabel('Number of Partitions')
plt.title('Number of Partitions in Memory Management')
plt.show()
