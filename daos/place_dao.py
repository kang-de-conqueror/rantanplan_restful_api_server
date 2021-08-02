from utils.my_connection import MyConnection
from dtos.place_dto import PlaceDTO
from dtos.signal_dto import SignalDTO


class PlaceDAO:
    def add_signal_identified_place(self, id, data):
        my_connection = MyConnection()
        isCreated = False
        scan_id = 0
        try:
            conn = my_connection.conn
            cursor = my_connection.cursor
            insert_place_sql = "INSERT INTO Places(ID, Name, Address) VALUES(?,?,?)"
            insert_place_values = [id, data.get(
                "place_name"), data.get("place_address")]
            cursor.execute(insert_place_sql, insert_place_values)
            insert_scan_sql = "INSERT INTO Implementations(StartTime, EndTime, RoundCount, PlaceID) OUTPUT Inserted.ID VALUES(?,?,?,?)"
            insert_scan_values = [data.get("start_time"), data.get(
                "end_time"), data.get("round_count"), id]
            cursor.execute(insert_scan_sql, insert_scan_values)
            for row in cursor.fetchall():
                scan_id = row[0]
            insert_signal_sql = "INSERT INTO Signals(BSSID, SSID, Frequency, SignalLevel, SampleCount, ImplementationID) VALUES(?,?,?,?,?,?)"
            for elm in data.get("signals"):
                insert_signal_values = [elm["bssid"], elm["ssid"], elm["frequency"],
                                      elm["signal_level"], elm["sample_count"], scan_id]
                cursor.execute(insert_signal_sql, insert_signal_values)
            conn.commit()
            isCreated = True
        except Exception as e:
            my_connection.conn.rollback()
            isCreated = False
            raise Exception(e)
        finally:
            my_connection.conn.close()
        return isCreated

    def add_signal_existed_place(self, id, data):
        my_connection = MyConnection()
        isCreated = False
        scan_id = 0
        try:
            conn = my_connection.conn
            cursor = my_connection.cursor
            insert_scan_sql = "INSERT INTO Implementations(StartTime, EndTime, RoundCount, PlaceID) OUTPUT Inserted.ID VALUES(?,?,?,?)"
            insert_scan_values = [data.get("start_time"), data.get(
                "end_time"), data.get("round_count"), id]
            cursor.execute(insert_scan_sql, insert_scan_values)
            for row in cursor.fetchall():
                scan_id = row[0]
            insert_signal_sql = "INSERT INTO Signals(BSSID, SSID, Frequency, SignalLevel, SampleCount, ImplementationID) VALUES(?,?,?,?,?,?)"
            for elm in data.get("signals"):
                insert_signal_values = [elm["bssid"], elm["ssid"], elm["frequency"],
                                      elm["signal_level"], elm["sample_count"], scan_id]
                cursor.execute(insert_signal_sql, insert_signal_values)
            conn.commit()
            isCreated = True
        except Exception as e:
            my_connection.conn.rollback()
            isCreated = False
            raise Exception(e)
        finally:
            my_connection.conn.close()
        return isCreated

    def search_place(self, core_signal, map_place, map_place_signal):
        my_connection = MyConnection()
        try:
            conn = my_connection.conn
            cursor = my_connection.cursor
            select_signal_sql = '''
                    SELECT p.ID as PlaceID, p.Name, p.Address, i.ID, i.StartTime,
                    i.EndTime, i.RoundCount, si.ID, si.BSSID, si.SSID, si.Frequency,
                    si.SignalLevel, si.SampleCount FROM Places p INNER JOIN Implementations i
                    ON i.PlaceID = p.ID INNER JOIN Signals si ON si.ImplementationID = i.ID
                    WHERE si.BSSID=?
                    '''
            select_signal_values = [core_signal.get("bssid")]
            cursor.execute(select_signal_sql, select_signal_values)
            for row in cursor.fetchall():
                place_id = row[0]
                place_name = row[1]
                place_address = row[2]
                place_dto = PlaceDTO(place_id, place_name, place_address)

                bssid = row[8]
                ssid = row[9]
                frequency = row[10]
                signal_level = row[11]
                sample_count = row[12]
                row_signal = SignalDTO(bssid, ssid, frequency, signal_level, sample_count)
                if place_id not in map_place:
                    map_place[place_id] = place_dto

                if place_id in map_place_signal:
                    current_signal_list = map_place_signal[place_id]
                    isExisted = False
                    for index, value in enumerate(current_signal_list):
                        current_signal = value
                        if current_signal.bssid == row_signal.bssid:
                            core_signal_level = int(core_signal.get("signal_level"))
                            row_signal_level = int(row_signal.signal_level)
                            current_signal_level = int(current_signal.signal_level)
                            if abs(current_signal_level - core_signal_level) >= abs(row_signal_level - core_signal_level):
                                current_signal_list[index] = row_signal
                            isExisted = True
                            break
                    if not isExisted:
                        current_signal_list.append(row_signal)
                else:
                    map_place_signal[place_id] = [row_signal]
        except Exception as e:
            raise Exception(e)
        finally:
            my_connection.conn.close()
