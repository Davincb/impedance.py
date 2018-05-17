from .fitting import circuit_fit, computeCircuit
import numpy as np

class BaseCircuit:
    """ A base class for all circuits

    """
    def __init__(self, initial_guess=None):
        """
        Constructor for the Randles' circuit class


        """
        if initial_guess is not None:
            for i in initial_guess:
                assert type(i) == type(0.5) or type(i) == type(1) or \
                type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
                (f'value {i} in initial_guess is not a number')
        self.initial_guess = initial_guess
        self.parameters_ = None

    def fit(self, frequencies, impedance):
        """
        Fit the circuit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        impedance: numpy array of dtype 'complex128'
            Impedance values to fit

        Returns
        -------
        self: returns an instance of self

        """
        # tests
        import numpy as np
        assert type(frequencies) == type([1.5]) or type(frequencies) == type(np.array([1.5]))
        assert len(frequencies) == len(impedance)
        for i in frequencies:
            assert type(i) == type(0.5) or type(i) == type(1) or \
            type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
            (f'value {i} in initial_guess is not a number')
        # check_valid_impedance()
        if self.initial_guess is not None:
            self.parameters_, _ = circuit_fit(frequencies, impedance, self.circuit, self.initial_guess)
        else:
            # TODO auto calc guess
            raise ValueError('no initial guess supplied')

        return self

    def _is_fit(self):
        if self.parameters_ is not None:
            return True
        else:
            return False

    def predict(self, frequencies):
        """ Predict impedance using a fit model

        Parameters
        ----------
        frequencies: numpy array
            Frequencies

        Returns
        -------
        impedance: numpy array of dtype 'complex128'
            Predicted impedance

        """

        if self._is_fit():
            # print('Output! {}'.format(self.parameters_))

            return computeCircuit(self.circuit,
                                   self.parameters_.tolist(),
                                   frequencies.tolist())

        else:
            raise ValueError("The model hasn't been fit yet")

class Randles(BaseCircuit):
    def __init__(self, initial_guess=None, CPE=False):
        """
        Constructor for the Randles' circuit class


        """
        # write some asserts to enforce typing
        if initial_guess is not None:
            for i in initial_guess:
                assert type(i) == type(0.5) or type(i) == type(1) or \
                type(i) == type(np.array([1])[0]) or type(i) == type(np.array([1.5])[0]), \
                (f'value {i} in initial_guess is not a number')
        
        if CPE:
            self.circuit = 'R_0-p(R_1,E_1/E_2)-W_1/W_2'
        else:
            self.circuit = 'R_0-p(R_1,C_1)-W_1/W_2'
        circuit_length = 5
        assert len(initial_guess) == circuit_length, 'Initial guess length needs to be equal to {circuit_length}'
        self.initial_guess = initial_guess
        self.parameters_ = None

    def __repr__(self):
        """
        Defines the pretty printing of the circuit

        """
        return "Randles circuit (initial_guess={}, circuit={})".format(self.initial_guess, self.circuit)
