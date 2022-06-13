from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    A class that configures the blog app
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        """
        Imports signals
        Args:
            self (object): self.
        Returns:
            n/a
        """
        import blog.signals
