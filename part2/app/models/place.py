class Place:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __str__(self):
        return f"Place(name={self.name}, location={self.location})"

    # Additional methods for place-related functionality can be added here.