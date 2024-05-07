from model.Base import Base

class CovidData(Base):
    """
    新冠数据
    """

    def __init__(self):
        super(CovidData, self).__init__('covid_data', 'id')

class Notice(Base):
    """
    预告
    """

    def __init__(self):
        super(Notice, self).__init__('notice', 'id')