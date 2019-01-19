def switchTriggerType(trigger):
    triggertype = {
        "OpenPanel":{
            "Data":{
                "TriggerType": "OpenPanel",
                "PanelName": str(input("输入面板名称："))
            }  
        },
    }
    return triggertype.get(trigger)