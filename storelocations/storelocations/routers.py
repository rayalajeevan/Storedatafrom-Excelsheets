class Router:
    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to users_db.
        """
        if model._meta.app_label == 'web_scrapping':
            return 'scrap'
        if model._meta.app_label=='pushcompany':
            return 'developers'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to users_db.
        """
        if model._meta.app_label == 'web_scrapping':
            return 'scrap'
        if model._meta.app_label=='pushcompany':
            return 'developers'
        return None
