from pydantic import BaseModel


class Character(BaseModel):
    id: int
    birth_year: str
    eye_color: str
    films: list[str]
    gender: str
    hair_color: str
    height: str
    homeworld: str
    mass: str
    name: str
    skin_color: str
    species: list[str] | list
    starships: list[str] | list
    vehicles: list[str] | list
