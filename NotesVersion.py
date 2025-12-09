
#Skeleton Program code for the AQA A Level Paper 1 Summer 2026 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9 programming environment

# paper one sections c and d

import random

def Main():
    SimulationParameters = []
    validSim = False #
    while not validSim: #
        SimNo = input("Enter simulation number: ")
        '''
        parameters = [StartingNumberOfNests, NumberOfRows, NumberOfColumns,
                      StartingFoodInNest, StartingNumberOfFoodCells, StartingAntsInNest,
                      NewPheromoneStrength, PheromoneDecay
        '''
        if SimNo == "1":
            SimulationParameters = [1, 5, 5, 500, 3, 5, 1000, 50]
            validSim = True #
        elif SimNo == "2":
            SimulationParameters = [1, 5, 5, 500, 3, 5, 1000, 100]
            validSim = True #
        elif SimNo == "3":
            SimulationParameters = [1, 10, 10, 500, 3, 9, 1000, 25]
            validSim = True #
        elif SimNo == "4":
            SimulationParameters = [2, 10, 10, 500, 3, 6, 1000, 25]
            validSim = True #
    ThisSimulation = Simulation(SimulationParameters)

    Choice = ""
    while Choice != "9":
        DisplayMenu()
        '''
        menu options
        1. display overal fetails
        2. display area details
        3. inspect cell
        4. advance on stage
        5. advance x stage
        9. quit
        '''
        Choice = GetChoice()
        if Choice == "1":
            print(ThisSimulation.GetDetails())
        elif Choice == "2":
            StartRow = 0
            StartColumn = 0
            EndRow = 0
            EndColumn = 0
            StartRow, StartColumn = GetCellReference()
            EndRow, EndColumn = GetCellReference()
            print(ThisSimulation.GetAreaDetails(StartRow, StartColumn, EndRow, EndColumn))
        elif Choice == "3":
            Row = 0
            Column = 0
            Row, Column = GetCellReference()
            print(ThisSimulation.GetCellDetails(Row, Column))
        elif Choice == "4":
            ThisSimulation.AdvanceStage(1)
            print("Simulation moved on one stage\n")
        elif Choice == "5":
            NumberOfStages = int(input("Enter number of stages to advance by: "))
            ThisSimulation.AdvanceStage(NumberOfStages)
            print(f"Simulation moved on {NumberOfStages} stages" + "\n")
    #input() dont know why this is here

def DisplayMenu():
    print()
    print("1. Display overall details")
    print("2. Display area details")
    print("3. Inspect cell")
    print("4. Advance one stage")
    print("5. Advance X stages")
    print("9. Quit")
    print()
    print("> ", end='')

def GetChoice():
    Choice = input()
    return Choice

def GetCellReference():
    print()
    Row = int(input("Enter row number: "))
    Column = int(input("Enter column number: "))
    print()
    return Row, Column


class Simulation():
    # construction method
    def __init__(self, SimulationParameters):
        self._StartingNumberOfNests = SimulationParameters[0]
        self._NumberOfRows = SimulationParameters[1]
        self._NumberOfColumns = SimulationParameters[2]
        self._StartingFoodInNest = SimulationParameters[3]
        self._StartingNumberOfFoodCells = SimulationParameters[4]
        self._StartingAntsInNest = SimulationParameters[5]
        self._NewPheromoneStrength = SimulationParameters[6]
        self._PheromoneDecay = SimulationParameters[7]
        self._Nests = []
        self._Ants = []
        self._Pheromones = []
        self._Grid = []

        Row = 0
        Column = 0
        for Row in range(1, self._NumberOfRows + 1):
            for Column in range(1, self._NumberOfColumns + 1):
                self._Grid.append(Cell(Row, Column))
                # sets up 1d list (grid) of cell objects

        # sets up a nest at 2,4 every time
        # if multiple nests then the other is random
        self.SetUpANestAt(2, 4)
        for Count in range(2, self._StartingNumberOfNests + 1):
            Allowed = False
            while Allowed == False:
                Allowed = True
                Row = random.randint(1, self._NumberOfRows)
                Column = random.randint(1, self._NumberOfColumns)
                for N in self._Nests:
                    if N.GetRow() == Row and N.GetColumn() == Column:
                        Allowed = False
            self.SetUpANestAt(Row, Column)

        # food can be placed where ever there is no 2 4 nest (no other check)
        # no check at other nest !!
        for Count in range(1, self._StartingNumberOfFoodCells + 1):
            Row = 2
            Column = 4
            while Row == 2 and Column == 4:
                Row = random.randint(1, self._NumberOfRows)
                Column = random.randint(1, self._NumberOfColumns)
            self.AddFoodToCell(Row, Column, 500)
            # 500 food is hard coded


    def SetUpANestAt(self, Row, Column):
        # sets up a nest at the specific place, with food(p) with a queen ant and worker ants(p)
        self._Nests.append(Nest(Row, Column, self._StartingFoodInNest))
        self._Ants.append(QueenAnt(Row, Column, Row, Column))
        for Worker in range(2, self._StartingAntsInNest + 1):
            self._Ants.append(WorkerAnt(Row, Column, Row, Column))

    def AddFoodToCell(self, Row, Column, Quantity):
        # adds food to the chosen cell
        self._Grid[self.__GetIndex(Row, Column)].UpdateFoodInCell(Quantity)

    def __GetIndex(self, Row, Column):
        # index of cell from its row and col
        print(Row,Column, (Row - 1) * self._NumberOfColumns + Column - 1)
        return (Row - 1) * self._NumberOfColumns + Column - 1
        ''' sim1 (5)
        3 1 = 2*5+0 = 10
        4 2 = 3*5+1 = 16
        5 5 = 4*5+4 = 24
        '''

    def __GetIndicesOfNeighbours(self, Row, Column):
        ListOfNeighbours = []
        for RowDirection in [-1, 0, 1]:
            for ColumnDirection in [-1, 0, 1]:
                NeighbourRow = Row + RowDirection
                NeighbourColumn = Column + ColumnDirection
                # checking if neighbour is valid, else -1 = invlaid
                if (RowDirection != 0 or ColumnDirection != 0) and NeighbourRow >= 1 and NeighbourRow <= self._NumberOfRows and NeighbourColumn >= 1 and NeighbourColumn <= self._NumberOfColumns:
                    ListOfNeighbours.append(self.__GetIndex(NeighbourRow, NeighbourColumn))
                else:
                    ListOfNeighbours.append(-1)
        # returns list (len of 9) indecies
        return ListOfNeighbours

    def __GetIndexOfNeighbourWithStrongestPheromone(self, Row, Column):
        StrongestPheromone = 0
        IndexOfStrongestPheromone = -1
        # why would it return -1 !!
        # gets all neighbours then checks the largest p, returns the neighbours index
        for Index in self.__GetIndicesOfNeighbours(Row, Column):
            if Index != -1 and self.GetStrongestPheromoneInCell(self._Grid[Index]) > StrongestPheromone:
                IndexOfStrongestPheromone = Index
                StrongestPheromone = self.GetStrongestPheromoneInCell(self._Grid[Index])
        return IndexOfStrongestPheromone

    def GetNestInCell(self, C):
        # checks if there is a nest in the cell
        for N in self._Nests:
            if N.InSameLocation(C):
                return N
        return None

    def UpdateAntsPheromoneInCell(self, A):
        for P in self._Pheromones:
            # if there is a p in the same cell and of the same ant this function is called for
            # increases the pheramone by the parameter
            if P.InSameLocation(A) and P.GetBelongsTo() == A.GetID():
                P.UpdateStrength(self._NewPheromoneStrength)
                return
        # else creates a new p at the ants cell, belonging to the ant and with the sim parameters
        self._Pheromones.append(Pheromone(A.GetRow(), A.GetColumn(), A.GetID(), self._NewPheromoneStrength, self._PheromoneDecay))

    def GetNumberOfAntsInCell(self, C):
        # checks how many ants in cell
        Count = 0
        for A in self._Ants:
            if A.InSameLocation(C):
                Count += 1
        return Count

    def GetNumberOfPheromonesInCell(self, C):
        # checks how many p in cell
        Count = 0
        for P in self._Pheromones:
            if P.InSameLocation(C):
                Count += 1
        return Count

    def GetStrongestPheromoneInCell(self, C):
        Strongest = 0
        # checks each pheromone in cell, returns the strongest
        for P in self._Pheromones:
            if P.InSameLocation(C):
                if P.GetStrength() > Strongest:
                    Strongest = P.GetStrength()
        return Strongest

    def GetDetails(self):
        Details = ""
        for Row in range(1, self._NumberOfRows + 1):
            for Column in range(1, self._NumberOfColumns + 1):
                Details += f"{Row}, {Column}: "
                TempCell = self._Grid[self.__GetIndex(Row, Column)]
                if self.GetNestInCell(TempCell) is not None:
                    Details += "| Nest |  "
                NumberOfAnts = self.GetNumberOfAntsInCell(TempCell)
                if NumberOfAnts > 0:
                    Details += f"| Ants: {NumberOfAnts} |  "
                NumberOfPheromones = self.GetNumberOfPheromonesInCell(TempCell)
                if NumberOfPheromones > 0:
                    Details += f"| Pheromones: {NumberOfPheromones} |  "
                AmountOfFood = TempCell.GetAmountOfFood()
                if AmountOfFood > 0:
                    Details += f"| {AmountOfFood} food |  "
                Details += "\n"
        return Details

    def GetAreaDetails(self, StartRow, StartColumn, EndRow, EndColumn):
        Details = ""
        for Row in range(StartRow, EndRow + 1):
            for Column in range(StartColumn, EndColumn + 1):
                Details += f"{Row}, {Column}: "
                TempCell = self._Grid[self.__GetIndex(Row, Column)]
                if self.GetNestInCell(TempCell) is not None:
                    Details += "| Nest |  "
                NumberOfAnts = self.GetNumberOfAntsInCell(TempCell)
                if NumberOfAnts > 0:
                    Details += f"| Ants: {NumberOfAnts} |  "
                NumberOfPheromones = self.GetNumberOfPheromonesInCell(TempCell)
                if NumberOfPheromones > 0:
                    Details += f"| Pheromones: {NumberOfPheromones} |  "
                AmountOfFood = TempCell.GetAmountOfFood()
                if AmountOfFood > 0:
                    Details += f"| {AmountOfFood} food |  "
                Details += "\n"
        return Details

    def AddFoodToNest(self, Food, Row, Column):
        # first checks to find the correct nest
        # then increases the nestfood by food
        for N in self._Nests:
            if N.GetRow() == Row and N.GetColumn() == Column:
                N.ChangeFood(Food)
                return

    def GetCellDetails(self, Row, Column):
        CurrentCell = self._Grid[self.__GetIndex(Row, Column)]
        Details = CurrentCell.GetDetails()
        N = self.GetNestInCell(CurrentCell)
        if N is not None:
            Details += f"Nest present ({N.GetFoodLevel()} food)" + "\n\n"
        if self.GetNumberOfAntsInCell(CurrentCell) > 0:
            Details += "ANTS\n"
            for A in self._Ants:
                if A.InSameLocation(CurrentCell):
                    Details += A.GetDetails() + "\n"
            Details += "\n\n"
        if self.GetNumberOfPheromonesInCell(CurrentCell) > 0:
            Details += "PHEROMONES\n"
            for P in self._Pheromones:
                if P.InSameLocation(CurrentCell):
                    Details += f"Ant {P.GetBelongsTo()} with strength of {P.GetStrength()}" + "\n\n"
            Details += "\n\n"
        return Details

    def AdvanceStage(self, NumberOfStages):
        for Count in range(1, NumberOfStages + 1):
            PheromonesToDelete = []
            for P in self._Pheromones:
                P.AdvanceStage(self._Nests, self._Ants, self._Pheromones)
                if P.GetStrength() == 0:
                    PheromonesToDelete.append(P)
            for P in PheromonesToDelete:
                self._Pheromones.remove(P)
            for A in self._Ants:
                A.AdvanceStage(self._Nests, self._Ants, self._Pheromones)
                CurrentCell = self._Grid[self.__GetIndex(A.GetRow(), A.GetColumn())]
                if A.GetFoodCarried() > 0 and A.IsAtOwnNest():
                    self.AddFoodToNest(A.GetFoodCarried(), A.GetRow(), A.GetColumn())
                    A.UpdateFoodCarried(-A.GetFoodCarried())
                elif CurrentCell.GetAmountOfFood() > 0 and A.GetFoodCarried() == 0:
                    FoodObtained = CurrentCell.GetAmountOfFood() + 1
                    while FoodObtained > CurrentCell.GetAmountOfFood() or (A.GetFoodCarried() + FoodObtained) > A.GetFoodCapacity():
                        FoodObtained = random.randint(1, A.GetFoodCapacity())
                    CurrentCell.UpdateFoodInCell(-FoodObtained)
                    A.UpdateFoodCarried(FoodObtained)
                else:
                    if A.GetFoodCarried() > 0:
                        self.UpdateAntsPheromoneInCell(A)
                    A.ChooseCellToMoveTo(self.__GetIndicesOfNeighbours(A.GetRow(), A.GetColumn()), self.__GetIndexOfNeighbourWithStrongestPheromone(A.GetRow(), A.GetColumn()))
            for N in self._Nests:
                self._Nests, self._Ants, self._Pheromones = N.AdvanceStage(self._Nests, self._Ants, self._Pheromones)

class Entity():
    # all entities have a cell (row, column) and an ID
    def __init__(self, StartRow, StartColumn):
        self._Row = StartRow
        self._Column = StartColumn
        self._ID = None

    def InSameLocation(self, E):
        return E.GetRow() == self._Row and E.GetColumn() == self._Column

    def GetRow(self):
        return self._Row

    def GetColumn(self):
        return self._Column

    def GetID(self):
        return self._ID

    def AdvanceStage(self, Nests, Ants, Pheromones):
        pass

    def GetDetails(self):
        return ""

class Cell(Entity):
    # cells have the attribute of food, everything else is other objects
    def __init__(self, StartRow, StartColumn):
        super().__init__(StartRow, StartColumn)
        self._AmountOfFood = 0

    def GetAmountOfFood(self):
        return self._AmountOfFood

    def GetDetails(self):
        Details = f"{super().GetDetails()}{self._AmountOfFood} food present" + "\n\n"
        return Details

    def UpdateFoodInCell(self, Change):
        self._AmountOfFood += Change

class Ant(Entity):
    _NextAntID = 1
    # each ant will have a unique consequtive ID

    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn):
        # in addition to entity inheritance, ants have their nest, stages alive, food capacity and type
        super().__init__(StartRow, StartColumn)
        self._NestRow = NestInRow
        self._NestColumn = NestInColumn
        self._ID = Ant._NextAntID
        Ant._NextAntID += 1
        self._Stages = 0
        self._AmountOfFoodCarried = 0
        self._FoodCapacity = 0
        self._TypeOfAnt = ""

    def GetFoodCapacity(self):
        return self._FoodCapacity

    def IsAtOwnNest(self):
        return self._Row == self._NestRow and self._Column == self._NestColumn

    def AdvanceStage(self, Nests, Ants, Pheromones):
        self._Stages += 1

    def GetDetails(self):
        return f"{super().GetDetails()}  Ant {self._ID}, {self._TypeOfAnt}, stages alive: {self._Stages}"

    def UpdateFoodCarried(self, Change):
        self._AmountOfFoodCarried += Change

    def _ChangeCell(self, NewCellIndicator, RowToChange, ColumnToChange):
        if NewCellIndicator > 5: # [6,7,8]
            RowToChange += 1
        elif NewCellIndicator < 3: # [0,1,2]
            RowToChange -= 1
        if NewCellIndicator in [0, 3, 6]:
            ColumnToChange -= 1
        elif NewCellIndicator in [2, 5, 8]:
            ColumnToChange += 1
        # [0,1,2,3,4,5,6,7,8] all neighbours
        # finds and returns the direcition
        return RowToChange, ColumnToChange

    def _ChooseRandomNeighbour(self, ListOfNeighbours):
        Chosen = False
        while Chosen == False:
            RNo = random.randint(0, len(ListOfNeighbours) - 1)
            if ListOfNeighbours[RNo] != -1:
                Chosen = True
        # returms random neighbour as long a it exists (is not -1)
        return RNo

    def ChooseCellToMoveTo(self, ListOfNeighbours, IndexOfNeighbourWithStrongestPheromone):
        pass

    def GetFoodCarried(self):
        return self._AmountOfFoodCarried

    def GetNestRow(self):
        return self._NestRow

    def GetNestColumn(self):
        return self._NestColumn

    def GetTypeOfAnt(self):
        return self._TypeOfAnt

# question about the queen doing something !!
class QueenAnt(Ant):
    # queen ant will inherit all the ant attributes and methods
    # queens will not move
    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn): # /:(
        super().__init__(StartRow, StartColumn, NestInRow, NestInColumn)
        self._TypeOfAnt = "queen"

class WorkerAnt(Ant):
    def __init__(self, StartRow, StartColumn, NestInRow, NestInColumn):
        super().__init__(StartRow, StartColumn, NestInRow, NestInColumn)
        self._TypeOfAnt = "worker"
        self._FoodCapacity = 30

    def GetDetails(self):
        return f"{super().GetDetails()}, carrying {self._AmountOfFoodCarried} food, home nest is at {self._NestRow} {self._NestColumn}"

    def ChooseCellToMoveTo(self, ListOfNeighbours, IndexOfNeighbourWithStrongestPheromone):
        # happends to each worker ant when a stage progresses
        # is they have no food they go
        if self._AmountOfFoodCarried > 0:
            if self._Row > self._NestRow:
                self._Row -= 1
            elif self._Row < self._NestRow:
                self._Row += 1
            if self._Column > self._NestColumn:
                self._Column -= 1
            elif self._Column < self._NestColumn:
                self._Column += 1
        elif IndexOfNeighbourWithStrongestPheromone == -1:
            # if they have food they return to the nest by following p
            IndexToUse = self._ChooseRandomNeighbour(ListOfNeighbours)
            self._Row, self._Column = self._ChangeCell(IndexToUse, self._Row, self._Column)
        else:
            # or they
            IndexToUse = ListOfNeighbours.index(IndexOfNeighbourWithStrongestPheromone)
            self._Row, self._Column = self._ChangeCell(IndexToUse, self._Row, self._Column)

class Nest(Entity):
    _NextNestID = 1

    def __init__(self, StartRow, StartColumn, StartFood):
        super().__init__(StartRow, StartColumn)
        self._FoodLevel = StartFood
        self._NumberOfQueens = 1
        self._ID = Nest._NextNestID
        Nest._NextNestID += 1

    def ChangeFood(self, Change):
        # the food can never be negative
        self._FoodLevel += Change
        if self._FoodLevel < 0:
            self._FoodLevel = 0

    def GetFoodLevel(self):
        return self._FoodLevel

    def AdvanceStage(self, Nests, Ants, Pheromones):
        if Ants is None:
            # if ants have all died the sim is over
            return

        AntsToCull = 0
        Count = 0
        for A in Ants:
            if A.GetNestRow() == self._Row and A.GetNestColumn() == self._Column:
                if A.GetTypeOfAnt() == "queen":
                    Count += 10
                else:
                    Count += 2
        self.ChangeFood(-int(Count))
        if self._FoodLevel == 0 and len(Ants) > 0:
            AntsToCull += 1
        if self._FoodLevel < len(Ants):
            AntsToCull += 1
        if self._FoodLevel < len(Ants) * 5:
            AntsToCull += 1
            if AntsToCull > len(Ants):
                AntsToCull = len(Ants)
            for A in range(1, AntsToCull + 1):
                RPos = random.randint(0, len(Ants) - 1)
                if Ants[RPos].GetTypeOfAnt() == "queen":
                    self._NumberOfQueens -= 1
                Ants.pop(RPos)
        else:
            for A in range(1, self._NumberOfQueens + 1):
                RNo1 = random.randint(0, 99)
                if RNo1 < 50:
                    RNo2 = random.randint(0, 99)
                    if RNo2 < 2:
                        Ants.append(QueenAnt(self._Row, self._Column, self._Row, self._Column))
                    else:
                        Ants.append(WorkerAnt(self._Row, self._Column, self._Row, self._Column))
        return Nests, Ants, Pheromones

class Pheromone(Entity):
    def __init__(self, Row, Column, BelongsToAnt, InitialStrength, Decay):
        super().__init__(Row, Column)
        self._BelongsTo = BelongsToAnt
        self._Strength = InitialStrength
        self._PheromoneDecay = Decay

    def AdvanceStage(self, Nests, Ants, Pheromones):
        self._Strength -= self._PheromoneDecay
        if self._Strength < 0:
            self._Strength = 0

    def UpdateStrength(self, Change):
        self._Strength += Change

    def GetStrength(self):
        return self._Strength

    def GetBelongsTo(self):
        return self._BelongsTo

if __name__ == "__main__":
    Main()


'''
CLASS DIAGRAMS:
+ public (most methods)
# protected (these are protected _)
- private (cannot access even if inherited __)
inheritance (arrow point to parent)

Entity (_Row,_Column,_ID)
- Cell (super,_AmountOfFood)
- Ant (super,_NestRow,_NestColumn,Stages,_AmountOfFoodCarried,_FoodCapacity,_TypeOfAnt)
    - QueenAnt (super)
    - WorkerAnt (super)
- Nest (super,_FoodLevel,_NumberOfQueens)
- Pheromone (super,_BelongsTo,_Strength,_PheromoneDecay)519915
'''
