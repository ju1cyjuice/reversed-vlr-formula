import pandas as pd

# Rating Formula is from a linear regression model in the .Rmd file
def calculate_rating(kills, deaths, assists, first_kills, first_deaths, kast_percent, adr, rounds):
    rating = (
        0.7339368
        + 1.1087893 * (kills / rounds)
        - 0.9253321 * (deaths / rounds)
        + 0.2213096 * (assists / rounds)
        - 0.2574188 * (first_deaths / rounds)
        + 0.0039686 * (adr * rounds - kills * 150) / rounds
    )
    return round(rating, 2)

def modify_csv(rounds):
    df = pd.read_csv('stats.csv')
    df['Rating'] = df.apply(lambda row: calculate_rating(int(row['Kills']), int(row['Deaths']), int(row['Assists']), int(row['FK']), int(row['FD']), float(row['KAST']), float(row['ADR']), rounds), axis=1)
    df = df.sort_values(by='Rating', ascending=False)
    df.to_csv('stats.csv', index=False)

if __name__=="__main__":
    rounds = int(input("Number of Rounds: "))
    modify_csv(rounds)

    # ratings = []
    # names = []
    # n = int(input("# of players: "))
    # for i in range(n): 
    #     name = input("Player Name: ")
    #     names.append(name)
    #     kills = int(input("# of kills: "))
    #     deaths = int(input("# of deaths: "))
    #     assists = int(input("# of assists: "))
    #     fk = int(input("# of first kills: "))
    #     fd = int(input("# of first deaths: "))
    #     kast = int(input("KAST (without the %): "))
    #     adr = float(input("Average Damage per Round: "))
    #     rounds = int(input("# of rounds: "))
    #     ratings.append(calculate_rating(kills, deaths, assists, fk, fd, kast, adr, rounds))
    
    # ratings, names = zip(*sorted(zip(ratings, names), reverse=True))
    # ratings = list(ratings)
    # names = list(names)
    
    # print("-----------------------------------------")
    # for i in range(n):
    #     print(f"{names[i]}: {ratings[i]}")
