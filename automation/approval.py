from database.database import update_post_status

def approve_post(post_id):
    update_post_status(post_id, 'approved')

def reject_post(post_id):
    update_post_status(post_id, 'rejected')
