from django.urls import reverse

def get_obj_admin_change_url(obj, link_text=None):
    if not link_text:
        link_text = str(obj)
    url = reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',  args=[obj.id] )
    return f'<a href="{url}">{link_text}</a>'