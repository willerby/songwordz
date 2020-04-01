class Results:
    def __init__(self, ps_error=None, pd_results=None, pl_results=None):
        self.b_error = True if ps_error else False
        self.s_error_message = ps_error
        self.d_result = pd_results
        self.l_result = pl_results
