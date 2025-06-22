class Review:
    def __init__(self, rating, comment):
        self.rating = rating
        self.comment = comment

    def __str__(self):
        return f'Review(rating={self.rating}, comment="{self.comment}")'