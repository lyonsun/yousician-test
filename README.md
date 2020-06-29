# Code assignment from Yousician

## How to run

1. [Install Docker Compose](https://docs.docker.com/engine/install/ubuntu/)

2. Clone this code repository onto your computer or any virtual machines in the cloud:

   ```shellscript
   git clone git@github.com:lyonsun/yousician-test.git
   ```

3. Cd into root folder of this code repository:

   ```shellscript
   cd yousician-test
   ```

4. Duplicate file `.env.sample` as `.env` in the same directory (Change credentials in `.env` file if needed). Cd into api folder and do the same thing (Remeber to cd back afterwards for future actions).

   ```shellscript
   cp .env.sample .env
   ```

5. Build all docker services and put the application up and running in the background:

   ```shellscript
   docker-compose up -d
   ```

6. Open your favorite browser, and go to: [http://localhost](http://localhost)

7. Use curl or Postman or any other rest clients you perfer to test the APIs. Endpoints can be found further down in this documentation.

## How to test

1. Open another terminal, and run the following command:

   ```shellscript
   docker exec -it yousician-test-api pytest tests
   ```

   or:

   ```shellscript
   docker exec -it yousician-test-api python -m unittest tests
   ```

2. You should see something similiar to this:

   ```shellscript
   ======================================== test session starts ========================================
   platform linux -- Python 3.7.3, pytest-5.4.3, py-1.9.0, pluggy-0.13.1
   rootdir: /backend-api
   collected 18 items

   tests/test_empty_database.py .                                                                [  5%]
   tests/test_get_all_songs.py ..                                                                [ 16%]
   tests/test_get_average_difficulty.py ..                                                       [ 27%]
   tests/test_get_ratings.py ....                                                                [ 50%]
   tests/test_hello.py .                                                                         [ 55%]
   tests/test_rating.py ......                                                                   [ 88%]
   tests/test_search_songs.py ..                                                                 [100%]

   ======================================== 18 passed in 0.87s =========================================
   ```

## Endpoints

- GET /songs

  - Returns a list of songs with some details on them
  - Add possibility to paginate songs.

- GET /songs/avg/difficulty

  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.

- GET /songs/search

  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.

- POST /songs/rating

  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5.

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.
