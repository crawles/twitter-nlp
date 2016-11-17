import time

import numpy as np
import pandas as pd

log_df = pd.DataFrame(columns = ['time'])

def num_connects_in_last_n(log, nmin):
    '''Trims log and counts number of connections in last nmin'''
    del_log = time.time() - np.array(log)
    nsec= nmin * 60
    log = np.array(log)[del_log <= (nsec)]
    return list(log), len(log)
