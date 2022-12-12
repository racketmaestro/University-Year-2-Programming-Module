from diffusion import Diffusion

def main():
    
    space1 = Diffusion(11,15,[1, 1, 1, 1], 11*[1], 11*[1], 15*[0], 15*[0])
    
    # print(space1.rows)
    # print(space1.cols)
    # print(space1.bc_settings)
    # print(space1.left_bc)
    # print(space1.right_bc)
    # print(space1.bottom_bc)
    # print(space1.top_bc)
    # print(space1.space)
    print(type(space1.space))
    print(type(space1.space[0][1]))

    
    space1.set_cell([4,6],[5,9],1)
    space1.print_space()
    print()
    space1.next_step(100)
    space1.print_space()
    print()
    

    # print(type(space1.rows))
    # print(type(space1.cols))
    # print(type(space1.bc_settings))
    # print(type(space1.bc_settings[0]))
    # print(type(space1.left_bc))
    # print(type(space1.left_bc[0]))
    # print(type(space1.right_bc))
    # print(type(space1.right_bc[0]))
    # print(type(space1.bottom_bc))
    # print(type(space1.bottom_bc[0]))
    # print(type(space1.top_bc))
    # print(type(space1.top_bc[0]))

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

    space1 = Diffusion(10,10,[2, 2, 2, 2], 10*[1], 10*[1], 10*[1], 10*[1])
    space1.set_cell([4,5],[4,5],1)
    space1.next_step(10060)
    space1.print_space()
    print()

if __name__ == '__main__':
    main()

