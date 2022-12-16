class Diffusion:
    """
    The Diffusion class represents a 2D space diffusion simulation. An initial state value can be assigned to a subset of the 2D space.
    The class can be used to compute the change of state for the space after a given number of time steps.

    Methods:
        - __init__: Initializes the Diffusion class with default or user-specified values for number of rows and columns,
        boundary conditions settings for each border, and boundary conditions initial values for each index at the 4 borders.
        - set_cell: Sets the state value for a range of cells in the 2D space.
        - print_space: Prints the current state of the 2D space.
        - du_x: Computes the derivative of the state with respect to time, due to adjacent horizontal cells, at a given index.
        - du_y: Computes the derivative of the state with respect to time, due to adjacent vertical cells, at a given index.
        - du: Computes the net derivative of the state with respect to time.
        
    Attributes:
        - rows (int): The number of rows in the 2D space.
        - cols (int): The number of columns in the 2D space.
        - bc_settings (list): A list of boundary condition settings for each of the 4 borders.
        - left_bc (list): A list of boundary condition values for the left border.
        - right_bc (list): A list of boundary condition values for the right border.
        - top_bc (list): A list of boundary condition values for the top border.
        - bottom_bc (list): A list of boundary condition values for the bottom border.
        - space (list): A 2D array representing the state of each particle.
    """

    def __init__(self, rows= None, cols= None, bc_settings= None, left_bc= None, right_bc= None, top_bc= None, bottom_bc= None):
        # set default values if None is passed into positional arguments
        self.rows  = int(rows) if rows else 10
        self.cols = int(cols) if cols else 10
        self.bc_settings = list(map(int,bc_settings)) if bc_settings else [1,1,1,1]   
        self.left_bc = [float(i) for i in left_bc] if left_bc else [0.0] * self.rows
        self.right_bc = [float(i) for i in right_bc] if right_bc else [0.0] * self.rows
        self.top_bc = [float(i) for i in top_bc] if top_bc else [0.0] * self.cols
        self.bottom_bc = [float(i) for i in bottom_bc] if bottom_bc else [0.0] * self.cols

        # initialise 2D array of space with default values of 0.0
        self.space = [[0.0 for i in range(self.cols)] for j in range(self.rows)]
        
    def set_cell(self, row_range, column_range, state):
        '''iterate over the row and column indexes and set to state'''
        for row in range(row_range[0],row_range[1]+1):
            for col in range(column_range[0],column_range[1]+1):
                
                self.space[row][col] = float(state)

    def print_space(self):
        for i in range(self.rows):
            for j in range(self.cols):
                print(f'{self.space[i][j]:1.4f}',end=' ')
            print()
            
    
    def du_x(self, row_idx, col_idx):
        '''return delta x at the given input index'''
        
        if col_idx < self.cols-1 and col_idx > 0:
        # index is not at left or right border    
            du_x = self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] + self.space[row_idx][col_idx-1]
            
        elif col_idx == self.cols-1:
        # index given is at the right border
            bc_setting_right = self.bc_settings[1]
            if bc_setting_right == 1:
            # Direchlet condition
                du_x = self.right_bc[row_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx][col_idx - 1]
            else:
            # Neumann condition
                du_x = 2*self.space[row_idx][col_idx-1] - 2*self.space[row_idx][col_idx] + 2*self.right_bc[row_idx]
                
        elif col_idx == 0:
        # index given is at the left border
            bc_setting_left = self.bc_settings[0]
            if bc_setting_left == 1:
            # Direchlet condition
                du_x = self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] + self.left_bc[row_idx]
            else:
            # Neumann condition
                du_x = 2*self.space[row_idx][col_idx + 1] - 2*self.space[row_idx][col_idx] - 2*self.left_bc[row_idx]
                
        return du_x
        
    def du_y(self, row_idx, col_idx):
        '''return delta y at the given input index'''
        
        if row_idx < self.rows-1 and row_idx > 0:
        # index is not at top or bottom border
            du_y = self.space[row_idx +1][col_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx-1][col_idx]
        
        elif row_idx == self.rows-1:
        # index given is at bottom border
            bc_setting_bottom = self.bc_settings[3]
            if bc_setting_bottom == 1:
            # Direchlet condition
                du_y = self.bottom_bc[col_idx] - 2*self.space[row_idx][col_idx] + self.space[row_idx-1][col_idx]
            else:
            # Neumann condition
                du_y = 2*self.space[row_idx-1][col_idx] - 2*self.space[row_idx][col_idx] + 2*self.bottom_bc[col_idx]
        
        elif row_idx == 0:
        # index given is at top border
            bc_setting_top = self.bc_settings[2]
            if bc_setting_top == 1:
            # Direchlet condition
                du_y = self.space[row_idx+1][col_idx] - 2*self.space[row_idx][col_idx] + self.top_bc[col_idx]
            else:
            # Neumann condition
                du_y = 2*self.space[row_idx+1][col_idx] - 2*self.space[row_idx][col_idx] - 2*self.top_bc[col_idx]
        
        return du_y

    
    def du(self,row_idx,col_idx):
        '''returns final delta u at the index passed'''
        delta_x = self.du_x(row_idx,col_idx)
        delta_y = self.du_y(row_idx,col_idx)
        du = 0.0001*(delta_x + delta_y)
        return du


    def next_step(self, n_steps):
        '''modify the state of space given a number of time steps'''
        du_array = [[0.0 for i in range(self.cols)] for j in range(self.rows)]
        n_steps = int(n_steps)
        # iterate for n_steps times, for every single particle within space
        for n in range(n_steps):
            for i in range(0,self.rows):
                for j in range(0,self.cols):
                    du =  self.du(i,j)
                    # Change value of du_array at the index by du
                    du_array[i][j] = du
            # now change each self.space particle by the corresponding du amount 
            for p in range(self.rows):
                for q in range(self.cols):
                    self.space[p][q] += du_array[p][q]
