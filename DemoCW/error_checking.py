class TrackValueError(ValueError):
    def __init__(self, message="Track must be a non-empty string"):
        self.message = message
        super().__init__(self.message)

class ArtistValueError(ValueError):
    def __init__(self, message="Artist must be a non-empty string"):
        self.message = message
        super().__init__(self.message)

class RatingValueError(ValueError):
    def __init__(self, message ="Rating must be an integer between 1 and 5"):
        self.message = message
        super().__init__(self.message)

class PlayCountValueError(ValueError):
    def __init__(self, message="Play count must be a non-negative integer"):
        self.message = message
        super().__init__(self.message)