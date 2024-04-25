import subprocess
import re
from scipy.stats import ttest_rel
import random
import numpy as np
import plotly.graph_objects as go


def execute_pacman_simulation(agent, training_sessions, games, map_layout, ghost_strategy, ghost_count):
    command = f"python pacman.py -p {agent} -a numTraining={training_sessions} -x {training_sessions} -n {games} -l {map_layout} -g {ghost_strategy} -k {ghost_count} -q"
    # print(command)
    process_output = subprocess.run(command, stdout=subprocess.PIPE, shell=True)

    average_scores = re.findall(r"Average Score: (\-?\d+\.?\d*)", str(process_output.stdout))
    return [float(score) for score in average_scores]

def perform_statistical_comparisons():
    print("Starting statistical comparisons...")
    agent_list = ['SemiGradientTDQAgent', 'ApproximateQAgent', 'TrueOnlineTDQAgent']
    game_layouts = ['mediumClassic', 'smallGrid','trickyClassic']
    simulation_results = {agent: [] for agent in agent_list}

    for layout in game_layouts:
        for agent in agent_list:
            layout_scores = []
            for _ in range(100):
                ghost_number = random.choice(range(1, 5))
                layout_scores.extend(execute_pacman_simulation(agent, 50, 60, layout, 'RandomGhost', ghost_number))
            simulation_results[agent].append(layout_scores)

    for agent_1 in simulation_results:
        for agent_2 in simulation_results:
            if agent_1 != agent_2:
                for index, layout in enumerate(game_layouts):
                    t_stat, p_val = ttest_rel(simulation_results[agent_1][index], simulation_results[agent_2][index])
                    print(f"T-test between {agent_1} and {agent_2} on {layout}: T-stat={t_stat}, P-value={p_val}")

def simulate_pacman_games():
    agents = ['SemiGradientTDQAgent', 'ApproximateQAgent', 'TrueOnlineTDQAgent']
    episodes_range = list(range(50, 100, 10))
    games_count = 1500
    map_layouts = ['mediumClassic', 'trickyClassic', 'smallGrid']
    ghosts_count = 2
    scores_list = []
    rates_list = []

    print(agents)
    for agent in agents:
        for layout in map_layouts:
            print(layout)
            layout_rates = []
            for episodes in episodes_range:
                cmd = f"python pacman.py -p {agent} -a extractor=SimpleExtractor -x {episodes} -n {games_count} -l {layout} -k {ghosts_count} -q"
                process_result = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

                score_pattern = b'Score:\s*(-?\d+)'
                found_scores = re.findall(score_pattern, process_result.stdout)
                processed_scores = [int(score.decode()) for score in found_scores]
                scores_list.append(sum(processed_scores) / len(processed_scores))

                rate_pattern = b'Win Rate:\s*\d+/\d+\s*\((\d+\.\d+)\)'
                win_rate_match = re.search(rate_pattern, process_result.stdout)
                if win_rate_match:
                    win_rate = float(win_rate_match.group(1))
                    layout_rates.append(win_rate)

            rates_list.append(layout_rates)
            # print(rates_list)
            plot_win_rates(episodes_range, layout_rates, agent, layout)

def plot_win_rates(episodes, win_rates, agent_name, layout_name):
    fig = go.Figure(data=go.Scatter(x=episodes, y=win_rates, mode='lines+markers', name=layout_name))
    fig.update_layout(
        title=f'Win Rates for {agent_name} on {layout_name}',
        xaxis_title='Training Episodes',
        yaxis_title='Win Percentage',
        template='plotly_dark'
    )
    fig.show()

perform_statistical_comparisons()
simulate_pacman_games()
