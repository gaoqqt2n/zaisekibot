import sqlite3
import os

dbname = 'database.sqlite3'

class ReaderWriter(object):
    __select_query = 'select condition from members where id LIKE ?'

    def Execute(self, query, params):
        self.cursor.execute(query, params)
        self.db.commit()

    def ConnectToDB(self):
        self.db = sqlite3.connect(dbname)
        self.cursor = self.db.cursor()

    def Delete(self, id):
        id_datas = (id,)
        query = 'delete from members where id=?'
        self.cursor.execute(query, id_datas)
        query = 'delete from timecard where id=?'
        self.cursor.execute(query, id_datas)
        self.db.commit()

    def ToggleCondition(self, id):
        sel_data = (id,)
        self.cursor.execute(self.__select_query, sel_data)
        upd_query1 = 'update members set condition=? where id LIKE ?'
        result = self.cursor.fetchone()
        self.UpdateTime(id, 0 if result[0] == 1 else 0)
        if result[0] == 0:
            upd_data1 = (2, id)
        else:
            upd_data1 = (0, id)

        self.cursor.execute(upd_query1, upd_data1)
        self.db.commit()

    def Getcondition(self, id):
        sel_data = (id,)
        self.cursor.execute(self.__select_query, sel_data)
        result = self.cursor.fetchone()
        return result[0]

    def ChangeCondition(self, id, condition):
        query = 'update members set condition=? where id LIKE ?'
        set_data = (condition, id)
        current_Condition = self.Getcondition(id)
        if condition == 0 and current_Condition != 0:
            self.UpdateTime(id, 0)
        elif current_Condition == 0 and condition != 0:
            self.UpdateTime(id, 1)
        else:
            pass
        self.cursor.execute(query, set_data)
        self.db.commit()

    def UpdateTime(self, id, to_in_or_out):
        id_data = (id,)
        if to_in_or_out == 0:
            upd_query2 = '''update timecard set login_time=strftime("%Y%m%d%H%M%S",
                            datetime(datetime(),"localtime")) where id LIKE ?'''
        else:
            upd_query2 = '''update timecard set logout_time=strftime("%Y%m%d%H%M%S",
                            datetime(datetime(),"localtime")) where id LIKE ?'''
        self.cursor.execute(upd_query2, id_data)

    def GetName(self, id):
        query = 'select name from members where id LIKE ?'
        id_data = (id,)
        res = self.cursor.execute(query, id_data)
        return res.fetchone()

    def GetZaishituUsers(self):
        query = 'select name from members where condition=0'
        res = self.cursor.execute(query)
        return res

    def GetGakunaiUsers(self):
        query = 'select name from members where condition=1'
        res = self.cursor.execute(query)
        return res

    def GetSugumodoruUsers(self):
        query = 'select name from members where condition=3'
        res = self.cursor.execute(query)
        return res

    def Show(self):
        query = 'select * from members'
        for row in self.cursor.execute(query):
            print(row)

    def Regist(self, code, name):
        query = 'insert into members values(?,?,0)'
        q_data = (code, name)
        self.cursor.execute(query, q_data)
        query = 'insert into timecard values(?,strftime("%Y%m%d%H%M%S",datetime(datetime(),"localtime")),"00000000000000")'
        q_data = (code,)
        self.cursor.execute(query, q_data)
        self.db.commit()

    def Close(self):
        self.db.close()