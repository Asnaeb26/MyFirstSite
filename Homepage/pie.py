# import matplotlib.pyplot as plt
# import numpy as np
# from Homepage.models import SpentMoney
#
# # def pie(*args):
# #     labels = ['Nokia', 'Samsung', 'Apple', 'Lumia']
# #     values = [10, 50, 25, 15]
# #     colors = ['yellow', 'green', 'red', 'blue']
# #     plt.pie(values, labels=labels, colors=colors)
# #     plt.axis('equal')
# #     plt.savefig('static/Homepage/pie.svg')
# #
# #
#
#
# # def pie(*args):
# #     all_objects = SpentMoney.objects.all()
# #     labels = []
# #     for label in all_objects:
# #         labels.append(label.category)
# #     labels = set(labels)
# #     dict = {}
# #     for j in labels:
# #         sum = 0
# #         for i in all_objects:
# #             if i.category == j:
# #                 sum += i.add_money
# #         dict[j] = sum
# #     return dict
#
# def pie(*args):
#     all_objects = SpentMoney.objects.all()
#     categories = []
#     for label in all_objects:
#         categories.append(label.category)
#     categories = set(categories)
#     labels = []
#     values = []
#     for j in categories:
#         total = 0
#         for i in all_objects:
#             if i.category == j:
#                 total += i.add_money
#         labels.append(j)
#         values.append(total)
#     # labels = ['Nokia', 'Samsung', 'Apple', 'Lumia']
#     # values = [20, 50, 25, 5]
#     # colors = ['yellow', 'green', 'red', 'blue']
#     plt.pie(values, labels=labels, autopct='%1.2f%%')
#     plt.axis('equal')
#     plt.legend(loc='best')
#     plt.savefig('static/Homepage/pie.svg')
#     return
#
#
# pie()
