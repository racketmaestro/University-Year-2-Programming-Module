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
        

def main():
    
    space1 = Diffusion(11,15,[1, 1, 1, 1], 11*[1], 11*[1], 15*[0], 15*[0])
    
    print(space1.rows)
    print(space1.cols)
    print(space1.bc_settings)
    print(space1.left_bc)
    print(space1.right_bc)
    print(space1.bottom_bc)
    print(space1.top_bc)
    print(space1.space)
    print(type(space1.space))
    print(type(space1.space[0][1]))
    print()
    
    space1.set_cell([4,6],[5,9],1)
    space1.print_space()
    print()
    space1.next_step(100)
    space1.print_space()
    print()
    

    print(type(space1.rows))
    print(type(space1.cols))
    print(type(space1.bc_settings))
    print(type(space1.bc_settings[0]))
    print(type(space1.left_bc))
    print(type(space1.left_bc[0]))
    print(type(space1.right_bc))
    print(type(space1.right_bc[0]))
    print(type(space1.bottom_bc))
    print(type(space1.bottom_bc[0]))
    print(type(space1.top_bc))
    print(type(space1.top_bc[0]))

    print()
    space1 = Diffusion(11,15,[1, 1, 1, 1], 11*[0], 11*[0], 15*[0], 15*[0])
    space1.set_cell([4,6],[5,9],1)
    space1.set_cell([0,2],[0,2],1)
    space1.next_step(10000)
    space1.print_space()
    print()
    space1 = Diffusion(11,15,[2, 2, 1, 1], 11*[0], 11*[0], 15*[1], 15*[1])
    space1.set_cell([4,6],[5,9],1)
    space1.set_cell([0,2],[0,2],1)
    space1.next_step(10000)
    space1.print_space()
    print()

if __name__ == '__main__':
    main()




    


