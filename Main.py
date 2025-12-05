#cosc 1010 Final Project
#Monte Carlo simmulation, end of game strategies for basketball game
#Finish date 12/5/25
#Due Date 12/5/25

import random

#Parameters for the game

NUM_TRIALS = 10000

#shooting percentages
three_point_pct =  0.35
two_point_pct = 0.55
opp_free_throw_pct = 0.65

prob_offensive_rebound = 0.25
prob_win_overtime = 0.50

#Times (in seconds)

start_time = 30.0
time_for_three = 7.0
time_for_two = 5.0
time_for_foul = 3.0
time_for_final_shot = 7.0
time_for_rebound = 3.0


#Function for did a shot go in?

def shot_made(probability):
    return random.random() < probability
    #returns true if a shot with said probability goes in


#Strategy #1:

def simulate_three_point_strategy():
    time_remaining = start_time
    score_diff = 3
    points_scored = 0
    time_remaining -= time_for_three
    if time_remaining <= 0:
        return False, points_scored
    if shot_made(three_point_pct):
        score_diff += 3
        points_scored += 3
        if shot_made(prob_win_overtime):
            return True, points_scored
        else:
            return False, points_scored
    else:
        return False, points_scored
    
    
    #strategy #2, quick 2 point, foul, try to win with a 3
def simulate_foul_strategy():
    time_remaining = start_time
    score_diff = -3
    points_scored = 0

    time_remaining -= time_for_two
    if time_remaining <= 0:
        return False, points_scored
    
    if shot_made(two_point_pct):
        score_diff += 2
        points_scored += 2
    else:
        time_remaining -= time_for_rebound
        if time_remaining <= 0 or not shot_made(prob_offensive_rebound):
            return False, points_scored
        
        time_remaining -= time_for_two
        if time_remaining <= 0:
            return False, points_scored
        
        if shot_made(two_point_pct):
            score_diff += 2
            points_scored += 2
        else:
            return False, points_scored
        
# Hopefully down by 1 at this point

    time_remaining -= time_for_foul
    if time_remaining <= 0:
        return False, points_scored
    
    free_throws_made = 0
    for _ in range(2):
        if shot_made(opp_free_throw_pct):
            free_throws_made += 1

    score_diff -= free_throws_made

    time_remaining -= time_for_final_shot
    if time_remaining <= 0:
        return False, points_scored
    
    if shot_made(three_point_pct):
        points_scored += 3
        score_diff += 3

        if score_diff> 0:
            return True, points_scored
        elif score_diff == 0:
            if shot_made(prob_win_overtime):
                return True, points_scored
            else:
                return False, points_scored
        else:
            return False, points_scored
    else:
        return False, points_scored
    
#Run the Monte Carlo now

def run_simulation(NUM_TRIALS):
    three_wins = 0
    foul_wins = 0
    three_points_total = 0
    foul_points_total = 0

    for _ in range(NUM_TRIALS):
        win_three, pts_three = simulate_three_point_strategy()
        if win_three:
            three_wins += 1
        three_points_total += pts_three

        win_foul, pts_foul = simulate_foul_strategy()
        if win_foul:
            foul_wins += 1
        foul_points_total += pts_foul


#Computing Statistics
    three_win_percent = 100.0 * three_wins / NUM_TRIALS
    foul_win_percent = 100.0 * foul_wins / NUM_TRIALS
    three_avg_points = three_points_total / NUM_TRIALS
    foul_avg_points = foul_points_total / NUM_TRIALS

    print("After", NUM_TRIALS, "simulated games:\n")

    print("Strategy 1: Take a 3 pointer right away")
    print("Win percentage:", three_win_percent)
    print("Average points scored:", three_avg_points)
    print()

    print("Strategy 2: Quick 2 point, then foul, then 3")
    print("Win percentage:", foul_win_percent)
    print("Average points scored:", foul_avg_points)


run_simulation(NUM_TRIALS)
