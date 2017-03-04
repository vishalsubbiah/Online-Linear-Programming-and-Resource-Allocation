# Online-Linear-Programming-and-Resource-Allocation
Project for CME 307

Problem 0: Saturday, 4 March

## Note: The Difference Online and Offline: 

Offline: No incoming orders, all bets are fixed. 

Online: While you're performing the optimization, you may get another order or bid. Set up everything prior to the new order and an assume prior orders are already decided. Then solve the single optimization problem for the lone new order with the previous order values now fixed. 

## Note: Shadow Pricing in SLPM

Treat the problem as offline at first. Take those values, and store them as a state price vector. 
Then introduce 1 through j bidders (j+1 through k unknown), and use the former state price vector for the
j+1 through k bidders. 
