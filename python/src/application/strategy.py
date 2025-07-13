import os
import json
import numpy as np
from backtesting import Strategy


class OrderBookStrategy(Strategy):

    delta_jump_level = 15
   
    def init(self):
        super().init()

        delta = self.data.df['delta']
        mask_up = self.data.df['delta'] > self.delta_jump_level
        mask_down = self.data.df['delta'] < -self.delta_jump_level

        signal = np.zeros(len(delta))
        signal[mask_up] = 1
        signal[mask_down] = -1

        self.signal = self.I(lambda x: x, signal)

    def next(self):

        if not self.position:
            
            if self.signal[-1] == 1:
                tp = self.data.mid_price[-1] + 0.02 * self.data.mid_price[-1]
                sl = self.data.mid_price[-1] - 0.01 * self.data.mid_price[-1]
                self.sell(tp=tp, sl=sl)
            
            elif self.signal[-1] == -1:
                tp = self.data.mid_price[-1] - 0.02 * self.data.mid_price[-1]
                sl = self.data.mid_price[-1] + 0.01 * self.data.mid_price[-1]
                self.sell(tp=tp, sl=sl)
        
        super().next()
        

from pprint import pprint
        
def save_strategy_result(stats: dict, save_folder_path=None) -> str:
    
    output_str = '\n'.join([f"{k:<25}: {round(v,5) if isinstance(v, float) else v}" for k,v in stats.items() if not k.startswith('_')])

    if save_folder_path:
        with open(os.path.join(save_folder_path, 'strategy_report.txt'), 'w', encoding='utf8') as file:
            file.write(output_str)
    
    if not stats['_trades'].empty:
        trades = stats['_trades'].to_json(orient="index")
        parsed = json.loads(trades)        
        with open(os.path.join(save_folder_path, 'strategy_trades.json'), "w") as f:
            json.dump(parsed, f, indent=4)   

    return output_str
    

