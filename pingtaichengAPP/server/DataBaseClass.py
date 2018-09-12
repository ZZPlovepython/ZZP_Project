import mysql.connector
import datetime
from datetime import timedelta


class DataBaseOperation(object):
    """Class for DataBase operation
       main property:
       list factorylist
       dic Eqpdic {facID: Eqplist}(list Eqplist)
       datetime date
       DBconnect DBconnector
       Operation:
       string newFactory(self, string facID, string address, string responsor)
       string newEquipment(self, String facID, string EqpID, dic SP)
       string maintainDB(self)"""

    def __init__(self, arg):
        super(DataBaseOperation, self).__init__()
        self.factoryList = []
        self.Eqpdic = {}
        self.config = {'host': '127.0.0.1',
                       'user': 'root',
                       'password': '123456',
                       'port': 3306,
                       'database': 'scaleserver',
                       'charset': 'utf8'}
        try:
            self.cnn = mysql.connector.connect(**self.config)
        except mysql.connector.Error as e:
            print('connect fails!{}'.format(e))

    def newFactory(self, facID, address, responsor):
        cursor = self.cnn.cursor()
        queryString = ("select * from factory where ID = %s" % facID)
        result = cursor.execute(queryString).fetchall()
        if (not result):
            return "Factory exist, create database fail!"
        else:
            queryString = ("insert into factory(ID, address, responsor) values (%s, %s, %s)" % (facID, address, responsor))
            cursor.execute(queryString)
            cursor.commit()
            queryString = ("CREATE TABLE `%s` (`ID` varchar(20) NOT NULL, `supplier` varchar(20) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `supplier` (`supplier`),CONSTRAINT `equipment_ibfk_1` FOREIGN KEY (`supplier`) REFERENCES `supplier` (`ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + "Eqp"))
            cursor.execute(queryString)
            queryString = ("CREATE TABLE `%s` (`ID` varchar(20) NOT NULL,`info` varchar(100) DEFAULT NULL,`contact` varchar(20) DEFAULT NULL,PRIMARY KEY (`ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + "Sup"))
            cursor.execute(queryString)
            queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`EqpID` varchar(20) DEFAULT NULL,`Timestamp` datetime DEFAULT NULL,`fault` int(11) DEFAULT NULL,`alarm` int(11) DEFAULT NULL,`nromal` int(11) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `EqpID` (`EqpID`),KEY `ix_countState_Timestamp` (`Timestamp`),CONSTRAINT `countstate_ibfk_1` FOREIGN KEY (`EqpID`) REFERENCES `equipment` (`ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + "countState"))
            cursor.execute(queryString)
            cursor.close()
            return "New Factory Create Successfully"

    def newEquip(self, facID, EqpID, SPdic):
        cursor = self.cnn.cursor()
        queryString = ("select * from %s where ID = %s" % (facID + "Eqp", EqpID))
        result = cursor.execute(queryString).fetchall()
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if result:
            queryString = ("insert into %s (`Timestamp`, `SencerNum`, `SencerName`, `EqpID`, `NoLoad_set`, `EmptyLoad_set`, `Temp`, `Wet`, `ExcV`, `Sensitivity`, `Resistance`, `standard`, `zeropoint`) VALUES (%s,%d,%s,%s,%s,%s,%f,%f,%s,%s,%s,%s,%s)" % (date, SPdic['Num'], SPdic['Name'], EqpID, SPdic['Noload'], SPdic['Empty'], SPdic['Temp'], SPdic['Wet'], SPdic['ExcV'], SPdic['Sensivity'], SPdic['Resistance'], SPdic['Standard'], SPdic['Zeropoint']))
            cursor.execute(queryString)
            cursor.commit()
            return "Equipment is exicted, updating the thread"
        else:
            queryString = ("insert into %s(ID,supplier) values(%s, %s)" % (facID + "Eqp", EqpID, SPdic['supplier']))
            cursor.execute(queryString)
            cursor.commit()
            queryString = ("select * from %s where ID = %s" % (facID + "Sup", SPdic['supplier']))
            result1 = cursor.execute(queryString).fetchall()
            if (not result1):
                queryString = ("insert into %s(ID,info,contact) values(%s, %s, %s)" % (facID + "Sup", SPdic['supplier'], SPdic['info'], SPdic['contact']))
                cursor.execute(queryString)
                cursor.commit()
            queryString = ("insert into %s(EqpID,Timestamp,fault,alarm,normal) values(%s, %s, 0,0,0)" % (facID + "countstate", EqpID, date))
            cursor.execute(queryString)
            cursor.commit()
            queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`SencerNum` int(11) DEFAULT NULL,`SencerName` varchar(125) DEFAULT NULL,`EqpID` varchar(20) DEFAULT NULL,`NoLoad_set` varchar(100) DEFAULT NULL,`EmptyLoad_set` varchar(100) DEFAULT NULL,`Temp` float DEFAULT NULL,`Wet` float DEFAULT NULL,`ExcV` varchar(100) DEFAULT NULL,`Sensitivity` varchar(100) DEFAULT NULL,`Resistance` varchar(100) DEFAULT NULL,`standard` varchar(100) DEFAULT NULL,`zeropoint` varchar(100) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `EqpID` (`EqpID`),KEY `ix_Thread_Timestamp` (`Timestamp`),CONSTRAINT `thread_ibfk_1` FOREIGN KEY (`EqpID`) REFERENCES `equipment` (`ID`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + EqpID +"Thread"))
            cursor.execute(queryString)
            queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`record` varchar(250) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `ix_Operation_Timestamp` (`Timestamp`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + EqpID +"operation"))
            cursor.execute(queryString)
            queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`WeightTag1` float DEFAULT NULL,`WeightTag2` float DEFAULT NULL,`WeightTag3` float DEFAULT NULL,`WeightTag4` float DEFAULT NULL,`Weight` float DEFAULT NULL,PRIMARY KEY (`ID`),KEY `ix_NewVal_Timestamp` (`Timestamp`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + EqpID + "NewVal" + date[:10]))
            cursor.execute(queryString)
            queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`faultCode` int(11) DEFAULT NULL,`eqpState` int(11) DEFAULT NULL,`faultTime` datetime DEFAULT NULL,`RecoverTime` datetime DEFAULT NULL,`PeriodSecond` int(11) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `ix_FaultMsg_Timestamp` (`Timestamp`),KEY `ix_FaultMsg_faultTime` (`faultTime`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (facID + EqpID + "FaultMsg" + date[:10]))
            cursor.execute(queryString)
            queryString = ("insert into %s (`Timestamp`, `SencerNum`, `SencerName`, `EqpID`, `NoLoad_set`, `EmptyLoad_set`, `Temp`, `Wet`, `ExcV`, `Sensitivity`, `Resistance`, `standard`, `zeropoint`) VALUES (%s,%d,%s,%s,%s,%s,%f,%f,%s,%s,%s,%s,%s)" % (date, SPdic['Num'], SPdic['Name'], EqpID, SPdic['Noload'], SPdic['Empty'], SPdic['Temp'], SPdic['Wet'], SPdic['ExcV'], SPdic['Sensivity'], SPdic['Resistance'], SPdic['Standard'], SPdic['Zeropoint']))
            cursor.execute(queryString)
            cursor.commit()
            return "Equipment create successfully!"

    def maintainDB(self):
        cursor = self.cnn.cursor()
        queryString = ("select ID from factory")
        createDate = (datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
        result = cursor.execute(queryString).fetchall()
        if result:
            for item in result:
                self.factorylist.append(item)
                queryString = ("select ID from %s" % (item + 'Eqp'))
                result1 = cursor.execute(queryString).fetchall()
                if result1:
                    self.Eqpdic[item] = result1
                else:
                    return "No Equipment in factory %s" % item
            for fac in self.factorylist:
                for eqp in self.Eqplist[fac]:
                    queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`WeightTag1` float DEFAULT NULL,`WeightTag2` float DEFAULT NULL,`WeightTag3` float DEFAULT NULL,`WeightTag4` float DEFAULT NULL,`Weight` float DEFAULT NULL,PRIMARY KEY (`ID`),KEY `ix_NewVal_Timestamp` (`Timestamp`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (fac + eqp + "NewVal" + createDate[:10]))
                    cursor.execute(queryString)
                    queryString = ("CREATE TABLE `%s` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Timestamp` datetime DEFAULT NULL,`faultCode` int(11) DEFAULT NULL,`eqpState` int(11) DEFAULT NULL,`faultTime` datetime DEFAULT NULL,`RecoverTime` datetime DEFAULT NULL,`PeriodSecond` int(11) DEFAULT NULL,PRIMARY KEY (`ID`),KEY `ix_FaultMsg_Timestamp` (`Timestamp`),KEY `ix_FaultMsg_faultTime` (`faultTime`)) ENGINE=InnoDB DEFAULT CHARSET=utf8" % (fac + eqp + "FaultMsg" + createDate[:10]))
                    cursor.execute(queryString)
            return "create DB successfully"
        else:
            return "No factory please create factory first"
