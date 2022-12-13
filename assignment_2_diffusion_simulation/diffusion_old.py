class Diffusion:

    def __init__(self, rows = 10, cols = 10, bc_settings = [1,1,1,1], left_bc = None, right_bc = None, top_bc = None, bottom_bc = None):
        self.rows  = int(rows)
        self.cols = int(cols)
        self.bc_settings = list(map(int,bc_settings))

        # set default values if none is passed into arguments
        if left_bc is None:
            self.left_bc = list(map(float,rows*[0]))
        else:
            self.left_bc = list(map(float,left_bc))

        if right_bc is None:
            self.right_bc = list(map(float,rows*[0]))
        else:
            self.right_bc = list(map(float,right_bc))

        if top_bc is None:
            self.top_bc = list(map(float,cols*[0]))
        else:
            self.top_bc = list(map(float,top_bc))

        if bottom_bc is None:
            self.bottom_bc = list(map(float,cols*[0]))
        else:
            self.bottom_bc = list(map(float,bottom_bc))

        # initialise 2D array of space with default values of 0.0
        self.space = [[0.0 for i in range(self.cols)] for j in range(self.rows)]
        
    def set_cell(self, row_range, column_range, state):
        # iterate over the row and column indexes and set to state
        for row in range(row_range[0],row_range[1]+1):
            for col in range(column_range[0],column_range[1]+1):
                
                self.space[row][col] = float(state)

    def print_space(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(f'{self.space[i][j]:10.6f}',end='')
            print()
            
    
    def du_x(self, row_idx, col_idx):   

        # if index is not at left or right border
        if col_idx < self.cols-1 and col_idx > 0: 
            du_x = self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] + self.space[row_idx][col_idx-1]
        # if index given is at the right border
        elif col_idx == self.cols-1: 
            # check boundary condition at right border
            bc_setting_right = self.bc_settings[1]
            if bc_setting_right == 1:
                du_x = self.right_bc[row_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx][col_idx - 1]
            else:
                du_x = 2*self.space[row_idx][col_idx-1] - 2*self.space[row_idx][col_idx] + 2*self.right_bc[row_idx]
        #if index given is at the left border
        elif col_idx == 0: 
            # check boundary condition at left border
            bc_setting_left = self.bc_settings[0]
            if bc_setting_left == 1: 
                du_x = self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] + self.left_bc[row_idx]
            else:
                du_x = 2*self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] - 2*self.left_bc[row_idx]
                
        return du_x
        
    def du_y(self, row_idx, col_idx):
        # if is not at top or bottom border
        if row_idx < self.rows-1 and row_idx > 0: 
            du_y = self.space[row_idx +1][col_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx-1][col_idx]
        # if index given is at bottom border
        elif row_idx == self.rows-1: 
            # check boundary condition at bottom border
            bc_setting_bottom = self.bc_settings[3]
            if bc_setting_bottom == 1:
                du_y = self.bottom_bc[col_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx-1][col_idx]
            else:
                du_y = 2*self.space[row_idx-1][col_idx] - 2*self.space[row_idx][col_idx] + 2*self.bottom_bc[col_idx]
        # if index given is at top border
        elif row_idx == 0: 
            # check boundary condition at top border
            bc_setting_top = self.bc_settings[2]
            if bc_setting_top == 1:
                du_y = self.space[row_idx+1][col_idx] - 2*self.space[row_idx][col_idx] + self.top_bc[col_idx]
            else:
                du_y = 2*self.space[row_idx+1][col_idx] - 2*self.space[row_idx][col_idx] - 2*self.top_bc[col_idx]
        
        return du_y

    # calculate the final delta u at the index given
    def du(self,row_idx,col_idx):
        delta_x = self.du_x(row_idx,col_idx)
        delta_y = self.du_y(row_idx,col_idx)
        du = 0.0001*(delta_x + delta_y)
        return du


    def next_step(self, n_steps): 
        n_steps = int(n_steps)
        # iterate for n_steps times, for every single particle within space
        # for n in range(n_steps+1):
        for n in range(n_steps):
            for i in range(0,self.rows):
                for j in range(0,self.cols):
                    du =  self.du(i,j)
                    # Change value at the index by du
                    self.space[i][j] += du


    


