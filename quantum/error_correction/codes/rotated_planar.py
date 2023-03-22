import math
from typing import List, Union


class RPlanarCode:
    """Rotated Planar surface code, defined as coordinates over:
        D: data qubits
        X: X-type stabilizer qubits
        Z: Z-type stabilizer qubits

    Example for dimension = 3
    (a.k.a. Surface-17 https://arxiv.org/pdf/1612.08208.pdf)
    
                    X0
        D0      D1      D2
    Z0      X1      Z1
        D3      D4      D5
            Z2      X2      Z3
        D6      D7      D8
            X3

    Example for dimension = 5
    
                    X0              X1
        D0      D1      D2      D3      D4
    Z0      X2      Z1      X3      Z2
        D5      D6      D7      D8      D9
            Z3      X4      Z4      X5      Z5
        D10     D11     D12     D13     D14
    Z6      X6      Z7      X7      Z8
        D15     D16     D17     D18     D19
            Z9      X8      Z10     X9      Z11
        D20     D21     D22     D23     D24
            X10             X11

    """

    def __init__(self, dimension: int) -> None:

        if dimension & 0 or dimension == 1:
            raise ValueError("Dimension must be an odd number greater than 1!")

        self._dimension = dimension
        self._num_stabilizer_qubits = int((dimension**2 - 1) / 2)
        self._name = f"D = {self._dimension} Rotated Planar Surface Code"

        self._parity_checks = {
            "x": [],
            "z": []
        }

        # Z-type parity checks
        p_check_weight_2 = (1 << self._dimension) + 1
        p_check_weight_4 = ((3 << self._dimension) + 3) << 1
        
        p_temp = 0
        for p in range(self._num_stabilizer_qubits):

            if p_temp % self._dimension == 0:
                self._parity_checks["z"].append(p_check_weight_2)
                if p_temp == 0:
                    p_check_weight_2 = \
                        p_check_weight_2 << (2 * self._dimension) - 1
                    p_temp += 1
                elif p_temp == self._dimension:
                    p_check_weight_2 = p_check_weight_2 << 1
                    p_check_weight_4 = p_check_weight_4 << 2
                    p_temp = 0
            else:
                self._parity_checks["z"].append(p_check_weight_4)
                p_check_weight_4 = p_check_weight_4 << 2
                p_temp += 1

        # X-type parity checks
        p_check_weight_2 = 6
        p_check_weight_4 = (3 << self._dimension) + 3
        
        p_temp = 0
        for p in range(self._num_stabilizer_qubits):

            if p_temp % self._dimension == 0:
                self._parity_checks["z"].append(p_check_weight_2)
                if p_temp == 0:
                    p_check_weight_2 = \
                        p_check_weight_2 << (2 * self._dimension) - 1
                    p_temp += 1
                elif p_temp == self._dimension:
                    p_check_weight_2 = p_check_weight_2 << 1
                    p_check_weight_4 = p_check_weight_4 << 2
                    p_temp = 0
            else:
                self._parity_checks["z"].append(p_check_weight_4)
                p_check_weight_4 = p_check_weight_4 << 2
                p_temp += 1

    # def apply_error(self, index: int, error_type: str="x"):

    #     if index > self._dimension**2 - 1:
    #         raise ValueError(f"Index {index} higher than number of data qubits!")

    #     if error_type not in self._error_data_qubits.keys():
    #         raise ValueError(
    #             f"Error type must be one of {list(self._error_data_qubits.keys())}"
    #         )

    #     # update the errored data qubits
    #     if index not in self._error_data_qubits[error_type]:
    #         self._error_data_qubits[error_type].append(index)
    #     else:
    #         self._error_data_qubits[error_type].remove(index)

    #     # update the active syndrome qubits
    #     syndrome_type = next(
    #         s for s in list(self._active_syndrome_qubits.keys()) if s != error_type
    #     )

    #     data_row, data_col = self._get_qubit_row_column(index, "d")

    # def _get_qubit_row_column(self, index: int, type: str="z") -> (int, int):
        
    #     if (type == "x" or type == "z") and \
    #         (index > self._num_stabilizer_qubits - 1):
    #         raise ValueError("Index greater than number of stabilizer qubits!")


    #     if type == "z":
    #         dim = math.ceil(self._dimension / 2)
    #     elif type == "x":
    #         dim = math.floor(self._dimension / 2)
    #     elif type == "d":
    #         dim = self._dimension

    #     else:
    #         raise ValueError("Invalid qubit type!")

    #     return math.floor(index / dim), index % dim

    def _convert_list_to_int(self, error_string: List[int]) -> int:
                num = 0
                for i in error_string:
                    num += (1 << i)
                return num

    def generate_syndrome(
        self, error_string: Union[int, List[int]], error_type: str="x"
    ) -> int:

        if isinstance(error_string, List):
            error_string = self._convert_list_to_int(error_string)

        syndrome_type = next(s for s in ["x", "z"] if s != error_type)

        syndrome = 0
        for i, parity_check in enumerate(self._parity_checks[syndrome_type]):
            res = 0
            par = parity_check & error_string
            while par:
                res ^= par & 1
                par >>= 1

            syndrome += res << i

        return syndrome 

    def draw(
        self,
        x_error_string: Union[int, List[int]]=0,
        z_error_string: Union[int, List[int]]=0
    ) -> None:
        """Method to print diagrammatic string representation of the code to
        the terminal.
        """
        
        x_syndrome = 0
        z_syndrome = 0
        if x_error_string:
            if isinstance(x_error_string, List):
                x_error_string = self._convert_list_to_int(x_error_string)
            z_syndrome = self.generate_syndrome(x_error_string, error_type="x")
        if z_error_string:
            if isinstance(z_error_string, List):
                z_error_string = self._convert_list_to_int(z_error_string)
            x_syndrome = self.generate_syndrome(z_error_string, error_type="z")

        x = 0
        z = 0
        str_code = "{:>16}".format("")

        # first X qubits
        for i in range(math.floor(self._dimension / 2)):
            str_code += "X" + "{:<15}".format(i)
            x += 1
        str_code += "\n" + "{:>4}".format("")

        # D, Z and remaining X qubits
        even_row = True  # toggle flag between rows
        for d in range(self._dimension**2):
            if d > 0 and d % self._dimension == 0:
                str_code += "\n"
                if z < self._num_stabilizer_qubits:
                    if not even_row:
                            str_code += "{:>8}".format("")

                    for i in range(math.ceil(self._dimension / 2)):

                        if (1 << z) & z_syndrome:
                            str_code += "\033[93m"
                        str_code += "Z"  + "{:<7}".format(z) + "\033[0m"
                        z += 1

                        if i != math.ceil(self._dimension / 2) - 1:

                            if (1 << x) & x_syndrome:
                                str_code += "\033[92m"

                            str_code += "X"  + "{:<7}".format(x) + "\033[0m"
                            x += 1

                    str_code += "\n" + "{:>4}".format("")
                    even_row = not even_row

            has_x_error = (1 << d) & x_error_string
            has_z_error = (1 << d) & z_error_string

            if has_x_error and has_z_error:
                str_code += "\033[95m"
            elif has_x_error:
                str_code += "\033[91m"
            elif has_z_error:
                str_code += "\033[94m"

            str_code += "D" + "{:<7}".format(d) + "\033[0m"
        str_code += "\n" + "{:>8}".format("")

        # last X qubits
        for i in range(x, self._num_stabilizer_qubits):
            str_code += "X" + "{:<15}".format(i)
        str_code += "\n"

        
        print()
        print(str_code)
        print()
        print(self._name)
        print()
        print("\033[91mX errors")
        print("\033[94mZ errors")
        print("\033[95mXZ errors")
        print("\033[92mX syndrome")
        print("\033[93mZ syndrome\033[0m")
        print()

if __name__ == "__main__":

    code = RPlanarCode(7)
    code.draw(x_error_string=1090519040, z_error_string=256)
    code.draw(x_error_string=[19, 30, 36], z_error_string=[8])