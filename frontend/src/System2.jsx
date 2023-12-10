import { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import Button from "@mui/material/Button";

export default function System2() {
  const [movies, setMovies] = useState([]);
  const [recommendMovies, setRecommendMovies] = useState([]);
  const [recommended, setRecommended] = useState(false);
  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/movies`
      );
      let data = await response.json();
      console.log(data);
      setMovies(data);
    };
    fetchData();
  }, []);

  const handleChangeRate = (rate, movieID) => {
    const newMovies = movies.map((movie) => {
      if (movie.MovieID === movieID) {
        return {
          ...movie,
          Rate: rate,
        };
      }
      return movie;
    });
    setMovies(newMovies);
  };

  const handleGetRecommendations = (e) => {
    e.preventDefault();
    const postData = movies.filter((movie) => movie.Rate);
    console.log(postData);
    async function fetchData() {
      const response = await fetch(
        `${import.meta.env.VITE_BACKEND_URL}/api/recommend/collaborative`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(postData),
        }
      );
      const data = await response.json();
      console.log(data);
      setRecommendMovies(data);
      setRecommended(true);
    }
    fetchData();
  };

  return (
    <Box>
      <Box sx={{ display: "flex" }}>
        <Typography variant="h4">Rate some movies below to</Typography>
        <Button
          variant="contained"
          sx={{ marginLeft: 2 }}
          onClick={handleGetRecommendations}
        >
          Get recommendations
        </Button>
      </Box>
      {recommended ? (
        <Box>
          <Button
            sx={{ margin: 1 }}
            variant="outlined"
            onClick={() => setRecommended(false)}
          >
            Try Again
          </Button>
          <Box sx={{ display: "flex", flexFlow: "wrap" }}>
            {recommendMovies.map((movie) => {
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
      ) : (
        <Box sx={{ display: "flex", flexFlow: "wrap" }}>
          {movies.map((movie) => {
            return (
              <Card
                sx={{ width: 200, margin: 1 }}
                key={movie.MovieID}
                variant="outlined"
              >
                <CardContent>
                  <Typography variant="p">{movie.Title}</Typography>
                  <br />
                  <FormControl>
                    <FormLabel id="demo-radio-buttons-group-label">
                      Rate
                    </FormLabel>
                    <RadioGroup
                      aria-labelledby="demo-radio-buttons-group-label"
                      defaultValue="female"
                      name="radio-buttons-group"
                    >
                      {[1, 2, 3, 4, 5].map((rate) => {
                        return (
                          <FormControlLabel
                            key={rate}
                            value={rate}
                            control={<Radio />}
                            label={rate}
                            onChange={() =>
                              handleChangeRate(rate, movie.MovieID)
                            }
                          />
                        );
                      })}
                    </RadioGroup>
                  </FormControl>
                </CardContent>
              </Card>
            );
          })}
        </Box>
      )}
    </Box>
  );
}
