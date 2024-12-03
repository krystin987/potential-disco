from models.hash_table import HashTable

# Example usage
hash_table = HashTable(size=10)
hash_table.insert(1, "123 Main St", "EOD", "Salt Lake City", "84101", 5.0, "At the hub")
hash_table.insert(2, "456 Elm St", "10:30 AM", "Salt Lake City", "84115", 2.5, "En route")
print(hash_table)

# Look up package with ID 1
package = hash_table.lookup(1)
if package:
    print("Package found:", package)
else:
    print("Package not found.")