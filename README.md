
## readme


#### https://en.wikipedia.org/wiki/Metasearch_engine


### to run

#### docker
 * docker compose up -- build
 	* or makefile

 #### local
 	* virtual env
 	* will need to setup docker first ie docker compose up -d --build
 		ie so you can hit the search engine
 	* go into .env, update IS_DOCKER=true


 cp .env.sample .env
 provide a gemini key -> it has free tier for now or you can use ollama.

 update IS_DOCKER depending on how you execute code against the search engine.

 default should be IS_DOCKER=true.
 if you want to run python from a virtual environment locally set IS_DOCKER=false

