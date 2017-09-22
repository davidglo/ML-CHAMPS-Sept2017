import numpy as np
from numpy import linalg as LA
from scipy.special import factorial


def loadData(fileName):
    """
    This function takes a .csv file generated after processing the original CSV files with the package PANDAS.
    The data is arranged with first the geometries in a 'clean datases' arrangement. This means that the headers tell
    the atom label for each coordinate. For example, for a molecule with 3 hydrogens, the first two lines of the csv
    file for the geometries look like:

    ``H1x, H1y, H1z, H2x, H2y, H2z, H3x, H3y, H3z
    0,1.350508,0.7790238,0.6630868,1.825709,1.257877,-0.1891705,1.848891,1.089646``

    Then there are the partial charges and then 2 values of the energies (all in similar format to the geometries).

    **Note**: This is specific to the CH4CN system!

    :fileName: .csv file (string)

    :return:
    :matrixX: a list of lists with characters and floats.
    :matrixY: a numpy array of energy differences (floats) of size (n_samples,)
    :matrixQ: a list of numpy arrays of the partial charges -  size (n_samples, n_atoms)
    """

    if fileName[-4:] != ".csv":
        raise ValueError("Error: the file extension is not .csv")

    inputFile = open(fileName, 'r')
    isFirstLine = True

    # Lists that will contain the data
    matrixX = []
    matrixY = []
    matrixQ = []

    # Reading the file
    for line in inputFile:
        if isFirstLine:
            line = next(inputFile)
            isFirstLine = False

        line = line.replace("\n", "")
        listLine = line.split(",")

        geom = extractGeom(listLine)
        eneDiff = extractEneDiff(listLine)
        partQ = extractQ(listLine)

        matrixX.append(geom)
        matrixY.append(eneDiff)
        matrixQ.append(partQ)

    matrixY = np.asarray(matrixY)

    return matrixX, matrixY

def extractGeom(lineList):
    """
    Function used by loadPd_q to extract the geometries.

    :lineList: line with geometries in clean format, partial charges and energies
    :return: list of geometry in format [['H',-0.5,0.0,0.0,'H',0.5,0.0,0.0], ['H',-0.3,0.0,0.0,'H',0.3,0.0,0.0]...
    """
    geomPart = lineList[1:22]
    atomLab = ["C","H","H","H","H","C","N"]
    finalGeom = []

    for i in range(len(atomLab)):
        finalGeom.append(atomLab[i])
        for j in range(3):
            finalGeom.append(float(geomPart[3*i+j]))

    return finalGeom

def extractEneDiff(lineList):
    """
    This function is used by loadPd_q  to extract the energy from a line of the clean data set.

    :param lineList: line with geometries in clean format, partial charges and energies
    :return: energy difference (float)
    """
    enePart = lineList[-2:]
    eneDiff = float(enePart[1]) - float(enePart[0])
    return eneDiff

def extractQ(lineList):
    """
    This function is used by loadPd_q to extract the partial charges from a line of the clean data set.

    :lineList: line with geometries in clean format, partial charges and energies
    :return: numpy array of partial charges of size (n_atoms)
    """
    qPart = lineList[22:-2]
    for i in range(len(qPart)):
        qPart[i] = float(qPart[i])

    qPart = np.asarray(qPart)
    return qPart



def loadX(fileX):
    """
    This function takes a .csv file that contains on each line a different configuration of the system in the format
        "C,0.1,0.1,0.1,H,0.2,0.2,0.2..." and returns a list of lists with the configurations of the system.
        
        The following functions generate .csv files in the correct format:
        
        1. XMLtoCSV
        2. XYZtoCSSV
        3. MolproToCSV
        
        The function returns a list of lists where each element is a different configuration for a molecule. For example,
        for a sample with 3 hydrogen atoms the matrix returned will be:
        ``[['H',-0.5,0.0,0.0,'H',0.5,0.0,0.0], ['H',-0.3,0.0,0.0,'H',0.3,0.0,0.0], ['H',-0.7,0.0,0.0,'H',0.7,0.0,0.0]]``
        
        :fileX: The .csv file containing the geometries of the system (string)
        :return: a list of lists with characters and floats.
    """
    
    if fileX[-4:] != ".csv":
        raise  ValueError("Error: the file extension is not .csv")

    inputFile = open(fileX, 'r')

    # Creating an empty matrix of the right size
    matrixX = []
    
    for line in inputFile:
        
        line = line.replace(",\n","")
        listLine = line.split(",")
        
        # converting the numbers to float
        for i in range(0,len(listLine)-1,4):
            for j in range(3):
                listLine[i+j+1] = float(listLine[i+j+1])
        matrixX.append(listLine)
    
    inputFile.close()
    return matrixX

def loadY(fileY):
    """
        This function takes a .csv file containing the energies of a system and returns an array with the energies contained
        in the file.
        
        :fileY: the .csv file containing the energies of the system (string)
        :return: numpy array of shape (n_samples, 1)
    """
    
    # Checking that the input file has the correct .csv extension
    if fileY[-4:] != ".csv":
        raise ValueError("Error: the file extension is not .csv")
    
    inputFile = open(fileY, 'r')

    y_list = []
    for line in inputFile:
        y_list.append(float(line))

    matrixY = np.asarray(y_list).reshape((len(y_list), 1))
    
    inputFile.close()
    return matrixY


class CoulombMatrix():
    """This class contains the functions required to generate the following variations of  Coulomb matrices (with nuclear charges) for M configurations of N atoms:

    1. Standard *unsorted* and *unrandomised* matrix
    2. The eigen spectrum of the Coulomb matrix: vector containing the eigenvalues in descending order
    3. The sorted Coulomb matrix
    4. The randomly sorted Coulomb matrix
    5. The trimmed Coulomb matrix: this is the triangular part of the standard Coulomb matrix
    6. The partially randomised Coulomb matrix

    The explanation for how the matrices 1 to 4 are constructed can be found in this `paper <http://pubs.acs.org/doi/abs/10.1021/ct400195d/>`_.

    When it is initialised, the raw data of each configuration with atom labels and their xyz coordinates is passed.

    :matrixX: list of lists, where each of the inner lists represents a sample configuration. An example is shown below: [ [ 'C', 0.1, 0.3, 0.5, 'H', 0.0, 0.5 1.0, 'H', 0.0, -0.5, -1.0, ....], [...], ... ].

    """

    def __init__(self, matrixX):

        self.rawX = matrixX
        self.Z = {
                    'C': 6.0,
                    'H': 1.0,
                    'N': 7.0
                 }

        self.n_atoms = int(len(self.rawX[0])/4)
        self.n_samples = len(self.rawX)


        self.coulMatrix = np.zeros((self.n_samples, self.n_atoms**2))
        self.__generateCM()

    def getCM(self):
        """
        This function returns the standard Coulomb matrix. Each line is the flattened matrix for each sample.

        :return: numpy array of shape (n_samples, n_atoms**2)
        """
        return self.coulMatrix

    def __generateCM(self):
        """
        This function generates the standard Coulomb Matrix descriptor as a numpy array of size (n_samples, n_atoms^2).
        Each line is the matrix for one sample.
        """

        # This is a coulomb matrix for one particular sample in the dataset
        indivCM = np.zeros((self.n_atoms, self.n_atoms))
        sampleCount = 0

        for item in self.rawX:

            labels = ""  # This is a string containing all the atom labels
            coord = []  # This is a list of tuples with the coordinates of all the atoms in a configuration

            # This gathers the atom labels and the coordinates for one sample
            for i in range(0, len(item), 4):
                labels += item[i]
                coord.append(np.array([float(item[i + 1]), float(item[i + 2]), float(item[i + 3])]))

            # Diagonal elements
            for i in range(self.n_atoms):
                indivCM[i, i] = 0.5 * self.Z[labels[i]] ** 2.4

            # Off-diagonal elements
            for i in range(self.n_atoms - 1):
                for j in range(i + 1, self.n_atoms):
                    distanceVec = coord[i] - coord[j]
                    distance = np.sqrt(np.dot(distanceVec, distanceVec))
                    indivCM[i, j] = self.Z[labels[i]] * self.Z[labels[j]] / distance
                    indivCM[j, i] = indivCM[i, j]

            # The coulomb matrix for each sample is flattened and added to the total coulomb matrix
            self.coulMatrix[sampleCount, :] = indivCM.flatten()
            sampleCount += 1

    def generateES(self):
        """
        This function calculates the eigen spectrum from the standard Coulomb matrix.

        :return: numpy array of shape (n_samples, n_atoms)
        """

        self.coulES = np.zeros((self.n_samples, self.n_atoms))

        for i in range(self.n_samples):
            tempCM = np.reshape(self.coulMatrix[i, :], (self.n_atoms, self.n_atoms))
            tempES, tempDiag = LA.eig(tempCM)
            self.coulES[i,:] = tempES

        return self.coulES

    def generateSCM(self):
        """
        This function calculates the sorted Coulomb matrix starting from the standard matrix. It then returns the
        triangular part of the matrix.

        :return: numpy array of size (N_samples, n_atoms*(n_atoms+1)/2)
        """

        coulS = np.zeros((self.n_samples, int(self.n_atoms * (self.n_atoms+1) * 0.5)))

        for i in range(self.n_samples):
            tempCM = np.reshape(self.coulMatrix[i, :], (self.n_atoms, self.n_atoms))

            # Sorting the Coulomb matrix rows and columns in descending order of the norm of each row.
            rowNorms = np.zeros(self.n_atoms)
            for j in range(self.n_atoms):
                rowNorms[j] = LA.norm(tempCM[j, :])

            permutations = np.argsort(rowNorms)
            permutations = permutations[::-1]

            tempCM = tempCM[permutations, :]
            tempCM = tempCM[:, permutations]
            coulS[i, :] = self.trimAndFlat(tempCM)

        return coulS

    def generateRSCM(self, y_data, numRep=5):
        """
        This function creates the randomy sorted Coulomb matrix starting from the standard Coulomb matrix and it
        transforms the y part of the data so that there are numRep copies of each energy.

        :y_data: a numpy array of energy values of shape (N_samples,)
        :numRep: number of randomly sorted matrices to be generated per sample - int
        :return: the randomly sorted CM - numpy array of size (N_samples*numRep, n_atoms^2) and a numpy array of energy values of size (N_samples*numRep,)
        """

        # Checking reasonable numRep value
        if(isinstance(numRep, int) == False):
            raise ValueError("Error: you gave a non-integer value for the number of RSCM that you want to generate.")
        elif(numRep < 1):
            raise ValueError("Error: you cannot generate less than 1 RSCM per sample. Enter an integer value > 1.")

        counter = 0
        coulRS = np.zeros((self.n_samples*numRep, int(self.n_atoms * (self.n_atoms+1) * 0.5)))
        y_bigdata = np.zeros((self.n_samples*numRep,))

        for i in range(self.n_samples):
            tempCM = np.reshape(self.coulMatrix[i, :], (self.n_atoms, self.n_atoms))

            # Calculating the norm vector for the coulomb matrix
            rowNorms = np.zeros(self.n_atoms)

            for j in range(self.n_atoms):
                rowNorms[j] = LA.norm(tempCM[j, :])

            for k in range(numRep):
                # Generating random vectors and adding to the norm vector
                randVec = np.random.normal(loc=0.0, scale=np.std(rowNorms), size=self.n_atoms)
                rowNormRan = rowNorms + randVec
                # Sorting the new random norm vector
                permutations = np.argsort(rowNormRan)
                permutations = permutations[::-1]
                # Sorting accordingly the Coulomb matrix
                tempRandCM = tempCM[permutations, :]
                tempRandCM = tempRandCM[:,permutations]
                # Adding flattened and trimmed randomly sorted Coulomb matrix to the final descriptor matrix
                coulRS[counter, :] = self.trimAndFlat(tempRandCM)
                counter = counter + 1

            # Copying multiple values of the energies
            y_bigdata[numRep*i:numRep*i+numRep] = y_data[i]

        return coulRS, y_bigdata

    def generateTriangCM(self):
        """
        This function returns the flattened triangular part of the original Coulomb matrix for each sample in the data.

        :return: numpy array of shape (n_samples, n_atoms * (n_atoms+1)/2 )
        """
        self.trimCM = np.zeros((self.n_samples, int(self.n_atoms * (self.n_atoms+1) * 0.5)))

        for i in range(self.n_samples):
            tempCM = np.reshape(self.coulMatrix[i,:], (self.n_atoms, self.n_atoms))
            self.trimCM[i,:] = self.trimAndFlat(tempCM)

        return self.trimCM

    def trimAndFlat(self, X):
        """
        This function takes one Coulomb matrix and returns the triangular part of it as a vector.

        :X: Coulomb matrix for *one* sample. numpy array of shape (n_atoms, n_atoms)
        :return: numpy array of shape (n_atoms*(n_atoms+1)/2, )
        """
        size = int(self.n_atoms * (self.n_atoms+1) * 0.5)
        temp = np.zeros((size,))
        counter = 0

        for i in range(self.n_atoms):
            for j in range(i, self.n_atoms):
                temp[counter] = X[i][j]
                counter = counter + 1

        return temp

    def generatePRCM(self, y_data, numRep=2):
        """
        This function generates the partially randomised Coulomb matrix. This consists in a matrix where the columns and
        rows corresponding to each atom are ordered with increasing nuclear charge and when there are atoms with the
        same nuclear charge the columns and rows are randomised.

        :y_data: the energies for each sample - numpy array of shape (n_samples,)
        :numRep: The largest number of permutations to be carried out
        :return: the new Coulomb matrix - numpy array of shape (n_samples*n, n_features) and the y array of shape (n_samples*min(n_perm, numRep),)
        """
        PRCM = []

        for j in range(self.n_samples):
            flatMat = self.coulMatrix[j, :]
            currentMat = np.reshape(flatMat, (self.n_atoms, self.n_atoms))

            # Check if there are two elements that are the same (check elements along diagonal)
            diag = currentMat.diagonal()
            idx_sort = np.argsort(diag)
            sorted_diag = diag[idx_sort]
            vals, idx_start, count = np.unique(sorted_diag, return_counts=True, return_index=True)

            # Work out the number of possible permutations n_perm
            permarr = factorial(count)
            n_perm = int(np.prod(permarr))

            # Decide which one is smaller, numRep or n_perm
            if numRep >= n_perm:
                isNumRepBigger = True
            else:
                isNumRepBigger = False

            # Finding out which rows/columns need permuting. Each element of dupl_col is a list of the indexes of the
            # columns that can be permuted.
            dupl_col = []
            for j in range(count.shape[0]):
                dupl_ind = range(idx_start[j],idx_start[j]+count[j])
                dupl_col.append(dupl_ind)

            # Permute the appropriate indexes randmoly
            if isNumRepBigger:
                permut_idx = self.permutations(dupl_col, n_perm, self.n_atoms)
            else:
                permut_idx = self.permutations(dupl_col, numRep, self.n_atoms)

            # Order the rows/coloumns in terms of smallest to largest diagonal element
            currentMat = currentMat[idx_sort, :]
            currentMat = currentMat[:, idx_sort]

            # Apply the permutations that have been obtained to the rows and columns
            for i in range(min(numRep,n_perm)):
                currentMat = currentMat[permut_idx[i], :]
                currentMat = currentMat[:, permut_idx[i]]
                PRCM.append(self.trimAndFlat(currentMat))

        # Turn PRCM into a numpy array of size (n_samples*min(n_perm, numRep), n_features)
        PRCM = np.asarray(PRCM)

        # Modify the shape of y
        y_big = np.asarray(np.repeat(y_data,min(n_perm, numRep)))

        return PRCM, y_big

    def permutations(self, col_idx, num_perm, n_atoms):
        """
        This function takes a list of the columns that need permuting. It returns num_perm arrays of permuted indexes.
        It returns a numpy array where each row is a different permutation of the indexes. For example, if col_idx was:

        ``[[1 2 3], [4 5]]``

        This means that the columns 1 2 3 correspond to atoms with identical nuclear charge and 4 5 also have the same
        nuclear charge among them. if ``num_perm = 3``, then this function could return:

        ``[[3 2 1 4 5], [2 1 3 4 5], [3 1 2 5 4]]``

        :col_idx: list of list of columns' indexes that need permuting
        :num_perm: number of permutations desired (int)
        :n_atoms: total number of atoms in the system
        :return: an array of shape (num_perm, n_atoms) of permuted indexes.
        """
        all_perm = np.zeros((num_perm, n_atoms), dtype=np.int8)
        temp = col_idx

        for j in range(num_perm):
            for i in range(len(col_idx)):
                temp[i] = np.random.permutation(col_idx[i])
            flat_temp = [item for sublist in temp for item in sublist]
            all_perm[j,:] = flat_temp

        return all_perm

    def plot(self, X):
        """
        This function plots a Coulomb matrix as a heatmap.

        :X: A flat coulomb matrix - numpy array of shape (n_atoms**2,1)
        """
        import seaborn as sns

        matrix = np.reshape(X, (self.n_atoms, self.n_atoms))
        sns.heatmap(data=matrix, cmap='YlOrRd', vmin=0, vmax=60)
        # sns.plt.savefig("CM1.png", transparent=True, dpi=800)
        sns.plt.show()



