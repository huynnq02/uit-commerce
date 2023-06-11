
# class ItemDocument(Document):
#     name = Text()

#     class Index:
#         name = 'items'  # Specify the Elasticsearch index name

#     @classmethod
#     def search(cls, query):
#         search = Search(index=cls.Index.name).query('match', name=query)
#         response = search.execute()
#         return response