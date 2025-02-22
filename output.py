
import pandas as pd

class output():
    def __init__(self):
        self.date_lst = []
        self.close_lst = []
        self.signal_lst = []
        self.prev_signal_lst = []
        self.action_lst = []


    def save_csv(self, contents, dframe, signal, prev_signal, predict_result):
        date = contents[-1][0]
        close = dframe['close'].iloc[-1]
        

        self.date_lst.append(date)
        self.close_lst.append(close)
        self.signal_lst.append(signal)
        self.prev_signal_lst.append(prev_signal)
        self.action_lst.append(predict_result["action"])


    def output_csv(self):
        output_lst = [self.date_lst,  self.close_lst, self.signal_lst, self.prev_signal_lst, self.action_lst]
        df_output = pd.DataFrame(output_lst).transpose()
        df_output.columns=['date','close_price', 'signal','prev_signal','action']
        df_output.to_csv("output.csv", index=False)


"""
import pandas as pd

class Output:
    def __init__(self):
        self.date_lst = []
        self.open_lst = []
        self.high_lst = []
        self.low_lst = []
        self.close_lst = []
        self.tick_volume_lst = []
        self.pos_lst = []
        self.signal_lst = []
        self.prev_signal_lst = []
        self.action_lst = []

    def save_csv(self, contents, dframe, signal, prev_signal, predict_result):
        # ذخیره داده‌های `contents`
        self.date_lst.append(contents[-1][0])
        self.open_lst.append(contents[-1][1])
        self.high_lst.append(contents[-1][2])
        self.low_lst.append(contents[-1][3])
        self.close_lst.append(dframe['close'].iloc[-1])
        self.tick_volume_lst.append(contents[-1][5])
        self.pos_lst.append(contents[-1][6])

        # ذخیره داده‌های سیگنال و اکشن
        self.signal_lst.append(signal)
        self.prev_signal_lst.append(prev_signal)
        self.action_lst.append(predict_result["action"])

    def output_csv(self):
        # ساخت لیست‌های خروجی
        output_lst = [
            self.date_lst,
            self.open_lst,
            self.high_lst,
            self.low_lst,
            self.close_lst,
            self.tick_volume_lst,
            self.pos_lst,
            self.signal_lst,
            self.prev_signal_lst,
            self.action_lst,
        ]
        # تبدیل به DataFrame
        df_output = pd.DataFrame(output_lst).transpose()
        df_output.columns = [
            "date",
            "open",
            "high",
            "low",
            "close_price",
            "tick_volume",
            "pos",
            "signal",
            "prev_signal",
            "action",
        ]
        # ذخیره به فایل CSV
        df_output.to_csv("output.csv", index=False)
        
        
"""
