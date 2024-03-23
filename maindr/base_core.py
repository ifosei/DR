def base_core_func(Pl,Vsl,d,ol,Vsg,Ul,Ug):
    g = 32.2
    gc = 32.2

    #input parameters
    # Pl = float(input('Density of liquid phase: '))
    # Vsl = float(input('Liquid slip velocity: '))
    # d = float(input('diameter of pipe, ft: '))
    # ol = float(input('gas liquid interfacial tension: '))
    # Vsg = float(input('Gas slip velocity: '))
    # Ul = float(input('liquid viscosity: '))
    # μg = float(input('gas viscosity: '))

    #calculating the liquid viscosity number, Nl
    Nl = Ul * ((g / (Pl * (ol)**3))**(1/4))

    #calculating the liquid and gas velocity number, Nlv and Ngv
    Nlv = Vsl * ((Pl / (g * ol) ) **(1/4))
    Ngv = Vsg * ((Pl / (g * ol) ) **(1/4))

    #calculating pipe diameter number, Nd
    Nd = d * (((g * Pl) / (ol)))**(1/4)
    Ls = 50 + (36 * Nlv)
    Lm = 75 + (84 * (Nlv ** 0.75))
    print(d,g,Pl,ol)
    return {
        'Nl':Nl,
        'Nlv':Nlv,
        'Ngv':Ngv,
        'Nd':Nd,
        'Ls':Ls,
        'Lm':Lm,
    }