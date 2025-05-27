# import matlab.engine
from scipy.constants import mu_0, epsilon_0, c
import pandas as pd
from enum import Enum
import numpy as np
from UI.tools import Distance, Frequency, Conductivity, Permeability, Float, Int, FilePath
class ModelType(Enum):
    PN = 1
    LDMOS = 2
    JFET = 3

class AlgorithmType(Enum):
    FVM = 1
    FDTD = 2
    FEM = 3
class Material(Enum):
    Si = 1
    PolySi = 2
    SiO2 = 3
    Si3N4 = 4
    SiC = 5
    HfO2 = 6
class Arguments(Enum):
    Vth = 1
    GMmax = 2
    IDsat = 3
    Ioff = 4
    Rout = 5
    Ron = 6
    BV = 7

class MeshType(Enum):
    Rectangular = 1
    Triangular = 2
    Hexagonal = 3
    Tetrahedral = 4
    Polyhedral = 5

class SaveType(Enum):
    Plt = 1
    Plx = 2
    Csv = 3
    TDR = 4
    VIS = 5
    TIF = 6


class Solver:
    @staticmethod
    def get_solver(mode=1):
        if mode == 1:
            return Solver.example_solver
        else:
            raise ValueError(f"Unknown mode: {mode}")
    @staticmethod
    def example_solver(
        model_name: str = "Example Model",
        model_type: ModelType = ModelType.PN,
        algorithm: AlgorithmType = AlgorithmType.FVM,
        mesh_type: MeshType = MeshType.Triangular,
        material: Material = Material.Si,
        temperature: Float = 300.0,
        frequency: Frequency = 1e9,
        conductivity: Conductivity = 1e-6,
        permeability: Permeability = mu_0,
        save_argument: Arguments = Arguments.Vth,
        save_path: FilePath = None,
        save_type: SaveType = SaveType.Csv
    ):
        # Placeholder for simulation logic

        print(f"Running solver for model: {model_name}")
        print(f"Model Type: {model_type}")
        print(f"Algorithm: {algorithm}")
        print(f"Mesh Type: {mesh_type}")
        print(f"Material: {material}")
        print(f"Temperature: {temperature} K")
        print(f"Frequency: {frequency} Hz")
        print(f"Conductivity: {conductivity} S/m")
        print(f"Permeability: {permeability} H/m")
        print(f"Save Argument: {save_argument}")
        print(f"Save Path: {save_path}")
        print(f"Save Type: {save_type}")

        






