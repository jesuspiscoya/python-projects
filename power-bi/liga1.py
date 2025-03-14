import os
import requests
from conexion import Conexion
from datetime import date
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("DB_HOST")
database = os.getenv("DB_DATABASE")

# Conexión a la base de datos
conn = Conexion(host, database)
conexion = conn.getConexion()


def get_liga1_seasons(url):
    response = requests.get(url, timeout=10)
    years = []

    if response.status_code == 200:
        data = response.json()

        try:
            cursor = conexion.cursor()
            cursor.execute("DELETE Stats")
            sql_check = "SELECT COUNT(*) FROM Seasons WHERE SeasonID = ?"
            sql_season = "INSERT INTO Seasons VALUES (?, ?, ?, ?, ?)"

            for _season in data["seasons"]:
                if _season["year"] >= 2019:
                    for i, _type in enumerate(_season["types"]):
                        season_id = f"{_season["year"]}0{_type["id"]}"
                        name = _type["abbreviation"]
                        year = _season["year"]
                        start_date = _type["startDate"].split("T")[0]
                        end_date = _type["endDate"].split("T")[0]

                        cursor.execute(sql_check, season_id)
                        exist = cursor.fetchone()[0]

                        if i < 2 and start_date <= date.today().strftime("%Y-%m-%d"):
                            years.append({"year": year, "type": _type["id"]})

                            if exist == 0:
                                cursor.execute(sql_season, (
                                    season_id,
                                    name,
                                    year,
                                    start_date,
                                    end_date
                                ))
                                print(f"Temporada {name} agregada.")

            conexion.commit()
            return years
        except Exception as e:
            print("Error en la consulta: ", e)
        finally:
            cursor.close()
    else:
        print("Error en la solicitud: ", response.status_code)


def get_liga1_teams(url, seasons):
    response = requests.get(url, timeout=10)

    if response.status_code == 200:
        data = response.json()

        try:
            cursor = conexion.cursor()
            sql_check = "SELECT COUNT(*) FROM Teams WHERE TeamID = ?"
            sql_team = "INSERT INTO Teams VALUES (?, ?, ?, ?)"

            for entry in data["children"][0]["standings"]["entries"]:
                cursor.execute(sql_check, entry["team"]["id"])
                exist = cursor.fetchone()[0]

                if exist == 0:
                    cursor.execute(sql_team, (
                        entry["team"]["id"],
                        entry["team"]["displayName"],
                        entry["team"]["abbreviation"],
                        entry["team"]["logos"][0]["href"]
                    ))
                    print(f"Equipo {entry['team']['displayName']} agregado.")

                season_id = f"{seasons["year"]}0{seasons["type"]}"
                team_id = entry["team"]["id"]
                rank = entry["stats"][10]["displayValue"]
                team_season_id = f"{season_id}{team_id}"
                stat_id = f"{season_id}{rank}"
                games_played = entry["stats"][0]["displayValue"]
                wins = entry["stats"][7]["displayValue"]
                ties = entry["stats"][6]["displayValue"]
                losses = entry["stats"][1]["displayValue"]
                goals_for = entry["stats"][5]["displayValue"]
                goals_against = entry["stats"][4]["displayValue"]
                goals_difference = entry["stats"][2]["displayValue"]
                points = entry["stats"][3]["displayValue"]

                get_liga1_teams_seasons((
                    team_season_id,
                    season_id,
                    team_id,
                    rank,
                ))

                get_liga1_statics((
                    stat_id,
                    team_season_id,
                    games_played,
                    wins,
                    ties,
                    losses,
                    goals_for,
                    goals_against,
                    goals_difference,
                    points
                ))

            conexion.commit()
        except Exception as e:
            print("Error al hacer la consulta: ", e)
        finally:
            cursor.close()
    else:
        print("Error al hacer la solicitud:", response.status_code)


def get_liga1_teams_seasons(team_season):
    try:
        cursor = conexion.cursor()
        sql_check = "SELECT COUNT(*) FROM TeamsSeasons WHERE TeamSeasonID = ?"
        sql_team_season = "INSERT INTO TeamsSeasons VALUES (?, ?, ?, ?)"

        cursor.execute(sql_check, team_season[0])
        exist = cursor.fetchone()[0]

        if exist == 0:
            cursor.execute(sql_team_season, team_season)
            print(f"Nuevo código TeamSeason {team_season[0]} agregado.")

        conexion.commit()
    except Exception as e:
        print("Error al hacer la consulta: ", e)
    finally:
        cursor.close()


def get_liga1_statics(stat):
    try:
        cursor = conexion.cursor()
        sql_stat = "INSERT INTO Stats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(sql_stat, stat)
        conexion.commit()
    except Exception as e:
        print("Error al hacer la consulta: ", e)
    finally:
        cursor.close()


seasons_liga1 = get_liga1_seasons(
    "https://site.web.api.espn.com/apis/v2/sports/soccer/per.1/standings")

for season in seasons_liga1:
    get_liga1_teams(
        f"https://site.web.api.espn.com/apis/v2/sports/soccer/per.1/standings?seasontype={season["type"]}&season={season["year"]}&sort=rank", season)

conn.closeConexion()
