from db.factory import MongoFactory
from bson.objectid import ObjectId
import numpy as np

class recommendDesigner():
    def __init__(self):
        self._projects = MongoFactory().get_connection().get_collection(collection_name='projects')
        self._users = MongoFactory().get_connection().get_collection(collection_name='users')
        self.weChat = [0.15,0.25,0.1,0.4,0.1]
        self.App = [0.25,0.35,0.1,0.2,0.1]
        self.Sitp = [0.4,0.15,0.2,0.15,0.1]
        self.ShanghaiInnovate = [0.3,0.1,0.1,0.2,0.3]
        self.mathModeling = [0.2,0.1,0.4,0.25,0.05]

    def createPoi(self, project_id):
        project = self._projects.find_one({
            '_id': ObjectId(project_id)
        })
        type= project['type']
        pp = [self.weChat,self.App,self.Sitp,self.mathModeling,self.ShanghaiInnovate]
        p = pp[int(type)]
        self._projects.update({
            '_id': ObjectId(project_id)
        },{
            '$set':{
                'Poi': p
            }
        })

    def recomendSta(self,username):
        user = self._users.find_one({
            'username':username
        })
        u_poi = np.array(user['Poi'])
        projects = list(self._projects.find())
        projects_poi = np.array(map(lambda x: x['Poi'], projects))
        result = np.dot(projects_poi, u_poi.reshape(-1, 1))
        for i, project in enumerate(projects):
            project['rate'] = result[i,0]
        projects.sort(key=lambda x: x['rate'], reverse=True)
        return projects[:3]



    def createUPoi(self, user_id):
        user = self._users.find_one({
            '_id':ObjectId(user_id)
        })
        pp = [self.weChat,self.App,self.Sitp,self.mathModeling,self.ShanghaiInnovate]
        pois = user['interest']
        upoi = np.array([0,0,0,0,0])
        for poi in pois:
            poi = np.array(pp[int(poi)])
            upoi = upoi + poi
        if len(pois) != 0:
            upoi = upoi/len(pois)
            print 'result'
        else:
            upoi = [0.2,0.2,0.2,0.2,0.2]
            print 'result'
        return self._users.update_one({
            '_id':ObjectId(user_id)
        },{
            '$set':{
                'Poi': list(upoi)
            }
        })

    def updatePoi(self,p_id,u_id):
        user = self._users.find_one({
            '_id': ObjectId(u_id)
        })
        project = self._projects.find_one({
            '_id': ObjectId(p_id)
        })
        u_poi = np.array(user['Poi'])
        p_poi = np.array(project['Poi'])
        u_npoi = (u_poi + p_poi) * 0.5
        p_npoi = (0.1 * u_poi + p_poi)/1.1
        self._user.update({
            '_id',ObjectId(u_id)
        },{
            '$set':{
                'Poi': u_npoi
            }
        }
        )
        self._projects.update({
            '_id',ObjectId(p_id)
        },{
            '$set':{
                'Poi': p_npoi
            }
        })


if __name__ == '__main__':
    rm = recommendDesigner()
    rm.recomendSta('5148478576')
