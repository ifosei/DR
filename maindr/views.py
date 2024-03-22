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
            request.session['d2']['flow_pattern'] = 1
            request.session['d2']['regime'] = 'Bubble flow regime'
            return redirect(fp1)
            
        elif (L1 + L2) * (d2['Nlv']) <= d2['Ngv'] <= d2['Ls']:
            request.session['d2']['flow_pattern'] = 2
            request.session['d2']['regime'] = 'Slug flow regime'
            return redirect(fp2)
            
        elif (d2['Ngv'] > d2['Lm']):
            request.session['d2']['flow_pattern'] = 3
            request.session['d2']['regime'] = 'Mist flow regime'
            S = 0
            Hl3 = (1 / (1 + (d1['Vsg'] / d2['Vsl'])))
            request.session['d2']['S'] = 0
            request.session['d2']['Hl3'] = Hl3
            
            
        elif d2['Ls'] < d2['Ngv'] < d2['Lm']:
            request.session['d2']['flow_pattern'] = 4
            request.session['d2']['regime'] = 'Transition flow regime'
    return render(request,'L_graph.html')

def fp1(request):
    if 'fp1sub' in request.POST:
        d2 = request.session['d2']
        F1 = float(request.POST.get('F1'))
        F2 = float(request.POST('F2'))
        F3 = float(request.POST('F3'))
        F4 = float(request.POST('F4'))

        F3p = F3 - (F4/d2['Nd'])
        S = F1 + (F2 * d2['Nlv']) + F3p * (d2['Ngv'] / (1 + d2['Nlv'] ))

        request.session['d2']['S'] = S
        # request.session['d2']['F2'] = F2
        # request.session['d2']['F3'] = F3
        # request.session['d2']['F4'] = F4

    return render(request,'fp1.html')

def fp2(request):
    d2 = request.session['d2']
    if 'fp1sub' in request.POST:
        F5 = float(request.POST.get('F5'))
        F6 = float(request.POST('F6'))
        F7 = float(request.POST('F7'))
        
        F6p = (0.029 * d2['Nd']) + F6 
        S = (1 + F5) * (((d2['Ngv'] ** 0.982) + F6p) / (1 + (F7 * d2['Nlv']))**2)
        request.session['d2']['S'] = S


    request.session['d2']['S'] = S
    return render(request,'fp2.html')

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
    Vs = (d2['S'] / (d2['ol'] / (d2['ol'] * g)) ** 0.25)
          
    #determining the liquid holdup, Hl 
    Hls = ((Vs - d1['Vsg'] - d1['Vsl']) + ((((Vs - d1['Vsg'] - d1['Vsl'])**2 ) + (4 * Vs * d['Vsl'] )) ** (1/2))) / (2 * Vs)

    NRe = (d2['Pl'] * d2['Vsl'] * d2['d']) / (d2['Ul'])
    if 'getdp' in request.POST:
        f1 = float(request.POST.get('f1'))
        R = (d1['Vsg'] /d2[' Vsl'])
        f3 = 1 + ( f1 * ((R / 50) ** (1/2))) 
        f2 = (f1 * R * (d2['Nd'] ** 2/3))
        Fm = (f1 * (f2 / f3))
            
        #calculating friction gradient according to flow regime, for bubble and slug,dp_dzs
        Vm = float(request.POST.get('Vm'))
        dp_dzs = (Fm * d1['Pl'] * d1['Vsl'] * Vm) / (2 * gc * d1['d'])

        request.session['d2']['dp'] = dp_dzs

    return render(request,'dpf1f2.html')

    
        

            