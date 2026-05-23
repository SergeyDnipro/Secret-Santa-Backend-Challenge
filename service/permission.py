class PermissionService:
    def __init__(self, *, admin_ids):
        self.admin_ids = admin_ids

    def is_admin(self, user_id):
        return user_id in self.admin_ids
