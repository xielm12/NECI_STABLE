#!/usr/bin/python
'''greens_analysis.py [options] file

Calculate and output a spectral function from a given set of eigenvalues and
corresponding spectral weights. These should be output from NECI from a KP-FCIQMC
calculation.'''

import sys
import optparse
import pandas as pd
import math

def extract_data(data_files, cutoff):
    '''Extract the eigenvalues and the spectral weights from the data file provided.'''

    norm_str = 'Norm of unperturbed initial wave function'
    start_str = 'Eigenvalues and overlaps when keeping '+str(cutoff)

    for data_file in data_files:
        f = open(data_file)
        have_data = False
        have_norm = False
        pairs = []
        for line in f:
            if not line.strip(): # If an empty line.
                have_data = False
                have_norm = False
            if have_data:
                values = line.split()
                pairs.append( [float(values[0]), float(values[1])] )
            if have_norm:
                unperturbed_norm = float(line.strip())
            if start_str in line:
                have_data = True
            if norm_str in line:
                have_norm = True
                
    return pairs, unperturbed_norm

def calculate_spectral_function(pairs, norm, minval, maxval, delta, broadening, ref_energy, inc_ground):

    nomega = int(math.ceil((maxval-minval)/delta))+1

    # Do we include the ground state eigenvector?
    if inc_ground:
        min_eigv = 0
    else:
        min_eigv = 1

    omega_list = []
    spectral_list = []
    for i in range(nomega):
        omega = minval + i*delta
        spec = 0.0
        for [eigv, unnormalised_weight] in pairs[min_eigv:]:
            weight = (unnormalised_weight/norm)**2
            spec += (broadening*weight)/(math.pi*(broadening**2 + (omega+ref_energy-eigv)**2))
        omega_list.append(omega)
        spectral_list.append(spec)

    results_dict = {'Omega' : pd.Series(omega_list), 
                    'Spectrum' : pd.Series(spectral_list)}

    results = pd.DataFrame(results_dict)

    return results

def parse_options(args):

    parser = optparse.OptionParser(usage = __doc__)
    parser.add_option('-g', '--inc-ground', action='store_true', dest='inc_ground',
                      default=False, help='Include the ground state in the spectrum.')
    parser.add_option('-m', '--min-plot', dest='minval', type='float', default=0.0,
                      help='The minimum omega to output results for.')
    parser.add_option('-n', '--max-plot', dest='maxval', type='float', default=4.0,
                      help='The maximum omega to output results for.')
    parser.add_option('-d', '--delta-omega', dest='delta', type='float', default=0.01,
                      help='The resolution in omega to plot.')
    parser.add_option('-b', '--broadening', dest='broadening', type= 'float',
                      default=0.1, help='The broadening factor to be used.')
    parser.add_option('-l', '--lowdin-cutoff', dest='cutoff', type='int', default=5,
                      help='The number of eigenvectors which were kept in the Lowdin '
                      'orthogonalisation procedure.')
    parser.add_option('-r', '--ref-energy', dest='ref_energy', type='float', 
                      default=0.0, help='The ground-state energy of the unperturbed '
                      'system.')
    (options, filenames) = parser.parse_args(args)
    
    if len(filenames) == 0:
        parser.print_help()
        sys.exit(1)

    return (options, filenames)

if __name__ == '__main__':
    (options, data_files) = parse_options(sys.argv[1:])
    pairs, norm = extract_data(data_files, options.cutoff)
    results = calculate_spectral_function(pairs, norm, options.minval, options.maxval,
                                         options.delta, options.broadening,
                                         options.ref_energy, options.inc_ground)

    print results.to_string(index=False)
