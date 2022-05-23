

# # Django
# from django.db import models

# # Utils
# from trello.utils.models import TrelloModel


# class Card(TrelloModel):
#     """Card Model"""

#     # list = models.ForeignKey('space_works.List', on_delete=models.CASCADE)


# class Comment(TrelloModel):
#     """ Comment model
#     + description
#     + created
#     + modified
#     """
#     name = None

#     # membership = models.ForeignKey('space_works.Membership', on_delete=models.CASCADE)

#     # card = models.ForeignKey(Card, on_delete=models.CASCADE)

#     def __str__(self):
#         """Return description by username """
#         return f"{self.description} by @{self.membership.user.username}"
