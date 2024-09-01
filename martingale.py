""""""
from matplotlib.pyplot import legend
from numpy import dtype
from scipy.ndimage import label

"""Assess a betting strategy.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		 	   		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		 	   		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		 	   		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		 	   		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   		  		  		    	 		 		   		 		  
or edited.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		 	   		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		 	   		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
Student Name: Tucker Balch (replace with your name)  		  	   		 	   		  		  		    	 		 		   		 		  
GT User ID: tb34 (replace with your User ID)  		  	   		 	   		  		  		    	 		 		   		 		  
GT ID: 900897987 (replace with your GT ID)  		  	   		 	   		  		  		    	 		 		   		 		  
"""

'''
YT notes. Assignment requirement breakdown:
1. modify bet strategy
- [?] how
- start with bet amount of $1. if lose, bet amount * 2
- win += bet amount
- loss -= bet amount

2. make bets
- 1000 successive bets -> 1 episode
- make bets by making successive calls to the get_spin_result(win_prob)
    - need to update the win_prob according to the correct probability of winning
    - [?] how to know what to put for win_prob?

[!] run the simulator repeatedly with randomised input and assess result in aggregate 

3. experiment 1
(I) produce 1 plot
- run 10 episodes 
- plot graph 
    - x: 0-300 (number of episodes?)
    - y: -256 to +100 (money left after each episode)

(II) produce 1 plot
- run 1000 episodes
- plot graph
    - x: 0-300 (spin round)
    - y: -256 to +100 (mean winnings for each spin round)
        > mean winnings of each spin round.
        > each episode will have 1000 spins. I will need to take the 1st spin of each episode and average the winnings (+/-).
    - 3 lines: mean, mean+std, mean-std at each point 
    
(III) produce 1 plot 
- use data in figure 2 and produce median of each spin round
- plot graph
    - x: 0-300 (spin round)
    - y: -256 to +100 (median winnings for each spin round)
    - 3 lines: median, median+std, median-std at each point 
'''
  		  	   		 	   		  		  		    	 		 		   		 		  
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def author():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    return "ylee948"  # replace tb34 with your Georgia Tech username.
  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
def gtid():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The GT ID of the student  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: int  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    return 904058037  # replace with your GT ID number

def study_group():
    return "ylee948"
  		  	   		 	   		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    Given a win probability between 0 and 1, the function returns whether the probability will result in a win.  		  	   		 	   		  		  		    	 		 		   		 		  
  		  	   		 	   		  		  		    	 		 		   		 		  
    :param win_prob: The probability of winning  		  	   		 	   		  		  		    	 		 		   		 		  
    :type win_prob: float  		  	   		 	   		  		  		    	 		 		   		 		  
    :return: The result of the spin.  		  	   		 	   		  		  		    	 		 		   		 		  
    :rtype: bool 
    
    YT notes:
    - np.random.random() gives a number between 0 and 1 		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    result = False  		  	   		 	   		  		  		    	 		 		   		 		  
    if np.random.random() <= win_prob:  		  	   		 	   		  		  		    	 		 		   		 		  
        result = True  		  	   		 	   		  		  		    	 		 		   		 		  
    return result  		  	   		 	   		  		  		    	 		 		   		 		  

def unlimited_bankroll():
    # print('Unlimited Bankroll')
    # print('======================================')
    winnings_list:[int] = []
    spin_round = 0
    episode_winnings = 0
    total_win_amount = 0
    total_loss_amount = 0
    win_prob = 18 / 37  # there are 18 black and 18 red and 1 green in the American Roulette
    while episode_winnings < 80:
        won = False
        bet_amount = 1
        while not won:
            # print('Spin Round:', spin_round)
            won = get_spin_result(win_prob)

            # print(f'\tBet amount: {bet_amount}')
            # print(f'\tResult: {"Won" if won else "Loss"}')

            if won:
                episode_winnings = episode_winnings + bet_amount
                total_win_amount = total_win_amount + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount
                total_loss_amount = total_loss_amount + bet_amount
                bet_amount = bet_amount * 2

            # print(f'\tAccumulated winnings: {episode_winnings}')
            winnings_list.append(episode_winnings)
            spin_round += 1

    # print(f'It took {spin_round} rounds to win $80')
    # print(f'Total win amount: {total_win_amount}')
    # print(f'Total loss amount: {total_loss_amount}')

    if spin_round < 1000:
        for i in range(spin_round, 1000):
            winnings_list.append(winnings_list[-1])

    return winnings_list

def limited_bankroll():
    # print('Limited Bankroll')
    # print("==================================")
    winnings_list:[int] = []
    spin_round = 0
    episode_winnings = 256
    win_prob = 18 / 37  # there are 18 black and 18 red and 1 green in the American Roulette
    insufficient_funds = False
    while -256 <= episode_winnings - 256 < 80 and not insufficient_funds:
        won = False
        bet_amount = 1
        while not won:
            # print('Spin Round:', spin_round)
            won = get_spin_result(win_prob)

            # print(f'\tBet amount: ${bet_amount}')
            # print(f'\tFunds left: ${episode_winnings}')
            #
            # print(f'\tResult: {"Won" if won else "Loss"}')

            if won:
                episode_winnings = episode_winnings + bet_amount
            else:
                episode_winnings = episode_winnings - bet_amount

                if episode_winnings <= 0:
                    # print(f'=======Stopped at {spin_round} rounds.=======')
                    # print(f'Insufficient funds. Bet amount is ${bet_amount} but funds left is ${episode_winnings}')
                    insufficient_funds = True
                    break

                bet_amount = bet_amount * 2
                if bet_amount > episode_winnings:
                    bet_amount = episode_winnings

            # print(f'\tAccumulated winnings: {episode_winnings - 256}')
            winnings_list.append(episode_winnings-256)
            spin_round += 1

    # if not insufficient_funds:
    #     print(f'It took {spin_round} rounds to win $80')

    if spin_round < 1000:
        for i in range(spin_round, 1000):
            winnings_list.append(winnings_list[-1])

    return winnings_list

def experiment_1():
    # Figure 1 - 10 episodes
    episodes_10 = []

    for i in range(10):
        episodes_10.append(unlimited_bankroll())

    columns = np.array(list(range(1, 1001)))
    rows = np.array(list(range(1, 11)))
    # column_index = pd.MultiIndex.from_product([['Winnings for each round'], columns])
    # row_index = pd.MultiIndex.from_product([['Episode'], rows])
    df_10_episodes = pd.DataFrame(episodes_10, columns=columns, index=rows)
    # print(df_10_episodes)

    fig_1 = plt.figure(1)
    plt.xlim(0,300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin round')
    plt.ylabel('Winnings')
    plt.title('Experiment 1 - Unlimited bankroll, 10 episodes\nCumulative winnings for each episode')

    for i in range(10):
        plt.plot(columns, np.array(episodes_10[i]), label='Episode '+str(i+1))

    plt.legend()
    # plt.show()
    # fig_1.savefig('./images/figure1_exp1_10eps_cumulative.png')

    # Figure 2 - 1000 episodes (mean)
    episodes_1000 = []

    for i in range(1000):
        episodes_1000.append(unlimited_bankroll())

    rows_1000 = np.array(list(range(1, 1001)))
    df_1000_episodes = pd.DataFrame(episodes_1000, columns=columns, index=rows_1000)
    mean_1000_episodes = df_1000_episodes.mean()
    std_1000_episodes = df_1000_episodes.std()
    median_1000_episodes = df_1000_episodes.median()

    print(f'Mean of all winnings: {mean_1000_episodes.sum()/1000}')
    # print(f'Standard deviation of each spin round over 1000 episodes in experiment 1: {std_1000_episodes}')

    # plt.figure(6)
    # plt.xlim(0, 300)
    # plt.ylim(-256, 100)
    # plt.plot(columns, np.array(std_1000_episodes))

    fig_2 = plt.figure(2)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin round')
    plt.ylabel('Mean winnings')
    plt.title('Experiment 1 - Unlimited bankroll, 1000 episodes\nMean winnings for each spin round')

    plt.plot(columns, np.array(mean_1000_episodes), label='Mean')
    plt.plot(columns, np.array(mean_1000_episodes.add(std_1000_episodes)), label='Mean + Std')
    plt.plot(columns, np.array(mean_1000_episodes.sub(std_1000_episodes)), label='Mean - Std')

    plt.legend()
    # plt.show()
    # fig_2.savefig('./images/figure2_exp1_1000eps_mean.png')

    # Figure 3 - 1000 episodes (median)
    fig_3 = plt.figure(3)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin round')
    plt.ylabel('Median winnings')
    plt.title('Experiment 1 - Unlimited bankroll, 1000 episodes\nMedian winnings for each spin round')

    plt.plot(columns, np.array(median_1000_episodes), label='Median')
    plt.plot(columns, np.array(median_1000_episodes.add(std_1000_episodes)), label='Median + Std')
    plt.plot(columns, np.array(median_1000_episodes.sub(std_1000_episodes)), label='Median - Std')

    plt.legend()
    # plt.show()
    # fig_3.savefig('./images/figure3_exp1_1000eps_median.png')

def experiment_2():

    episodes_1000 = []
    for i in range(1000):
        episodes_1000.append(limited_bankroll())

    columns = np.array(list(range(1, 1001)))
    rows = np.array(list(range(1, 1001)))
    df_1000_episodes = pd.DataFrame(episodes_1000, columns=columns, index=rows)
    mean_1000_episodes = df_1000_episodes.mean()
    std_1000_episodes = df_1000_episodes.std()
    median_1000_episodes = df_1000_episodes.median()

    # Figure 4 - 1000 episodes (Mean)
    fig_4 = plt.figure(4)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin round')
    plt.ylabel('Winnings')
    plt.title('Experiment 2 - Limited bankroll, 1000 episodes\nMean winnings for each spin round')

    plt.plot(columns, np.array(mean_1000_episodes), label='Mean')
    plt.plot(columns, np.array(mean_1000_episodes.add(std_1000_episodes)), label='Mean + Std')
    plt.plot(columns, np.array(mean_1000_episodes.sub(std_1000_episodes)), label='Mean - Std')

    plt.legend()
    # plt.show()
    # fig_4.savefig('./images/figure4_exp2_1000eps_mean.png')

    # Figure 5 - 1000 episodes (Median)
    fig_5 = plt.figure(5)
    plt.xlim(0, 300)
    plt.ylim(-256, 100)
    plt.xlabel('Spin round')
    plt.ylabel('Winnings')
    plt.title('Experiment 2 - Limited bankroll, 1000 episodes\nMedian winnings for each spin round')

    plt.plot(columns, np.array(median_1000_episodes), label='Median')
    plt.plot(columns, np.array(median_1000_episodes.add(std_1000_episodes)), label='Median + Std')
    plt.plot(columns, np.array(median_1000_episodes.sub(std_1000_episodes)), label='Median - Std')

    plt.legend()
    # plt.show()
    # fig_5.savefig('./images/figure5_exp2_1000eps_median.png')

def test_code():  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    Method to test your code  		  	   		 	   		  		  		    	 		 		   		 		  
    """  		  	   		 	   		  		  		    	 		 		   		 		  
    win_prob = 0.60  # set appropriately to the probability of a win  		  	   		 	   		  		  		    	 		 		   		 		  

    np.random.seed(gtid())  # do this only once
        # returns None

    # print(get_spin_result(win_prob))  # test the roulette spin
    # add your code here to implement the experiments
    experiment_1()
    experiment_2()
  		  	   		 	   		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		 	   		  		  		    	 		 		   		 		  
    test_code()

    # ls = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    # ls_2 = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    # nd_1 = np.array([np.array(ls), np.array(ls_2)], dtype=object )
    # columns = list(range(1, 11))
    # rows = list(range(1, 3))
    # df_1 = pd.DataFrame([ls, ls_2], rows, columns)
    # print(df_1)
