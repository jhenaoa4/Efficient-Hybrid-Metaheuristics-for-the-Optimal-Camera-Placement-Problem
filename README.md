# Efficient Hybrid Metaheuristics for the Optimal Camera Placement Problem

By Juliana Henao and Juan Carlos Rivera

To perform various surveillance tasks the use of camera networks is now important and the way this networks are placed can be a very complex problem to solve. In this regard, a variation of the well-known Set Covering Problem can be used to model this issue and its solution brings a way to place the camera network concerned. Thus, in this project there was implemented a Hybrid Metaheuristics, also evaluated its performance in order to solve the Optimal Camera Placement problem. The algorithm consist in a constructive part with a local neighbourhood search and a genetic part with exacts methods solved in Gurobi. The performance of the metaheuristics shows good solutions to the data sets used in the experiments.

## Statement of the problem

The Optimal Camera Placement Problem (OCP) is a special case of the of the Unicost Set Covering Problem (USCP) that consists of finding the optimal way to place cameras in order to cover an area to be monitored.

## Solution and Results

In order to solve the problem set above, a hybrid metaheuristic was developed, this algorithm has two parts, first there is a constructive hybrid part where a initial solution is built using also a Local Neighborhood Search (LNS) algorithm (destroy and repair), then that solution will be part of a initial population for a hybrid genetic algorithm.

The details of the description of the problem, the hybrid algorithm and results are in the paper atatched in this repository: Hybrid Metaheuristic Juliana Henao.pdf

## Run algorithm

In order to run this Metaheuristic, run the file
 
```bash
  OCPsolution.py
```
