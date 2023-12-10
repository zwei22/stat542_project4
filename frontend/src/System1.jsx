import { useState } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

export default function System1() {
  const [data, setData] = useState([]);
  const [genre, setGenre] = useState("");

  const genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children's",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western",
  ];

  const handleChange = (event) => {
    setGenre(event.target.value);
    async function fetchData() {
      // post request to backend
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/recommend/genre`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ genre: event.target.value }),
        }
      );
      const data = await response.json();
      console.log(data);
      setData(data);
    }
    fetchData();
  };

  return (
    <Box>
      <Typography variant="h4">Select a Genre</Typography>
      <FormControl sx={{ m: 1, width: "100%" }}>
        <InputLabel id="demo-select-small-label">Genre</InputLabel>
        <Select
          labelId="demo-select-small-label"
          id="demo-select-small"
          value={genre}
          label="Genre"
          onChange={handleChange}
        >
          {genres.map((genre) => (
            <MenuItem value={genre} key={genre}>
              {genre}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <Box sx={{ display: "flex", flexFlow: "wrap" }}>
        {data.map((movie) => {
          return (
            <Card
              sx={{ width: 200, margin: 1 }}
              key={movie.MovieID}
              variant="outlined"
            >
              <CardContent>
                <Typography variant="p">{movie.Title}</Typography>
              </CardContent>
            </Card>
          );
        })}
      </Box>
    </Box>
  );
}
