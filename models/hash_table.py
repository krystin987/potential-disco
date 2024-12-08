class HashTable:
    def __init__(self, size=10):
        """
        Initializes the hash table with a specified size.
        Each index contains an empty list to handle collisions using chaining.
        """
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash_function(self, package_id):
        """
        Hash function to calculate the index for a given package ID.
        """
        return package_id % self.size

    def insert(self, package_id, address, deadline, city, zip_code, weight, status, special_note, start_time):
        """
        Inserts the package data into the hash table.
        :param package_id: Unique identifier for the package.
        :param address: Delivery address.
        :param deadline: Delivery deadline.
        :param city: Delivery city.
        :param zip_code: Delivery zip code.
        :param weight: Package weight.
        :param status: Delivery status.
        :param special_note: Special note related to the package.
        :param start_time: Start time for package delivery.
        """
        index = self._hash_function(package_id)
        bucket = self.table[index]

        # Check if the package ID already exists and update it
        for item in bucket:
            if item["package_id"] == package_id:
                item.update({
                    "address": address,
                    "deadline": deadline,
                    "city": city,
                    "zip_code": zip_code,
                    "weight": weight,
                    "status": status,
                    "special_note": special_note,
                    "start_time": start_time
                })
                return

        # If the package ID does not exist, insert it as a new entry
        package_data = {
            "package_id": package_id,
            "address": address,
            "deadline": deadline,
            "city": city,
            "zip_code": zip_code,
            "weight": weight,
            "status": status,
            "special_note": special_note,
            "start_time": start_time
        }
        bucket.append(package_data)

    def lookup(self, package_id):
        """
        Looks up a package by its ID and returns the corresponding data components.
        :param package_id: Unique identifier for the package.
        :return: Dictionary containing package data or None if not found.
        """
        index = self._hash_function(package_id)
        bucket = self.table[index]

        # Search for the package in the bucket
        for item in bucket:
            if item["package_id"] == package_id:
                return item

        # If not found, return None
        return None

    def __str__(self):
        """
        Returns a string representation of the hash table for easy visualization.
        """
        return str(self.table)