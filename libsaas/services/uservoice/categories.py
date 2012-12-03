from . import resource


class ForumCategoriesBase(resource.UserVoiceResource):

    path = 'categories'

    def wrap_object(self, name):
        return {'category': name}



class ForumCategories(ForumCategoriesBase):
    pass


class ForumCategory(ForumCategoriesBase):
    pass
