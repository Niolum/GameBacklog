import uvicorn
from fastapi import FastAPI

from api.views import user_router, backlog_router, complete_game_router


app = FastAPI()

app.include_router(user_router)
app.include_router(backlog_router)
app.include_router(complete_game_router)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)