import json
from GuideNode import switchTriggerType

class GuideNode():
    """ 
    自定义生成GuideNode的类
    生成对象需要传递GuideNode的名称，以及是否有前置步骤（默认为True）
    """
    def __init__(self,GuideName:'str',hasPre:'bool'=True):
        self.__GuideName = GuideName
        self.__hasPre = hasPre
        if  self.__hasPre:
            self.__json_data = {
            "GuideName":self.__GuideName,
            "Triggers":[],
            "Preconditions":[],
            "NodeData":[]
            }
            
        else:
            self.__json_data = {
                "GuideName":self.__GuideName,
                "Triggers":[],
                "NodeData":[]
            }
    
    def creatTriggersData(self,*triggertypes):
        self.__triggertypes = triggertypes
        for trigger in self.__triggertypes:
            self.__triggerdata = switchTriggerType.switchTriggerType(trigger)
            self.__json_data["Triggers"].append(self.__triggerdata)


    def saveGuideJson(self):
        path = self.__GuideName + '.json'
        with open(path,'w',encoding='utf8') as fp:
            json.dump(self.__json_data,fp,ensure_ascii=False)


    
