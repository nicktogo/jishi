from db.factory import MongoFactory
from bson.objectid import ObjectId
from datetime import datetime

class CommentManager:
    def __init__(self):
        self._comments = MongoFactory().get_connection().get_collection(collection_name='comments')

    def create_comment(self, user_id, content, project_id):
        self._comments.insert_one({
            'userid': user_id,
            'content': content,
            'project_id': project_id,
            'created_time': datetime.now()
        }).inserted_id

    def del_comment(self, comment_id):
        self._comments.delete_one({'_id': ObjectId(comment_id)})

    def update_comment(self, comment_id, content):
        self._comments.update_one({
             '_id': ObjectId(comment_id)
        },{
            '$set': {
                'content': content
            }
        })

    def get_all_comment_by_projectid(self, project_id):
        return self._comments.find({
            'project_id': project_id
        })


if __name__ == '__main__':
    cm = CommentManager()


