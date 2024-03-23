from django.shortcuts import render, redirect
from .base_core import base_core_func

# Create your views here.

def base(request):

    if 'basecalcsub' in request.POST:
        Pl = float(request.POST.get('Pl'))
        Vsl = float(request.POST.get('Vsl'))
        d = float(request.POST.get('d'))
        ol = float(request.POST.get('ol'))
        Vsg = float(request.POST.get('Vsg'))
        Ul = float(request.POST.get('Ul'))
        Ug = float(request.POST.get('Ug'))

        base_core_dataset = base_core_func(Pl,Vsl,Vsg,d,ol,Ul,Ug)
        
        basecalcdata = {
            'Pl':Pl,
            'Vsl':Vsl,
            'd':d,
            'ol':ol,
            'Vsg':Vsg,
            'Ul':Ul,
            'Ug':Ug,
        }
        request.session['d1'] = basecalcdata
        request.session['d2'] = base_core_dataset

        return redirect(l_values)

    return render(request,'base.html')

def l_values(request):
    d1 = request.session['d1']
    d2 = request.session['d2']

    if 'lcalcsub' in request.POST:
        L1 = float(request.POST.get('L1'))
        L2 = float(request.POST.get('L2'))
    
        if 0 <= d2['Ngv'] <= (L1 + L2) * d2['Nlv']:
            request.session['flow_pattern'] = 1
            request.session['regime'] = 'Bubble flow regime'
            return redirect(fp1)
            
        elif (L1 + L2) * (d2['Nlv']) <= d2['Ngv'] <= d2['Ls']:
            request.session['flow_pattern'] = 2
            request.session['regime'] = 'Slug flow regime'
            return redirect(fp2)
            
        elif (d2['Ngv'] > d2['Lm']):
            request.session['flow_pattern'] = 3
            request.session['regime'] = 'Mist flow regime'
            S = 0
            Hl3 = (1 / (1 + (d1['Vsg'] / d1['Vsl'])))
            request.session['S'] = 0
            request.session['Hl3'] = Hl3
            return redirect(dpf3)
            
            
        elif d2['Ls'] < d2['Ngv'] < d2['Lm']:
            request.session['flow_pattern'] = 4
            request.session['regime'] = 'Transition flow regime'
            return redirect(dpf1f2)
    context={
        'Nd':d2['Nd'],
        }
    return render(request,'L_graph.html',context)

def fp1(request):
    d2 = request.session['d2']
    if 'fp1sub' in request.POST:

        F1 = float(request.POST.get('F1'))
        F2 = float(request.POST.get('F2'))
        F3 = float(request.POST.get('F3'))
        F4 = float(request.POST.get('F4'))

        F3p = F3 - (F4/d2['Nd'])
        S = F1 + (F2 * d2['Nlv']) + F3p * (d2['Ngv'] / (1 + d2['Nlv'] ))
        print('FDSDSAFSADFSADFDSAF')
        request.session['S'] = S
        # request.session['d2']['F2'] = F2
        # request.session['d2']['F3'] = F3
        # request.session['d2']['F4'] = F4
        return redirect(dpf1f2)
    context={
        'Nl':d2['Nl'],
    }
    return render(request,'fp1.html',context)

def fp2(request):
    d2 = request.session['d2']
    if 'fp2sub' in request.POST:
        F5 = float(request.POST.get('F5'))
        F6 = float(request.POST.get('F6'))
        F7 = float(request.POST.get('F7'))
        
        F6p = (0.029 * d2['Nd']) + F6 
        S = (1 + F5) * (((d2['Ngv'] ** 0.982) + F6p) / (1 + (F7 * d2['Nlv']))**2)



        request.session['S'] = S
        
        print(request.session['d2'])
        return redirect(dpf1f2)
    context={
        'Nl':d2['Nl'],
    }
        
    return render(request,'fp2.html',context)

# def fp3(request):
#     d2 = request.session['d2']
#     if 'fp1sub' in request.POST:
#         F5 = float(request.POST.get('F1'))
#         F6 = float(request.POST('F2'))
#         F7 = float(request.POST('F3'))
        
#         F6p = (0.029 * d2['Nd']) + F6 
#         S = (1 + F5) * (((d2['Ngv'] ** 0.982) + F6p) / (1 + (F7 * d2['Nlv']))**2)
#         request.session['d2']['S'] = S

#     return render(request,'fp3.html')

def dpf1f2(request):
    g = 32.2
    gc = 32.2
    d1 = request.session['d1']
    d2 = request.session['d2']
    #determining slip velocity for bubble or slug flow regime, Vs
    print(d2)
    Vs = (request.session['S'] / (d1['ol'] / (d1['ol'] * g)) ** 0.25)
          
    #determining the liquid holdup, Hl 
    Hls = ((Vs - d1['Vsg'] - d1['Vsl']) + ((((Vs - d1['Vsg'] - d1['Vsl'])**2 ) + (4 * Vs * d1['Vsl'] )) ** (1/2))) / (2 * Vs)

    NRe = (d1['Pl'] * d1['Vsl'] * d1['d']) / (d1['Ul'])
    if 'getDp' in request.POST:
        f1 = float(request.POST.get('f1'))
        R = (d1['Vsg'] / d1['Vsl'])
        f3 = 1 + ( f1 * ((R / 50) ** (1/2))) 
        f2 = (f1 * R * (d2['Nd'] ** 2/3))
        Fm = (f1 * (f2 / f3))
            
        #calculating friction gradient according to flow regime, for bubble and slug,dp_dzs
        Vm = float(request.POST.get('Vm'))
        dp_dzs = (Fm * d1['Pl'] * d1['Vsl'] * Vm) / (2 * gc * d1['d'])

        if request.session['flow_pattern'] == 4:
            request.session['dp_dzs'] = dp_dzs
            return redirect(dpf3)
        else:
            request.session['dp'] = dp_dzs
            return redirect(results)
    context={
        'NRe':NRe,
    }
    return render(request,'dpf1f2.html',context)

def dpf3(request):
    g = 32.2
    gc = 32.2
    if 'dpf3calc' in request.POST:
        d1 = request.session['d1']
        d2 = request.session['d2']
        Pg = float(request.POST.get('Pg'))
        rn = float(request.POST.get('rn'))
        Vsg1 = float(request.POST.get('Vsg1'))
        #correcting the gas density,ρg1                     
        Pg1 = (Pg * d2['Ngv']) / (d2['Lm'])
        #determining the liquid reynolds number, NRe                     
        NRe = (Pg1 * d1['Vsg'] * d1['d']) / (d1['Ug'])
        #determining the Weber number, Nwe
        Nwe = (Pg1 * ((d1['Vsg'])**2) * rn) / (d1['Ul'])
        #determining the dimensionless number, Nμ
        Nμ = (d1['Ul']**2) / (d1['Pl'] * d1['ol'] * rn)

        if Nwe * Nμ <= 0.005:
           rn_d = (0.0749 * d1['ol']) / (Pg * (Vsg1**2) * d1['d'])
        elif Nwe * Nμ > 0.005:
            rn_d = (((0.3713 * d1['ol']) / (Pg * (Vsg1**2) * d1['d'])) * (Nwe * Nμ)**0.302)
        import math
        f_f = ((1 / (4 * math.log10(0.27*(rn_d)))**2) + (0.067 * (rn_d)**1.73) ) *4 
        print('The friction factor for mist flow regime is ',f_f)

        #calculating friction gradient according to flow regime,for mist,dp_dzm
        dp_dzm = (f_f * Pg * Vsg1 ** 2) / (2 * gc * d1['d'])
        
        if request.session['flow_pattern'] == 4:
            request.session['dp_dzm'] = dp_dzm
            return redirect(dpf4)
        else:
            request.session['dp'] = dp_dzm
            return redirect('results')

    
    return render(request,'fp3.html')


def dpf4(request):
    d1 = request.session['d1']
    d2 = request.session['d2']
    dp_dzs = request.session['dp_dzs']
    dp_dzm = request.session['dp_dzm']
    A = (d2['Lm'] - d2['Ngv']) / (d2['Lm'] - d2['Ls'])
    B = (d2['Ngv'] - d2['Ls']) / (d2['Lm'] - d2['Ls'])
    dp_dzt = (A * dp_dzs) + (B * dp_dzm)

    request.session['dp'] = dp_dzt
    return redirect(results)


        

def results(request):
    dp = request.session['dp'] 
    regime = request.session['regime']
    context={
        'Dp':dp,
        'regime':regime,
    }
    return render(request,'results.html',context)